import ollama

client = ollama.Client()

model = "qwen3:4b"

user_input = input("Ask something: ")

response = client.chat(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant for e-commerce."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

print("\nQwen says:")
print(response["message"]["content"])