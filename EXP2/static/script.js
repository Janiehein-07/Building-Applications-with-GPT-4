// ================================
// GET ELEMENTS
// ================================

const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const typingContainer = document.getElementById("typingContainer");
const sendButton = document.getElementById("sendButton");

// ================================
// GENERATE BLOG
// ================================

async function generateBlog() {
  const topic = document.getElementById("topic").value.trim();
  const style = document.getElementById("style").value;
  const tone = document.getElementById("tone").value;
  const audience = document.getElementById("audience").value;
  const wordCount = document.getElementById("wordCount").value;
  const instructions = document.getElementById("instructions").value.trim();

  // Check topic

  if (!topic) {
    alert("Please enter a blog topic.");

    document.getElementById("topic").focus();

    return;
  }

  // Create prompt

  let prompt = `
Write a ${wordCount}-word blog on the topic "${topic}".

Writing Style: ${style}
Tone: ${tone}
Target Audience: ${audience}

Requirements:
- Create a suitable and engaging blog title.
- Include an Introduction.
- Include well-structured Main Content.
- Include a Conclusion.
- Use clear and simple English.
- Make the content informative and engaging.
- Try to stay close to ${wordCount} words.
`;

  if (instructions) {
    prompt += `
Additional Instructions:
${instructions}
`;
  }

  // Display the generated request in chat

  addUserMessage(
    `Generate a ${wordCount}-word ${style.toLowerCase()} blog about "${topic}" for ${audience}.`,
  );

  // Show typing

  showTyping();

  sendButton.disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: prompt,
      }),
    });

    const data = await response.json();

    hideTyping();

    if (response.ok) {
      addAIMessage(data.response);
    } else {
      addAIMessage("❌ " + (data.error || "Unable to generate the blog."));
    }
  } catch (error) {
    hideTyping();

    addAIMessage(
      "❌ Unable to connect to the server. Please make sure Flask and Ollama are running.",
    );

    console.error(error);
  }

  sendButton.disabled = false;

  messageInput.focus();
}

// ================================
// NORMAL CHAT MESSAGE
// ================================

async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  addUserMessage(message);

  messageInput.value = "";

  messageInput.style.height = "auto";

  showTyping();

  sendButton.disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: message,
      }),
    });

    const data = await response.json();

    hideTyping();

    if (response.ok) {
      addAIMessage(data.response);
    } else {
      addAIMessage("❌ " + (data.error || "Something went wrong."));
    }
  } catch (error) {
    hideTyping();

    addAIMessage("❌ Unable to connect to the server.");

    console.error(error);
  }

  sendButton.disabled = false;

  messageInput.focus();
}

// ================================
// ADD USER MESSAGE
// ================================

function addUserMessage(message) {
  const messageDiv = document.createElement("div");

  messageDiv.className = "message user-message";

  messageDiv.innerHTML = `

        <div class="message-content">

            <div class="message-name">
                You
            </div>

            <div class="bubble">
                ${escapeHTML(message)}
            </div>

        </div>

        <div class="avatar user-avatar">
            👤
        </div>

    `;

  chatContainer.appendChild(messageDiv);

  scrollToBottom();
}

// ================================
// ADD AI MESSAGE
// ================================

function addAIMessage(message) {
  const messageDiv = document.createElement("div");

  messageDiv.className = "message ai-message";

  messageDiv.innerHTML = `

        <div class="avatar ai-avatar">
            🤖
        </div>

        <div class="message-content">

            <div class="message-name">
                BlogBot
            </div>

            <div class="bubble blog-output">

                ${formatAIResponse(message)}

                <div class="blog-actions">

                    <button onclick="copyBlog(this)">
                        📋 Copy Blog
                    </button>

                </div>

            </div>

        </div>

    `;

  chatContainer.appendChild(messageDiv);

  scrollToBottom();
}

// ================================
// FORMAT AI RESPONSE
// ================================

function formatAIResponse(text) {
  let formatted = escapeHTML(text);

  // Remove unnecessary markdown horizontal lines
  formatted = formatted.replace(/^---+$/gm, "");

  // Main headings
  formatted = formatted.replace(/^### (.*)$/gm, "<h3>$1</h3>");

  formatted = formatted.replace(/^## (.*)$/gm, "<h3>$1</h3>");

  formatted = formatted.replace(/^# (.*)$/gm, "<h2>$1</h2>");

  // Bold text
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Numbered lists
  formatted = formatted.replace(
    /^(\d+)\.\s+(.*)$/gm,
    "<div class='blog-list-item'><span>$1.</span> $2</div>",
  );

  // Bullet lists
  formatted = formatted.replace(
    /^[-*]\s+(.*)$/gm,
    "<div class='blog-list-item'><span>•</span> $1</div>",
  );

  // Convert multiple line breaks
  formatted = formatted.replace(/\n{2,}/g, "<div class='blog-space'></div>");

  // Remaining single line breaks
  formatted = formatted.replace(/\n/g, "<br>");

  return formatted;
}
// ================================
// COPY BLOG
// ================================

function copyBlog(button) {
  const blogBubble = button.closest(".blog-output");

  const clone = blogBubble.cloneNode(true);

  const actions = clone.querySelector(".blog-actions");

  if (actions) {
    actions.remove();
  }

  const text = clone.innerText.trim();

  navigator.clipboard
    .writeText(text)
    .then(() => {
      button.innerHTML = "✅ Copied!";

      setTimeout(() => {
        button.innerHTML = "📋 Copy Blog";
      }, 2000);
    })
    .catch(() => {
      alert("Unable to copy the blog.");
    });
}

// ================================
// SET TOPIC
// ================================

function setTopic(topic) {
  document.getElementById("topic").value = topic;

  document.getElementById("topic").focus();

  document.getElementById("topic").scrollIntoView({
    behavior: "smooth",
    block: "center",
  });
}

// ================================
// NEW CHAT
// ================================

function newChat() {
  chatContainer.innerHTML = `

        <div class="message ai-message">

            <div class="avatar ai-avatar">
                🤖
            </div>

            <div class="message-content">

                <div class="message-name">
                    BlogBot
                </div>

                <div class="bubble welcome-bubble">

                    <h2>👋 Hello!</h2>

                    <p>
                        I'm your AI Blog Content Generator.
                        I can help you create professional
                        and engaging blog content.
                    </p>

                    <p>
                        Enter your blog requirements above
                        and click <strong>Generate Blog</strong>.
                    </p>

                    <div class="suggestions">

                        <button onclick="setTopic('Artificial Intelligence')">
                            🤖 Artificial Intelligence
                        </button>

                        <button onclick="setTopic('Cyber Security')">
                            🔐 Cyber Security
                        </button>

                        <button onclick="setTopic('Electric Vehicles')">
                            🚗 Electric Vehicles
                        </button>

                        <button onclick="setTopic('Climate Change')">
                            🌍 Climate Change
                        </button>

                    </div>

                </div>

            </div>

        </div>

    `;

  document.getElementById("topic").value = "";

  document.getElementById("instructions").value = "";

  messageInput.value = "";

  hideTyping();

  messageInput.focus();

  scrollToBottom();
}

// ================================
// ENTER KEY
// ================================

function handleKeyDown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();

    sendMessage();
  }
}

// ================================
// TEXTAREA AUTO RESIZE
// ================================

messageInput.addEventListener("input", autoResize);

function autoResize() {
  messageInput.style.height = "auto";

  messageInput.style.height = Math.min(messageInput.scrollHeight, 130) + "px";
}

// ================================
// TYPING INDICATOR
// ================================

function showTyping() {
  typingContainer.style.display = "flex";

  scrollToBottom();
}

function hideTyping() {
  typingContainer.style.display = "none";
}

// ================================
// SCROLL
// ================================

function scrollToBottom() {
  setTimeout(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }, 50);
}

// ================================
// HTML SECURITY
// ================================

function escapeHTML(text) {
  const div = document.createElement("div");

  div.textContent = text;

  return div.innerHTML;
}

// ================================
// INITIAL FOCUS
// ================================

messageInput.focus();
