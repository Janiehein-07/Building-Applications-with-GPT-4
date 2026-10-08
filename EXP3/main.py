from flask import Flask, render_template, request

from intent_module import detect_intent
from retrieval_module import retrieve_similar_email
from reply_module import generate_reply
from tone_module import improve_tone
from summary_module import summarize_conversation
from utils import save_reply


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        name = request.form["name"]
        subject = request.form["subject"]
        customer_email = request.form["email"]
        tone = request.form["tone"]

        # Q3 - Intent Detection
        intent = detect_intent(customer_email)

        # Q4/Q5 - Similar Email Retrieval
        similar = retrieve_similar_email(customer_email)

        # Q6 - Generate Reply
        reply = generate_reply(
            customer_email,
            similar["previous_reply"],
            intent
        )

        # Q7 - Tone Improver
        reply = improve_tone(reply, tone)

        # Q8 - Summary
        summary = summarize_conversation(customer_email)

        # Q9 - Save Reply
        save_reply(
            customer_email,
            reply,
            intent
        )

        result = {
            "name": name,
            "subject": subject,
            "intent": intent,
            "previous_email": similar["previous_email"],
            "previous_reply": similar["previous_reply"],
            "similarity": round(
                float(similar["similarity"]),
                2
            ),
            "reply": reply,
            "summary": summary
        }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )