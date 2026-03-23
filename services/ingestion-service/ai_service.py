# ai_service.py

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_incident(service_name, error_message, error_count):
    try:
        prompt = f"""
            Return ONLY valid JSON. No explanation. No markdown.

            Format:
            {{
                "root_cause": "string",
                "severity": "LOW or MEDIUM or HIGH or CRITICAL",
                "suggested_fix": "string"
            }}

            Incident:
            Service: {service_name}
            Error: {error_message}
            Count: {error_count}
            """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        # remove ```json if present
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)
    except Exception as e:
        return {
            "root_cause": "unknown",
            "severity": "LOW",
            "suggested_fix": f"AI failed: {str(e)}"
        }