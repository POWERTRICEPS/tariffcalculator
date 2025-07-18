import openai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))




def extract_json(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        return {"error": "Invalid JSON", "raw": raw}


def gpt_details(product, hts_code, country, base_duty, value_usd):
    prompt = f"""
You are a U.S. customs duty expert.

A product is being imported to the United States with the following info:
- Product: {product}
- HTS Code: {hts_code}
- Base Duty: {base_duty}
- Country of Origin: {country}
- Declared Value: ${value_usd}

Please:
1. Return a JSON object with:
   - base_duty_percent
   - section_301_percent
   - antidumping_percent
   - other_tariffs_percent
   - total_percent
   - total_duty_usd
   - duty_breakdown_explanation: a short paragraph explaining why each duty applies or does not apply in this case.

"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a U.S. customs tariff expert assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content

    parsed = extract_json(raw)
    
    return parsed