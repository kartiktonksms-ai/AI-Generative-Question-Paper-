import io
import os
import json
import time
import warnings
from dotenv import load_dotenv
from xhtml2pdf import pisa
from google import genai
from google.genai import types

load_dotenv()
warnings.filterwarnings("ignore", category=FutureWarning)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not set in .env file")

client = genai.Client(api_key=api_key)

# Try multiple models in order — if one hits quota, fall to the next free-tier model
MODELS = [
    'gemini-2.0-flash-lite',   # lightest, best for free quota
    'gemini-2.0-flash',        # fallback
    'gemini-2.5-flash',        # last resort
]


def _call_gemini(prompt: str) -> str:
    """
    Tries each model in MODELS with 2 attempts per model.
    Returns the raw text response, or raises if all fail.
    """
    last_error = None
    for model_id in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=4096,
                    )
                )
                print(f"[Gemini] Success with model: {model_id}")
                return response.text
            except Exception as e:
                last_error = e
                err_str = str(e)
                if '429' in err_str:
                    wait = 5 if attempt == 0 else 15
                    print(f"[Gemini] {model_id} quota hit, waiting {wait}s…")
                    time.sleep(wait)
                else:
                    print(f"[Gemini] {model_id} error: {e}")
                    break  # Non-quota error — skip this model entirely
    raise last_error


def generate_questions(subject, topic, level,
                       num_mcq=5, num_fill=4, num_match=3,
                       num_short=4, num_long=2):
    """
    Generates a B.Tech CSE question paper using Gemini AI.
    """
    import time
    random_seed = str(time.time())

    prompt = f"""You are an expert B.Tech Computer Science & Engineering professor at an Indian university.
Generate a university-level question paper for:
- Subject: {subject}
- Topic/Unit: {topic}
- Difficulty: {level}

Create EXACTLY:
- {num_mcq} MCQs (4 options each)
- {num_fill} Fill in the Blanks
- {num_match} Match the Following pairs
- {num_short} Short Answer Questions (include marks: 3 each)
- {num_long} Long Answer Questions (include marks: 10 each)

Return ONLY a valid JSON object, NO markdown, NO backticks, NO extra text:
{{
  "MCQs": [
    {{"id": 1, "text": "...", "options": ["opt1","opt2","opt3","opt4"], "answer": "opt1"}}
  ],
  "FillInBlanks": [
    {{"id": 1, "text": "... __________ ...", "answer": "word"}}
  ],
  "MatchTheFollowing": [
    {{"id": 1, "columnA": "Term or concept", "columnB": "Its definition"}}
  ],
  "ShortAnswer": [
    {{"id": 1, "text": "Question?", "answer": "Concise answer", "marks": 3}}
  ],
  "LongAnswer": [
    {{"id": 1, "text": "Detailed question?", "answer": "Key answer points", "marks": 10}}
  ]
}}
All questions must be specifically about "{topic}" in B.Tech CSE "{subject}".
"""

    try:
        text = _call_gemini(prompt).strip()

        # Strip markdown fences if model still wraps in them
        for fence in ['```json', '```']:
            if text.startswith(fence):
                text = text[len(fence):]
                break
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()

        parsed = json.loads(text)

        # Ensure all keys exist
        for key in ['MCQs', 'FillInBlanks', 'MatchTheFollowing', 'ShortAnswer', 'LongAnswer']:
            if key not in parsed:
                parsed[key] = []

        return parsed

    except json.JSONDecodeError as e:
        print(f"[JSON Error] {e} — using mock data")
        return _mock_data(subject, topic, num_mcq, num_fill, num_match, num_short, num_long)
    except Exception as e:
        print(f"[Generation Error] {e} — using mock data")
        return _mock_data(subject, topic, num_mcq, num_fill, num_match, num_short, num_long)


def _mock_data(subject, topic, num_mcq, num_fill, num_match, num_short, num_long):
    """Structured fallback when all API calls fail."""
    return {
        'MCQs': [
            {
                'id': i + 1,
                'text': f'[{subject}] Which of the following best describes "{topic}" concept {i+1}?',
                'options': [
                    f'A key principle of {topic}',
                    f'An unrelated concept to {topic}',
                    f'A common misconception about {topic}',
                    f'None of the above regarding {topic}'
                ],
                'answer': f'A key principle of {topic}'
            }
            for i in range(num_mcq)
        ],
        'FillInBlanks': [
            {'id': i + 1, 'text': f'In {subject}, the process of {topic} involves __________ as a key step.', 'answer': 'processing'}
            for i in range(num_fill)
        ],
        'MatchTheFollowing': [
            {'id': i + 1, 'columnA': f'{topic} Term {i+1}', 'columnB': f'Definition of {topic} Term {i+1}'}
            for i in range(num_match)
        ],
        'ShortAnswer': [
            {
                'id': i + 1,
                'text': f'Briefly explain the concept of {topic} as studied in {subject}. (3 marks)',
                'answer': f'{topic} is a fundamental concept in {subject}.',
                'marks': 3
            }
            for i in range(num_short)
        ],
        'LongAnswer': [
            {
                'id': i + 1,
                'text': f'Discuss {topic} in detail with examples from {subject}. Include its applications, advantages, and limitations. (10 marks)',
                'answer': f'Key points: definition, types, use-cases, advantages, limitations of {topic}.',
                'marks': 10
            }
            for i in range(num_long)
        ],
    }


def save_as_pdf(html_content: str):
    """Converts HTML to PDF via xhtml2pdf. Returns BytesIO or None on error."""
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        io.BytesIO(html_content.encode('utf-8')),
        dest=pdf_file,
        encoding='utf-8',
    )
    if pisa_status.err:
        print(f"[PDF Error] xhtml2pdf reported {pisa_status.err} error(s)")
        return None
    pdf_file.seek(0)
    return pdf_file
