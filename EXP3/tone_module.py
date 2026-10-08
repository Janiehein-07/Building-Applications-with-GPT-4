import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def improve_tone(reply, tone):

    prompt = f"""
Rewrite the following customer support reply in a {tone} tone.

Keep the meaning unchanged.
Make it professional and suitable for an email.

Reply:
{reply}

Rewritten reply:
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