async function getRecommendation() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  const userText = input.value.trim();

  if (userText === "") {
    alert("Please enter your preferences.");
    return;
  }

  // Display user message
  const userMessage = document.createElement("div");

  userMessage.className = "user-message";
  userMessage.innerText = userText;

  chatBox.appendChild(userMessage);

  input.value = "";

  // Loading message
  const loading = document.createElement("div");

  loading.className = "bot-message";
  loading.innerText = "Analyzing your preferences...";

  chatBox.appendChild(loading);

  try {
    const response = await fetch("/recommend", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        profile: userText,
      }),
    });

    const data = await response.json();

    loading.remove();

    const botMessage = document.createElement("div");

    botMessage.className = "bot-message";

    botMessage.innerText = data.recommendation || data.error;

    chatBox.appendChild(botMessage);
  } catch (error) {
    loading.innerText =
      "Something went wrong. Please check whether Ollama is running.";

    console.error(error);
  }

  chatBox.scrollTop = chatBox.scrollHeight;
}
