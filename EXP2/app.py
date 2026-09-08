from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# Ollama model
MODEL = "llama3.2"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "error": "Please enter a message."
            }), 400

        # Prompt for the AI Blog Generator
        prompt = f"""
You are an AI Blog Content Generator.

Your task is to help users create high-quality blog content.

User request:
{user_message}

Instructions:
- Understand what the user wants.
- If they ask for a blog, generate a well-structured blog.
- Use simple and clear English.
- Include a suitable title.
- Include Introduction, Main Content, and Conclusion when appropriate.
- Follow the requested topic, tone, style, audience, and word count.
- Do not mention that you are an AI unless the user specifically asks.
"""

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_response = response["message"]["content"]

        return jsonify({
            "response": ai_response
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "error": "Unable to generate a response. Make sure Ollama is running and Llama 3.2 is installed."
        }), 500


if __name__ == "__main__":
    print("=" * 50)
    print("   AI BLOG CONTENT GENERATOR")
    print("=" * 50)
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)

    app.run(debug=True)