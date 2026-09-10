import ollama


def generate_title(topic):

    prompt = f"""
    Generate 5 engaging and SEO-friendly blog titles
    for the following topic:

    {topic}

    Return only the titles as a numbered list.
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

    return response["message"]["content"]