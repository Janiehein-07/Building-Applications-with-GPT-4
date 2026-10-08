import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_reply(customer_email, previous_reply, intent):

    prompt = f"""
You are a professional customer support assistant.

Customer intent:
{intent}

Customer email:
{customer_email}

Previous similar reply:
{previous_reply}

Generate a professional, helpful and context-aware email reply.

Rules:
- Be polite and professional.
- Clearly address the customer's issue.
- Do not invent order numbers or personal information.
- Do not mention that an AI generated the reply.
- End with "Regards, Support Team".

Reply:
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