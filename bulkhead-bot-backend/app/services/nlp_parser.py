import os
from google import genai
from dotenv import load_dotenv

# This forces Python to load your .env file when testing locally
load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the new modern client
client = genai.Client(api_key=GEMINI_API_KEY)

def normalize_timeline_to_months(raw_timeline: str) -> float:
    """
    Takes a messy human timeline string and uses AI to convert it into a standardized 
    decimal representing months.
    """
    if not raw_timeline or raw_timeline.strip() == "":
        return 0.0

    prompt = f"""
    You are a data parsing assistant. Convert the following project timeline into a 
    single decimal number representing the timeline in MONTHS.
    
    Rules:
    - 1 week = 0.25
    - 2 weeks = 0.5
    - 1 year = 12.0
    - If it's an emergency/ASAP, output 0.0
    - Round to the nearest tenth.
    - Respond ONLY with the number. No text, no explanation.

    Timeline string: "{raw_timeline}"
    """

    try:
        # New syntax for the updated google-genai package
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        # Clean the response to ensure we only have the float
        clean_number = response.text.strip()
        return float(clean_number)
    except Exception as e:
        print(f"Error parsing timeline with AI: {e}")
        # Fallback safely to a high number so it isn't accidentally marked as an urgent emergency
        return 99.0