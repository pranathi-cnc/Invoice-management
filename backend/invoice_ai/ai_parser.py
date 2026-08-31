import os
import json


from dotenv import load_dotenv
from openai import OpenAI

from invoice_ai.prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1"
)


def parse_invoice(ocr_text):

    response = client.chat.completions.create(

        model="Meta-Llama-3.3-70B-Instruct",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": ocr_text
            }
        ],

        temperature=0,

        max_tokens=2500,

        response_format={
            "type": "json_object"
        },

        timeout=120

    )

    json_text = response.choices[0].message.content

    try:
        return json.loads(json_text)

    except Exception as e:

        print("\nLLM Returned Invalid JSON\n")
        print(json_text)

        raise e