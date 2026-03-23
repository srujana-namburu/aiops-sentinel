from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_incident(service_name, error_message, error_count):
    try:
        prompt = f"""
        You are an SRE expert.

        Analyze the following incident:

        Service: {service_name}
        Error: {error_message}
        Count: {error_count}

        Provide:
        1. Root cause
        2. Severity (LOW, MEDIUM, HIGH, CRITICAL)
        3. Suggested fix
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert SRE assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {str(e)}"