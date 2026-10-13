
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("analyzeForm");
    const fileInput = document.getElementById("file");
    const documentInput = document.getElementById("document");
    const submitButton = document.getElementById("analyzeButton");

    if (!form) return;

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            document.querySelector(".upload-title").textContent =
                fileInput.files[0].name;
        }
    });

    form.addEventListener("submit", function (event) {
        const fileSelected = fileInput.files.length > 0;
        const textEntered = documentInput.value.trim() !== "";

        if (!fileSelected && !textEntered) {
            event.preventDefault();
            alert("Please upload a TXT file or enter legal text.");
            return;
        }

        submitButton.disabled = true;
        submitButton.innerHTML = "Analyzing document...";
    });
});
