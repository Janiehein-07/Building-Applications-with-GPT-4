from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Ollama Configuration
# -----------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

# Folder for saved reports
REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


# ============================================================
# 1. EXTRACTED SYMPTOMS
# ============================================================

def extract_symptoms(symptoms):
    """
    Extract and clean symptoms entered by the patient.
    """

    if not symptoms:
        return []

    # Split symptoms using common separators
    separators = [",", "\n", ";"]

    cleaned_text = symptoms

    for separator in separators:
        cleaned_text = cleaned_text.replace(separator, ",")

    symptom_list = []

    for symptom in cleaned_text.split(","):
        symptom = symptom.strip()

        if symptom:
            symptom_list.append(symptom)

    return symptom_list


# ============================================================
# 2. CONTEXT ANALYSIS
# ============================================================

def analyze_context(data, extracted_symptoms):
    """
    Analyze patient information and create context
    for the AI model.
    """

    context = {
        "age": data.get("age", ""),
        "sex": data.get("sex", ""),
        "symptoms": extracted_symptoms,
        "duration": data.get("duration", ""),
        "severity": data.get("severity", ""),
        "medical_history": data.get("medical_history", ""),
        "medication": data.get("medication", ""),
        "allergies": data.get("allergies", ""),
        "additional_info": data.get("additional_info", "")
    }

    return context


# ============================================================
# 3. PROMPT GENERATION
# ============================================================

def generate_prompt(context):
    """
    Generate the prompt that will be sent to Ollama.
    """

    symptoms = ", ".join(context["symptoms"])

    prompt = f"""
You are an AI-powered Medical Symptom Information Assistant.

Your purpose is to provide GENERAL HEALTH INFORMATION only.

You are NOT a doctor and must NOT provide a confirmed diagnosis.

PATIENT INFORMATION

Age:
{context["age"]}

Sex:
{context["sex"]}

Symptoms:
{symptoms}

Duration:
{context["duration"]}

Severity:
{context["severity"]}

Medical History:
{context["medical_history"]}

Current Medication:
{context["medication"]}

Allergies:
{context["allergies"]}

Additional Information:
{context["additional_info"]}


PROVIDE THE RESPONSE USING EXACTLY THESE SECTIONS:

POSSIBLE CONDITIONS

List 2 or 3 possible explanations that may be associated
with the reported symptoms.

Do NOT say that the patient definitely has any condition.


WHY THESE WERE CONSIDERED

Briefly explain why these possibilities may be associated
with the symptoms.


FOLLOW-UP QUESTIONS

Ask useful questions that may help a healthcare professional
understand the situation better.


MEDICAL ATTENTION GUIDANCE

Explain when the patient should contact a healthcare professional.

If symptoms could represent an emergency, clearly recommend
immediate medical attention.


GENERAL SELF-CARE

Provide only general, low-risk suggestions when appropriate.

Do not recommend stopping or changing prescribed medication.


DISCLAIMER

This response provides general informational content only.
It is not a medical diagnosis or a substitute for professional
medical advice.

SAFETY RULES:

- Never give a confirmed diagnosis.
- Never claim certainty.
- Do not recommend stopping prescribed medicines.
- Do not recommend changing medication doses.
- Encourage professional medical attention for severe,
  worsening, or concerning symptoms.
- Use simple language.
"""

    return prompt


# ============================================================
# 4. OLLAMA RESPONSE
# ============================================================

def get_ollama_response(prompt):
    """
    Send the generated prompt to the local Ollama model.
    """

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 600
                }
            },
            timeout=300
        )

        if response.status_code != 200:
            return None, response.text

        result = response.json()

        return result.get("response", ""), None

    except requests.exceptions.ConnectionError:
        return None, "Ollama is not running. Please start Ollama."

    except requests.exceptions.Timeout:
        return None, "Ollama took too long to generate a response."

    except Exception as error:
        return None, str(error)


# ============================================================
# 5. COMPLETE STRUCTURED ANALYSIS
# ============================================================

def structure_analysis(ai_response, extracted_symptoms):
    """
    Create the final structured response.
    """

    structured_result = f"""
COMPLETE STRUCTURED ANALYSIS

--------------------------------------------------

EXTRACTED SYMPTOMS

"""

    for symptom in extracted_symptoms:
        structured_result += f"• {symptom}\n"

    structured_result += f"""

--------------------------------------------------

AI ANALYSIS

{ai_response}

--------------------------------------------------

DISCLAIMER

This AI-powered analysis is provided for general
informational purposes only.

It is NOT a medical diagnosis.

Please consult a qualified healthcare professional
for diagnosis, treatment, or medical advice.

--------------------------------------------------
"""

    return structured_result


# ============================================================
# 6. SAVE REPORT
# ============================================================

def save_report(data, final_result):
    """
    Save the generated analysis as a text report.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"medical_report_{timestamp}.txt"

    filepath = os.path.join(REPORT_FOLDER, filename)

    report = f"""
AI-POWERED MEDICAL SYMPTOM ASSISTANT
====================================

Generated:
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

PATIENT INFORMATION
-------------------

Age: {data.get("age", "")}
Sex: {data.get("sex", "")}

Symptoms:
{data.get("symptoms", "")}

Duration:
{data.get("duration", "")}

Severity:
{data.get("severity", "")}

Medical History:
{data.get("medical_history", "")}

Medication:
{data.get("medication", "")}

Allergies:
{data.get("allergies", "")}

Additional Information:
{data.get("additional_info", "")}


ANALYSIS
--------

{final_result}


DISCLAIMER
----------

This report is for informational purposes only.
It is not a medical diagnosis.
"""

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report)

    return filename


# ============================================================
# HOME SCREEN
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# MAIN ANALYSIS ROUTE
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No patient information received."
        }), 400

    # --------------------------------------------
    # STEP 1: Extract Symptoms
    # --------------------------------------------

    extracted_symptoms = extract_symptoms(
        data.get("symptoms", "")
    )

    if not extracted_symptoms:
        return jsonify({
            "success": False,
            "error": "Please enter at least one symptom."
        }), 400

    # --------------------------------------------
    # STEP 2: Context Analysis
    # --------------------------------------------

    context = analyze_context(
        data,
        extracted_symptoms
    )

    # --------------------------------------------
    # STEP 3: Prompt Generation
    # --------------------------------------------

    prompt = generate_prompt(context)

    # --------------------------------------------
    # STEP 4: Ollama Response
    # --------------------------------------------

    ai_response, error = get_ollama_response(prompt)

    if error:

        return jsonify({
            "success": False,
            "error": error
        }), 500

    # --------------------------------------------
    # STEP 5: Complete Structured Analysis
    # --------------------------------------------

    final_result = structure_analysis(
        ai_response,
        extracted_symptoms
    )

    # --------------------------------------------
    # STEP 6: Save Report
    # --------------------------------------------

    saved_file = save_report(
        data,
        final_result
    )

    # --------------------------------------------
    # SEND RESULT TO FRONTEND
    # --------------------------------------------

    return jsonify({
        "success": True,
        "result": final_result,
        "saved_report": saved_file,
        "extracted_symptoms": extracted_symptoms
    })


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)