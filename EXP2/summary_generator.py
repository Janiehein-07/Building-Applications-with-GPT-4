import ollama


def generate_summary(blog):

    prompt = f"""
    Summarize the following blog in approximately 100 words.

    Blog:
    {blog}

    Return only the summary.
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