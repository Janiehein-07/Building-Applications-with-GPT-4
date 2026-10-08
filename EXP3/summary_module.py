import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def summarize_conversation(customer_email):

    prompt = f"""
Summarize the following customer issue in approximately 50 words.

Customer Email:
{customer_email}

Summary:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()