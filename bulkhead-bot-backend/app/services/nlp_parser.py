import os
import re
from google import genai
from dotenv import load_dotenv


# This forces Python to load your .env file when testing locally
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Initialize the new modern client
client = genai.Client(api_key=GEMINI_API_KEY)




def _convert_timeline_unit_to_months(value: float, unit: str) -> float:
   unit = unit.lower()


   if "day" in unit:
       return round(value / 30.0, 1)
   if "week" in unit:
       return round(value * 0.25, 1)
   if "month" in unit:
       return round(value, 1)
   if "year" in unit:
       return round(value * 12.0, 1)


   return round(value, 1)


NUMBER_WORDS = {
   "a": 1.0,
   "an": 1.0,
   "zero": 0.0,
   "one": 1.0,
   "two": 2.0,
   "three": 3.0,
   "four": 4.0,
   "five": 5.0,
   "six": 6.0,
   "seven": 7.0,
   "eight": 8.0,
   "nine": 9.0,
   "ten": 10.0,
   "eleven": 11.0,
   "twelve": 12.0,
}


def _convert_timeline_value_to_float(value: str) -> float | None:
   if value is None:
       return None

   cleaned_value = value.strip().lower()
   if re.fullmatch(r"\d+(?:\.\d+)?", cleaned_value):
       return float(cleaned_value)

   if cleaned_value in NUMBER_WORDS:
       return NUMBER_WORDS[cleaned_value]

   return None


def normalize_timeline_to_months_hardcoded(raw_timeline: str) -> float | None:
   """
   Hardcoded parser draft.
   Returns a month value when the string can be interpreted locally.
   Returns None when the text should fall back to Gemini.
   """
   if not raw_timeline or raw_timeline.strip() == "":
       return None


   text = raw_timeline.lower().strip()
   text = re.sub(r"[;,()]", " ", text)
   text = re.sub(r"\s+", " ", text)


   urgent_keywords = [
       "soon",
       "asap",
       "urgent",
       "emergency",
       "immediately",
       "right away",
       "soon as possible",
       "as soon as possible",
   ]
   if any(keyword in text for keyword in urgent_keywords):
       return 0.0


   range_match = re.search(
       r"(?P<start>[a-z0-9.]+)\s*(?:-|to)\s*(?P<end>[a-z0-9.]+)\s*(?P<unit>weeks?|months?|years?|days?)",
       text,
   )
   if range_match:
       start = _convert_timeline_value_to_float(range_match.group("start"))
       end = _convert_timeline_value_to_float(range_match.group("end"))
       unit = range_match.group("unit")
       if start is not None and end is not None:
           value = (start + end) / 2.0
           return _convert_timeline_unit_to_months(value, unit)


   single_match = re.search(
       r"(?P<value>[a-z0-9.]+)\s*(?P<unit>weeks?|months?|years?|days?)",
       text,
   )
   if single_match:
       value = _convert_timeline_value_to_float(single_match.group("value"))
       unit = single_match.group("unit")
       if value is not None:
           return _convert_timeline_unit_to_months(value, unit)


   phrase_map = {
       "this week": 0.25,
       "in a week": 0.25,
       "next week": 0.25,
       "couple of weeks": 0.5,
       "a few weeks": 0.75,
       "few weeks": 0.75,
       "this month": 1.0,
       "within a month": 1.0,
       "next month": 1.0,
       "a couple months": 2.0,
       "a few months": 3.0,
       "few months": 3.0,
       "within 1 month": 1.0,
       "within 2 months": 2.0,
       "within 3 months": 3.0,
   }


   for phrase, months in phrase_map.items():
       if phrase in text:
           return months


   return None






def normalize_timeline_to_months(raw_timeline: str) -> float:
   """
   Takes a messy human timeline string and uses AI to convert it into a standardized
   decimal representing months.
   """
   if not raw_timeline or raw_timeline.strip() == "":
       return 99.0


   hardcoded_number = normalize_timeline_to_months_hardcoded(raw_timeline)
   if hardcoded_number is not None:
       return hardcoded_number


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
