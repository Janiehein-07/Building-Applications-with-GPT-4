
import ollama


def analyze_document(prompt):
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2,
            "num_predict": 600
        },
        keep_alive="10m"
    )

    return response["message"]["content"]
