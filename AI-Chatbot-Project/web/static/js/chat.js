/**
 * chat.js — ARIA Chatbot Frontend Logic
 * DecodeLabs AI Project 1 | Batch 2026
 *
 * Handles:
 * - Sending user messages to /api/chat
 * - Rendering bot & user messages
 * - Typing animation
 * - Session stats polling
 * - Mobile sidebar toggle
 * - Quick-topic shortcuts
 * - Session reset
 */

"use strict";

/* ── DOM References ──────────────────────────────────────────── */
const messagesContainer = document.getElementById("messagesContainer");
const messageInput      = document.getElementById("messageInput");
const sendBtn           = document.getElementById("sendBtn");
const typingIndicator   = document.getElementById("typingIndicator");
const charCount         = document.getElementById("charCount");
const resetBtn          = document.getElementById("resetBtn");
const sidebar           = document.getElementById("sidebar");
const sidebarToggle     = document.getElementById("sidebarToggle");
const mobileMenuBtn     = document.getElementById("mobileMenuBtn");
const sidebarOverlay    = document.getElementById("sidebarOverlay");
const statMessages      = document.getElementById("statMessages");
const statDuration      = document.getElementById("statDuration");
const quickBtns         = document.querySelectorAll(".quick-btn");
const welcomeTimeEl     = document.getElementById("welcomeTime");

/* ── State ───────────────────────────────────────────────────── */
let isWaiting   = false;   // Prevent multiple simultaneous requests
let msgCount    = 0;       // Local message counter
let statsTimer  = null;

/* ── Initialization ──────────────────────────────────────────── */
function init() {
  // Set welcome timestamp
  welcomeTimeEl.textContent = getCurrentTime();

  // Bind events
  sendBtn.addEventListener("click", handleSend);
  messageInput.addEventListener("keydown", handleKeydown);
  messageInput.addEventListener("input", handleInputChange);
  resetBtn.addEventListener("click", handleReset);
  sidebarToggle.addEventListener("click", toggleSidebar);
  mobileMenuBtn.addEventListener("click", toggleSidebar);
  sidebarOverlay.addEventListener("click", closeSidebar);

  // Quick topic buttons
  quickBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const msg = btn.dataset.msg;
      if (msg) sendMessage(msg);
      closeSidebar();
    });
  });

  // Auto-resize textarea
  messageInput.addEventListener("input", autoResizeTextarea);

  // Focus input
  messageInput.focus();

  // Start stats polling
  startStatsPolling();
}

/* ── Input Handling ──────────────────────────────────────────── */
function handleKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
}

function handleInputChange() {
  const len = messageInput.value.length;
  charCount.textContent = `${len}/500`;

  // Enable/disable send button
  sendBtn.disabled = len === 0 || isWaiting;

  // Color warn when near limit
  charCount.style.color = len > 450 ? "#f59e0b" : "";
}

function autoResizeTextarea() {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
}

function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
}

/* ── Send Message ────────────────────────────────────────────── */
async function handleSend() {
  const text = messageInput.value.trim();
  if (!text || isWaiting) return;
  sendMessage(text);
}

async function sendMessage(text) {
  if (!text || isWaiting) return;

  // Clear input
  messageInput.value = "";
  messageInput.style.height = "auto";
  charCount.textContent = "0/500";
  sendBtn.disabled = true;

  // Add user message to UI
  appendMessage("user", text, "user");
  msgCount++;

  // Show typing indicator
  showTyping();
  isWaiting = true;

  try {
    // Simulate realistic think time (400–900ms)
    const thinkTime = 400 + Math.random() * 500;

    const [response] = await Promise.all([
      fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      }),
      delay(thinkTime),
    ]);

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    hideTyping();
    appendMessage("bot", data.response, data.category);
    msgCount++;
    updateStats();

    // If farewell, disable input after a pause
    if (data.is_farewell) {
      await delay(1000);
      disableInput("Session ended. Click 'New Session' to start over.");
    }

  } catch (err) {
    hideTyping();
    appendMessage("bot",
      `⚠️ Connection error: ${err.message}\n\nMake sure the Flask server is running on port 5000.`,
      "error"
    );
    console.error("Chat API error:", err);
  } finally {
    isWaiting = false;
    sendBtn.disabled = messageInput.value.trim().length === 0;
    messageInput.focus();
  }
}

/* ── Message Rendering ───────────────────────────────────────── */
function appendMessage(role, text, category = "") {
  const isBot  = role === "bot";
  const isUser = role === "user";

  const wrapper = document.createElement("div");
  wrapper.className = `message ${isBot ? "bot-message" : "user-message"} msg-cat-${category}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = isBot ? "🤖" : "👤";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  const textEl = document.createElement("div");
  textEl.className = "message-text";
  textEl.textContent = text;          // Safe — no innerHTML for user content

  // Convert markdown-like **bold** and \n for display
  textEl.innerHTML = formatResponse(text);

  const timeEl = document.createElement("span");
  timeEl.className = "message-time";
  timeEl.textContent = getCurrentTime();

  bubble.appendChild(textEl);
  bubble.appendChild(timeEl);

  if (isBot) {
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
  } else {
    wrapper.appendChild(bubble);
    wrapper.appendChild(avatar);
  }

  messagesContainer.appendChild(wrapper);
  scrollToBottom();
}

/**
 * Light Markdown-like formatting for bot responses.
 * Converts **text** to <strong>, *text* to <em>, \n to <br>.
 */
function formatResponse(text) {
  // Escape HTML first
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return escaped
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\n/g, "<br />");
}

/* ── Typing Indicator ────────────────────────────────────────── */
function showTyping() {
  typingIndicator.style.display = "flex";
  scrollToBottom();
}

function hideTyping() {
  typingIndicator.style.display = "none";
}

/* ── Scroll ──────────────────────────────────────────────────── */
function scrollToBottom() {
  requestAnimationFrame(() => {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  });
}

/* ── Disable input after farewell ────────────────────────────── */
function disableInput(placeholder) {
  messageInput.disabled = true;
  messageInput.placeholder = placeholder;
  sendBtn.disabled = true;

  // Disable quick buttons
  quickBtns.forEach(btn => {
    btn.disabled = true;
    btn.style.opacity = "0.4";
  });
}

/* ── Stats ───────────────────────────────────────────────────── */
async function updateStats() {
  try {
    const res  = await fetch("/api/stats");
    const data = await res.json();
    statMessages.textContent = data.messages || "0";
    statDuration.textContent = data.duration || "0m 0s";
  } catch {
    // Non-critical — ignore
  }
}

function startStatsPolling() {
  statsTimer = setInterval(updateStats, 10000);  // Every 10s
}

/* ── Session Reset ───────────────────────────────────────────── */
async function handleReset() {
  if (!confirm("Start a new session? Current conversation will be lost.")) return;

  try {
    await fetch("/api/reset", { method: "POST" });
  } catch { /* ignore */ }

  // Clear messages
  messagesContainer.innerHTML = "";
  msgCount = 0;
  statMessages.textContent = "0";
  statDuration.textContent = "0m 0s";
  isWaiting = false;

  // Re-enable input
  messageInput.disabled = false;
  messageInput.placeholder = "Message ARIA... (Press Enter to send, Shift+Enter for new line)";
  sendBtn.disabled = true;

  quickBtns.forEach(btn => {
    btn.disabled = false;
    btn.style.opacity = "";
  });

  // Add fresh welcome message
  appendMessage("bot",
    "🔄 New session started!\n\nHello again! I'm ARIA — ready to assist. What would you like to chat about?",
    "greeting"
  );

  messageInput.focus();
  closeSidebar();
}

/* ── Sidebar Toggle ──────────────────────────────────────────── */
function toggleSidebar() {
  sidebar.classList.toggle("open");
  sidebarOverlay.classList.toggle("active");
}

function closeSidebar() {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.remove("active");
}

/* ── Utility ─────────────────────────────────────────────────── */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/* ── Start ───────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", init);
