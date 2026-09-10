import ollama


def detect_intent(user_input):

    prompt = f"""
    Identify the intent of the following user request.

    Possible intents:
    BLOG
    TITLE
    SUMMARY
    SEO
    UNKNOWN

    User request:
    {user_input}

    Return ONLY one intent name.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip().upper()