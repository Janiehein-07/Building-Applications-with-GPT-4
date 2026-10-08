import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def detect_intent(customer_email):

    prompt = f"""
Classify the following customer email into exactly ONE of these intents:

Delivery Issue
Refund Request
Product Complaint
Technical Support
Order Cancellation
General Inquiry

Customer Email:
{customer_email}

Return only the intent name.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"].strip()

    intents = [
        "Delivery Issue",
        "Refund Request",
        "Product Complaint",
        "Technical Support",
        "Order Cancellation",
        "General Inquiry"
    ]

    for intent in intents:
        if intent.lower() in result.lower():
            return intent

    return "General Inquiry"