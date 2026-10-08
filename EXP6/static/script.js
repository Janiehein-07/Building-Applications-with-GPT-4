// ============================================================
// GET HTML ELEMENTS
// ============================================================

const analyzeButton = document.getElementById("analyzeButton");

const extractedSection = document.getElementById("extractedSection");

const contextSection = document.getElementById("contextSection");

const promptSection = document.getElementById("promptSection");

const aiSection = document.getElementById("aiSection");

const resultSection = document.getElementById("resultSection");

const savedSection = document.getElementById("savedSection");

// ============================================================
// ANALYZE BUTTON
// ============================================================

analyzeButton.addEventListener("click", async function () {
  // --------------------------------------------------------
  // GET INPUT VALUES
  // --------------------------------------------------------

  const age = document.getElementById("age").value;

  const sex = document.getElementById("sex").value;

  const symptoms = document.getElementById("symptoms").value;

  const duration = document.getElementById("duration").value;

  const severity = document.getElementById("severity").value;

  const medicalHistory = document.getElementById("medical_history").value;

  const medication = document.getElementById("medication").value;

  const allergies = document.getElementById("allergies").value;

  const additionalInfo = document.getElementById("additional_info").value;

  // --------------------------------------------------------
  // VALIDATION
  // --------------------------------------------------------

  if (!age) {
    alert("Please enter the patient's age.");

    return;
  }

  if (!symptoms.trim()) {
    alert("Please enter at least one symptom.");

    return;
  }

  if (!duration.trim()) {
    alert("Please enter the symptom duration.");

    return;
  }

  // --------------------------------------------------------
  // DISABLE BUTTON
  // --------------------------------------------------------

  analyzeButton.disabled = true;

  analyzeButton.innerText = "Analyzing... Please wait";

  // --------------------------------------------------------
  // HIDE OLD RESULTS
  // --------------------------------------------------------

  extractedSection.classList.add("hidden");

  contextSection.classList.add("hidden");

  promptSection.classList.add("hidden");

  aiSection.classList.add("hidden");

  resultSection.classList.add("hidden");

  savedSection.classList.add("hidden");

  // --------------------------------------------------------
  // PREPARE DATA
  // --------------------------------------------------------

  const patientData = {
    age: age,

    sex: sex,

    symptoms: symptoms,

    duration: duration,

    severity: severity,

    medical_history: medicalHistory,

    medication: medication,

    allergies: allergies,

    additional_info: additionalInfo,
  };

  // ========================================================
  // FRONTEND → BACKEND
  // ========================================================

  try {
    const response = await fetch("/analyze", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(patientData),
    });

    const data = await response.json();

    // ====================================================
    // ERROR
    // ====================================================

    if (!data.success) {
      alert("Error: " + data.error);

      analyzeButton.disabled = false;

      analyzeButton.innerText = "Analyze Symptoms";

      return;
    }

    // ====================================================
    // 1. EXTRACTED SYMPTOMS
    // ====================================================

    showExtractedSymptoms(data.extracted_symptoms);

    // ====================================================
    // 2. CONTEXT ANALYSIS
    // ====================================================

    showContextAnalysis(patientData);

    // ====================================================
    // 3. PROMPT GENERATION
    // ====================================================

    promptSection.classList.remove("hidden");

    // ====================================================
    // 4. AI RESPONSE
    // ====================================================

    showAIResponse(data.result);

    // ====================================================
    // 5. COMPLETE STRUCTURED ANALYSIS
    // ====================================================

    document.getElementById("result").innerText = data.result;

    resultSection.classList.remove("hidden");

    // ====================================================
    // 6. SAVED REPORT
    // ====================================================

    document.getElementById("savedReport").innerText = data.saved_report;

    savedSection.classList.remove("hidden");

    // ====================================================
    // SCROLL TO RESULT
    // ====================================================

    resultSection.scrollIntoView({
      behavior: "smooth",

      block: "start",
    });
  } catch (error) {
    alert("Unable to connect to the Flask server.");

    console.error(error);
  }

  // --------------------------------------------------------
  // ENABLE BUTTON
  // --------------------------------------------------------

  analyzeButton.disabled = false;

  analyzeButton.innerText = "Analyze Symptoms";
});

// ============================================================
// SHOW EXTRACTED SYMPTOMS
// ============================================================

function showExtractedSymptoms(symptoms) {
  const container = document.getElementById("extractedSymptoms");

  container.innerHTML = "";

  symptoms.forEach(function (symptom) {
    const tag = document.createElement("span");

    tag.className = "symptom-tag";

    tag.innerText = symptom;

    container.appendChild(tag);
  });

  extractedSection.classList.remove("hidden");
}

// ============================================================
// SHOW CONTEXT ANALYSIS
// ============================================================

function showContextAnalysis(data) {
  const container = document.getElementById("contextContent");

  container.innerHTML = `

        <div class="context-grid">

            <div class="context-item">

                <strong>Age</strong>

                ${escapeHTML(data.age)}

            </div>


            <div class="context-item">

                <strong>Sex</strong>

                ${escapeHTML(data.sex || "Not provided")}

            </div>


            <div class="context-item">

                <strong>Duration</strong>

                ${escapeHTML(data.duration)}

            </div>


            <div class="context-item">

                <strong>Severity</strong>

                ${escapeHTML(data.severity)}

            </div>


            <div class="context-item">

                <strong>Medical History</strong>

                ${escapeHTML(data.medical_history || "None provided")}

            </div>


            <div class="context-item">

                <strong>Medication</strong>

                ${escapeHTML(data.medication || "None provided")}

            </div>


            <div class="context-item">

                <strong>Allergies</strong>

                ${escapeHTML(data.allergies || "None provided")}

            </div>


            <div class="context-item">

                <strong>Additional Information</strong>

                ${escapeHTML(data.additional_info || "None provided")}

            </div>

        </div>

    `;

  contextSection.classList.remove("hidden");
}

// ============================================================
// SHOW AI RESPONSE
// ============================================================

function showAIResponse(response) {
  const container = document.getElementById("aiContent");

  container.innerText = response;

  aiSection.classList.remove("hidden");
}

// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHTML(text) {
  const div = document.createElement("div");

  div.innerText = text;

  return div.innerHTML;
}
