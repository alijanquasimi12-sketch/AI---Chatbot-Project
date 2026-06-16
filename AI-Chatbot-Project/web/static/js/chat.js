/**
 * chat.js — ARIA × KMA² Intelligence Framework
 * KMA² Signature Series | Frontend Chat Engine v2.0
 * =====================================================
 * Handles: loading screen, chat UI, API calls, animations
 */

'use strict';

// ── DOM References ────────────────────────────────────────────
const loadingScreen    = document.getElementById('loadingScreen');
const loadingBar       = document.getElementById('loadingBar');
const loadingStatus    = document.getElementById('loadingStatus');
const messagesContainer = document.getElementById('messagesContainer');
const messageInput     = document.getElementById('messageInput');
const sendBtn          = document.getElementById('sendBtn');
const charCount        = document.getElementById('charCount');
const typingIndicator  = document.getElementById('typingIndicator');
const resetBtn         = document.getElementById('resetBtn');
const sidebarToggle    = document.getElementById('sidebarToggle');
const mobileMenuBtn    = document.getElementById('mobileMenuBtn');
const sidebar          = document.getElementById('sidebar');
const sidebarOverlay   = document.getElementById('sidebarOverlay');
const welcomeTime      = document.getElementById('welcomeTime');
const statMessages     = document.getElementById('statMessages');
const statDuration     = document.getElementById('statDuration');

// Settings & Modals
const settingsBtn      = document.getElementById('settingsBtn');
const settingsMenu     = document.getElementById('settingsMenu');
const themeToggle      = document.getElementById('themeToggle');
const privacyToggle    = document.getElementById('privacyToggle');
const privacyLockIcon  = document.getElementById('privacyLockIcon');
const aboutDevBtn      = document.getElementById('aboutDevBtn');
const aboutProjBtn     = document.getElementById('aboutProjBtn');
const menuResetBtn     = document.getElementById('menuResetBtn');
const modalOverlay     = document.getElementById('modalOverlay');
const floatingPrivacyBtn = document.getElementById('floatingPrivacyBtn');
const privacyToast       = document.getElementById('privacyToast');

// ── State ─────────────────────────────────────────────────────
let isWaitingResponse = false;
let statsInterval = null;

// ── Loading Screen ────────────────────────────────────────────
const LOADING_STEPS = [
  { pct: 15, msg: 'Initializing intelligence framework...' },
  { pct: 35, msg: 'Loading knowledge base (300+ intents)...' },
  { pct: 55, msg: 'Calibrating pattern recognition...' },
  { pct: 75, msg: 'Connecting KMA² engine...' },
  { pct: 92, msg: 'ARIA is ready. Launching interface...' },
  { pct: 100, msg: 'Welcome to KMA² Signature Series.' },
];

function runLoadingSequence() {
  let step = 0;
  const totalDuration = 2600; // ms
  const stepDelay = totalDuration / LOADING_STEPS.length;

  function nextStep() {
    if (step >= LOADING_STEPS.length) {
      // Dismiss loading screen
      setTimeout(() => {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => {
          loadingScreen.style.display = 'none';
        }, 700);
      }, 350);
      return;
    }
    const { pct, msg } = LOADING_STEPS[step];
    loadingBar.style.width = pct + '%';
    loadingStatus.textContent = msg;
    step++;
    setTimeout(nextStep, stepDelay);
  }

  nextStep();
}

// Start loading sequence on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  runLoadingSequence();
  welcomeTime.textContent = getCurrentTime();
  startStatsPolling();

  // Load saved theme
  const savedTheme = localStorage.getItem('aria-theme');
  if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    themeToggle.checked = true;
  }
});

// ── Utility Functions ─────────────────────────────────────────
function getCurrentTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom(smooth = true) {
  setTimeout(() => {
    messagesContainer.scrollTo({
      top: messagesContainer.scrollHeight,
      behavior: smooth ? 'smooth' : 'instant',
    });
  }, 40);
}

function setInputState(disabled) {
  messageInput.disabled = disabled;
  sendBtn.disabled = disabled || messageInput.value.trim().length === 0;
  isWaitingResponse = disabled;
}

// ── Message Rendering ─────────────────────────────────────────
function createUserMessage(text) {
  const el = document.createElement('div');
  el.className = 'message user-message';
  el.innerHTML = `
    <div class="user-avatar">U</div>
    <div class="message-bubble">
      <div class="message-text"><p>${escapeHtml(text)}</p></div>
      <span class="message-time">${getCurrentTime()}</span>
    </div>
  `;
  return el;
}

function createBotMessage(text, isWelcome = false) {
  const el = document.createElement('div');
  el.className = 'message bot-message' + (isWelcome ? ' welcome-message' : '');

  const formattedText = formatBotText(text);

  el.innerHTML = `
    <div class="message-avatar">
      <img src="/static/images/kma2-logo.png" alt="ARIA" class="msg-avatar-img" />
    </div>
    <div class="message-bubble">
      <div class="message-text">${formattedText}</div>
      <span class="message-time">${getCurrentTime()}</span>
    </div>
  `;
  return el;
}

function formatBotText(text) {
  if (!text) return '';

  // Escape HTML
  let safe = escapeHtml(text);

  // Convert **bold**
  safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Convert line breaks to <br> — preserve spacing in preformatted responses
  // Detect multiline (contains \n) responses → render as pre-text
  if (safe.includes('\n')) {
    // Convert blank lines to paragraph breaks
    const paragraphs = safe.split(/\n\n+/);
    if (paragraphs.length > 1) {
      return paragraphs.map(p => {
        const lines = p.replace(/\n/g, '<br>');
        return `<p>${lines}</p>`;
      }).join('');
    } else {
      return `<p>${safe.replace(/\n/g, '<br>')}</p>`;
    }
  }

  return `<p>${safe}</p>`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

// ── Typing Indicator ──────────────────────────────────────────
function showTyping() {
  typingIndicator.style.display = 'flex';
  scrollToBottom();
}

function hideTyping() {
  typingIndicator.style.display = 'none';
}

// ── API Call ──────────────────────────────────────────────────
async function sendMessage() {
  const text = messageInput.value.trim();
  if (!text || isWaitingResponse) return;

  // Render user message
  const userEl = createUserMessage(text);
  messagesContainer.appendChild(userEl);
  scrollToBottom();

  // Clear input
  messageInput.value = '';
  charCount.textContent = '0/500';
  autoResizeTextarea();

  // Disable input & show typing
  setInputState(true);
  showTyping();

  // Simulate realistic AI "thinking" delay
  const delay = 600 + Math.random() * 600;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });

    await new Promise(r => setTimeout(r, delay));
    hideTyping();

    if (!res.ok) throw new Error('API error: ' + res.status);

    const data = await res.json();
    const botEl = createBotMessage(data.response);
    messagesContainer.appendChild(botEl);
    scrollToBottom();

    // Handle farewell
    if (data.is_farewell) {
      setTimeout(() => {
        const hint = document.createElement('p');
        hint.style.cssText = 'text-align:center; color:var(--text-muted); font-size:0.72rem; padding:8px; opacity:0.7;';
        hint.textContent = 'Session ended. Click "New Session" to start fresh.';
        messagesContainer.appendChild(hint);
        scrollToBottom();
      }, 800);
    }

    // Update user avatar initials if name known
    if (data.user_name && data.user_name !== 'Unknown') {
      document.querySelectorAll('.user-avatar').forEach(el => {
        el.textContent = data.user_name.charAt(0).toUpperCase();
      });
    }

  } catch (err) {
    hideTyping();
    const errEl = createBotMessage("I encountered a connection issue. Please make sure the server is running and try again.");
    messagesContainer.appendChild(errEl);
    scrollToBottom();
    console.error('Chat error:', err);
  } finally {
    setInputState(false);
    messageInput.focus();
    updateStats();
  }
}

// ── Event Listeners ───────────────────────────────────────────
messageInput.addEventListener('input', () => {
  const len = messageInput.value.length;
  charCount.textContent = `${len}/500`;
  sendBtn.disabled = len === 0 || isWaitingResponse;

  // Color warning at 80% usage
  charCount.style.color = len > 400 ? '#e97070' : '';
  autoResizeTextarea();
});

messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) sendMessage();
  }
});

sendBtn.addEventListener('click', sendMessage);

// Quick topic buttons
document.querySelectorAll('.quick-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const msg = btn.dataset.msg;
    if (msg && !isWaitingResponse) {
      messageInput.value = msg;
      charCount.textContent = `${msg.length}/500`;
      sendBtn.disabled = false;
      autoResizeTextarea();
      sendMessage();
      // Close sidebar on mobile after selecting
      if (window.innerWidth <= 768) closeSidebar();
    }
  });
});

// Reset session function
async function handleReset() {
  try {
    await fetch('/api/reset', { method: 'POST' });
    while (messagesContainer.children.length > 1) {
      messagesContainer.removeChild(messagesContainer.lastChild);
    }
    updateStats();
    if (settingsMenu) settingsMenu.classList.remove('open');
  } catch (err) {
    console.error('Reset error:', err);
  }
}

resetBtn.addEventListener('click', handleReset);
if (menuResetBtn) menuResetBtn.addEventListener('click', handleReset);

// Sidebar toggle (desktop)
sidebarToggle?.addEventListener('click', () => {
  sidebar.classList.toggle('collapsed');
});

// Mobile sidebar open
mobileMenuBtn?.addEventListener('click', openSidebar);
sidebarOverlay?.addEventListener('click', closeSidebar);

function openSidebar() {
  sidebar.classList.add('open');
  sidebarOverlay.classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeSidebar() {
  sidebar.classList.remove('open');
  sidebarOverlay.classList.remove('show');
  document.body.style.overflow = '';
}

// ── Auto-resize textarea ──────────────────────────────────────
function autoResizeTextarea() {
  messageInput.style.height = 'auto';
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// ── Stats Polling ─────────────────────────────────────────────
async function updateStats() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) return;
    const data = await res.json();
    if (statMessages) statMessages.textContent = data.messages ?? 0;
    if (statDuration) statDuration.textContent = data.duration ?? '0m 0s';
  } catch (_) {
    // Silently ignore stats errors
  }
}

function startStatsPolling() {
  updateStats();
  statsInterval = setInterval(updateStats, 10000);
}

// ── Focus input after load ────────────────────────────────────
setTimeout(() => {
  if (window.innerWidth > 768) messageInput?.focus();
}, 3000); // After loading screen finishes

// ── Settings Menu & Theme Logic ───────────────────────────────
settingsBtn?.addEventListener('click', (e) => {
  e.stopPropagation();
  settingsMenu.classList.toggle('open');
});

document.addEventListener('click', (e) => {
  if (settingsMenu?.classList.contains('open') && !settingsMenu.contains(e.target) && e.target !== settingsBtn) {
    settingsMenu.classList.remove('open');
  }
});

// Theme Switcher
themeToggle?.addEventListener('change', (e) => {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('aria-theme', 'light');
  } else {
    document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('aria-theme', 'dark');
  }
});

// Privacy Mode Logic
function setPrivacyMode(enabled) {
  if (enabled) {
    messagesContainer.classList.add('privacy-mode');
    if (privacyLockIcon) privacyLockIcon.style.display = 'inline-block';
    if (privacyToggle) privacyToggle.checked = true;
    if (floatingPrivacyBtn) {
      floatingPrivacyBtn.classList.add('active');
      floatingPrivacyBtn.querySelector('.privacy-icon-unlocked').style.display = 'none';
      floatingPrivacyBtn.querySelector('.privacy-icon-locked').style.display = 'block';
    }
    if (privacyToast) {
      privacyToast.classList.add('show');
      setTimeout(() => privacyToast.classList.remove('show'), 3000);
    }
  } else {
    messagesContainer.classList.remove('privacy-mode');
    if (privacyLockIcon) privacyLockIcon.style.display = 'none';
    if (privacyToggle) privacyToggle.checked = false;
    if (floatingPrivacyBtn) {
      floatingPrivacyBtn.classList.remove('active');
      floatingPrivacyBtn.querySelector('.privacy-icon-unlocked').style.display = 'block';
      floatingPrivacyBtn.querySelector('.privacy-icon-locked').style.display = 'none';
    }
    if (privacyToast) privacyToast.classList.remove('show');
  }
}

privacyToggle?.addEventListener('change', (e) => {
  setPrivacyMode(e.target.checked);
});

floatingPrivacyBtn?.addEventListener('click', () => {
  const isEnabled = messagesContainer.classList.contains('privacy-mode');
  setPrivacyMode(!isEnabled);
});

// ── Modals Logic ──────────────────────────────────────────────
function openModal(modalId) {
  settingsMenu?.classList.remove('open');
  modalOverlay.classList.add('show');
  document.getElementById(modalId).classList.add('active');
}

function closeModals() {
  modalOverlay.classList.remove('show');
  document.querySelectorAll('.custom-modal').forEach(m => m.classList.remove('active'));
}

aboutDevBtn?.addEventListener('click', () => openModal('devModal'));
aboutProjBtn?.addEventListener('click', () => openModal('projModal'));

document.querySelectorAll('.modal-close').forEach(btn => {
  btn.addEventListener('click', () => closeModals());
});

modalOverlay?.addEventListener('click', (e) => {
  if (e.target === modalOverlay) closeModals();
});
