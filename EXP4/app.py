from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.json

    user_profile = data.get("profile", "")

    prompt = f"""
You are a personalized recommendation assistant.

Analyze the following user profile:

{user_profile}

Give exactly 5 personalized learning recommendations.

For each recommendation provide:

1. Recommendation name
2. Reason
3. Score out of 100

Consider:
- User interests
- Skill level
- Learning goal
- Preferred learning style
- Multiple interests

Return the answer in a simple format.

Example:

1. Python for AI
Reason: Matches the user's Python and AI interests.
Score: 95%

2. Machine Learning Basics
Reason: Suitable for a beginner interested in AI.
Score: 92%
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:4b",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        return jsonify({
            "recommendation": result["response"]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)