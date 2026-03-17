import google.generativeai as genai
import os

# API_KEY = 'AIzaSyB3NGFc0v4qqBm4bxgTHALNGs-FMNemha8'
API_KEY = 'AIzaSyB3NGFc0v4qqBm4bxgTHALNGs-FMNemha8'

print(f"Configuring API...")
try:
    genai.configure(api_key=API_KEY)
    
    print("Attempting with 'gemini-2.0-flash'...")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, do you work?")
    print("\nSuccess! Response:", response.text)
    
except Exception as e:
    print(f"\nError: {e}")
