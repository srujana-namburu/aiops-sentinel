import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RAG_URL = "http://127.0.0.1:8002/retrieve"

def get_rag_context(error_message):
    try:
        res = requests.get(RAG_URL, params={"query": error_message})
        return res.json().get("context", "")
    except:
        return ""

def analyze_incident(service_name, error_message, error_count):
    context = get_rag_context(error_message)

    prompt = f"""
You are an SRE AI assistant.

Incident:
Service: {service_name}
Error: {error_message}
Count: {error_count}

Runbook:
{context}

Classify severity (LOW, MEDIUM, HIGH, CRITICAL)
Suggest action.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content

    severity = "LOW"
    if "CRITICAL" in output:
        severity = "CRITICAL"
    elif "HIGH" in output:
        severity = "HIGH"
    elif "MEDIUM" in output:
        severity = "MEDIUM"

    return {
        "analysis": output,
        "severity": severity
    }