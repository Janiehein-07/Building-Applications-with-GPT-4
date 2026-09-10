import ollama


def generate_seo(blog):

    prompt = f"""
    Analyze the following blog and generate:

    1. 10 SEO keywords
    2. One SEO-friendly meta description of approximately 150-160 characters

    Blog:
    {blog}

    Format your response clearly.
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