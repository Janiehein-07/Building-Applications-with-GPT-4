
from flask import Flask, render_template, request, send_file
from preprocessing import preprocess_text
from prompt import create_prompt
from legal_analyzer import analyze_document
import os
import time

app = Flask(__name__)

OUTPUT_FOLDER = "outputs"
REPORT_PATH = os.path.join(OUTPUT_FOLDER, "legal_analysis.txt")

# Prevent accidentally uploading extremely large requests.
# Increase this if you need to analyze larger documents.
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    total_start = time.perf_counter()

    try:
        # Step 1: Read the uploaded file or entered text
        start = time.perf_counter()

        uploaded_file = request.files.get("file")
        entered_text = request.form.get("document", "")

        if uploaded_file and uploaded_file.filename:
            document = uploaded_file.read().decode("utf-8-sig")
        else:
            document = entered_text

        print(f"Document reading: {time.perf_counter() - start:.2f}s")

        if not document.strip():
            return render_template(
                "index.html",
                error="Please upload a document or enter legal text."
            )

        # Step 2: Preprocess the document
        start = time.perf_counter()
        cleaned_document = preprocess_text(document)
        print(f"Preprocessing: {time.perf_counter() - start:.2f}s")

        if not cleaned_document.strip():
            return render_template(
                "index.html",
                error="No usable text found in the document."
            )

        # Step 3: Create the AI prompt
        start = time.perf_counter()
        prompt = create_prompt(cleaned_document)
        print(f"Prompt creation: {time.perf_counter() - start:.2f}s")
        print(f"Prompt length: {len(prompt)} characters")

        # Step 4: Analyze using Ollama
        start = time.perf_counter()
        analysis = analyze_document(prompt)
        print(f"Ollama analysis: {time.perf_counter() - start:.2f}s")

        if not analysis or not analysis.strip():
            return render_template(
                "index.html",
                error="The AI returned an empty response. Please try again."
            )

        # Step 5: Save the downloadable report
        start = time.perf_counter()
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        with open(REPORT_PATH, "w", encoding="utf-8") as file:
            file.write(analysis)

        print(f"Report saving: {time.perf_counter() - start:.2f}s")
        print(f"Total processing time: {time.perf_counter() - total_start:.2f}s")

        return render_template("index.html", analysis=analysis)

    except UnicodeDecodeError:
        return render_template(
            "index.html",
            error="Unable to read this file as UTF-8 text. Please use a valid TXT file."
        )

    except Exception as error:
        app.logger.exception("Document analysis failed")
        return render_template(
            "index.html",
            error="Analysis failed. Check the VS Code terminal for details."
        )


@app.route("/download")
def download_report():
    if os.path.exists(REPORT_PATH):
        return send_file(
            REPORT_PATH,
            as_attachment=True,
            download_name="legal_analysis.txt",
            mimetype="text/plain"
        )

    return "Report not found.", 404


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="The uploaded request is too large. Please use a smaller document."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
