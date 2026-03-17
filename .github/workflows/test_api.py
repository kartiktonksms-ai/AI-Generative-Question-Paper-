import google.generativeai as genai
import os

API_KEY = 'AIzaSyB3NGFc0v4qqBm4bxgTHALNGs-FMNemha8'

print(f"Configuring API with key: {API_KEY[:5]}...")
try:
    genai.configure(api_key=API_KEY)
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
    print("\nAttempting with 'gemini-2.0-flash'...")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello")
    print("\nSuccess! Response:", response.text)
except Exception as e:
    print(f"\nFinal Error: {e}")
