import re

from openai import OpenAI
import json

from dotenv import load_dotenv  
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

def ask_openai(prompt:str):
    resp = openai_client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )

    raw_text = resp.choices[0].message.content
    print("Raw response from OpenAI:", raw_text)  # Debugging statement
    # Strip accidental markdown fences if present
    raw_text = re.sub(r"^```json\s*|```$", "", raw_text, flags=re.MULTILINE).strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        return raw_text