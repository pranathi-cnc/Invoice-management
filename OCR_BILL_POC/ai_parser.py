import json
import os

from dotenv import load_dotenv
from google import genai

from prompt import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_invoice(ocr_text):

    prompt = f"""
{SYSTEM_PROMPT}

OCR TEXT

-------------------------

{ocr_text}

-------------------------
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini returns it
    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    try:
        data = json.loads(text)

    except Exception:

        print(text)

        raise Exception("Gemini did not return valid JSON.")

    return data