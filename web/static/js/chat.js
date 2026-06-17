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
const statMessages     = document.getElementById('statMessages');
const statDuration     = document.getElementById('statDuration');

// Settings & Modals
const settingsBtn      = document.getElementById('settingsBtn');
const settingsMenu     = document.getElementById('settingsMenu');
const themeToggle      = document.getElementById('themeToggle');
const aboutDevBtn      = document.getElementById('aboutDevBtn');
const aboutProjBtn     = document.getElementById('aboutProjBtn');
const menuResetBtn     = document.getElementById('menuResetBtn');
const modalOverlay     = document.getElementById('modalOverlay');

// Privacy Mode (Nav Bar)
const privacyNavBtn          = document.getElementById('privacyNavBtn');
const privateSessionBanner   = document.getElementById('privateSessionBanner');
const privacyToast           = document.getElementById('privacyToast');

// ── State ─────────────────────────────────────────────────────
let isWaitingResponse = false;
let statsInterval = null;
let currentChatId = null;
let currentSearchQuery = '';
let ariaMode = localStorage.getItem('aria_mode') || 'normal';

// Multi-Chat DOM
const newChatBtn       = document.getElementById('newChatBtn');
const chatList         = document.getElementById('chatList');
const pinnedChatList   = document.getElementById('pinnedChatList');
const chatSearchInput  = document.getElementById('chatSearchInput');
const recentlyDeletedBtn = document.getElementById('recentlyDeletedBtn');
const deletedChatsContainer = document.getElementById('deletedChatsContainer');

// Stats Modal DOM
const statsModal       = document.getElementById('statsModal');
const openStatsBtn     = document.getElementById('openStatsBtn');
const closeStatsBtn    = document.getElementById('closeStatsBtn');
const dashChats        = document.getElementById('dashChats');
const dashMessages     = document.getElementById('dashMessages');
const dashPinned       = document.getElementById('dashPinned');
const dashDuration     = document.getElementById('dashDuration');
const dashLanguages    = document.getElementById('dashLanguages');
const dashVoice        = document.getElementById('dashVoice');
const dashPdf          = document.getElementById('dashPdf');
const dashTxt          = document.getElementById('dashTxt');

// Mode Selector DOM
const modeIndicatorBtn = document.getElementById('modeIndicatorBtn');
const modeMenu         = document.getElementById('modeMenu');
const headerModeText   = document.getElementById('headerModeText');

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

  function dismissLoadingScreen() {
    if (loadingScreen && loadingScreen.style.display !== 'none') {
      loadingScreen.classList.add('fade-out');
      setTimeout(() => {
        loadingScreen.style.display = 'none';
      }, 700);
    }
  }

  // Failsafe: Automatically dismiss after 3.5s no matter what
  setTimeout(dismissLoadingScreen, 3500);

  function nextStep() {
    if (step >= LOADING_STEPS.length) {
      setTimeout(dismissLoadingScreen, 350);
      return;
    }
    
    try {
      const { pct, msg } = LOADING_STEPS[step];
      if (loadingBar) loadingBar.style.width = pct + '%';
      if (loadingStatus) loadingStatus.textContent = msg;
    } catch (err) {
      console.error("Loading step error, continuing...", err);
    }
    
    step++;
    setTimeout(nextStep, stepDelay);
  }

  nextStep();
}

document.addEventListener('DOMContentLoaded', () => {
  runLoadingSequence();
  startStatsPolling();

  // Load saved theme
  const savedTheme = localStorage.getItem('aria-theme');
  if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    themeToggle.checked = true;
  }

  // Initialize Multi-Chat System
  initMultiChat();
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

function createBotMessage(text, isWelcome = false, isHistory = false) {
  const el = document.createElement('div');
  el.className = 'message bot-message' + (isWelcome ? ' welcome-message' : '');

  const formattedText = formatBotText(text);
  
  const isPinned = isHistory && window.currentPinnedTexts && window.currentPinnedTexts.has(text);
  const pinHtml = isPinned
    ? `<button class="msg-pin-btn is-pinned" onclick="togglePin(this)" aria-label="Pin message" style="color: #4CAF50; border-color: #4CAF50;">📌 Pinned</button>`
    : `<button class="msg-pin-btn" onclick="togglePin(this)" aria-label="Pin message">📌 Pin</button>`;

  // We add a data attribute to store the raw text for pinning
  el.setAttribute('data-raw-text', escapeHtml(text));

  el.innerHTML = `
    <div class="message-avatar">
      <img src="/static/images/kma2-logo.png" alt="ARIA" class="msg-avatar-img" />
    </div>
    <div class="message-bubble" style="display: flex; flex-direction: column;">
      <div class="message-text">${formattedText}</div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
        <span class="message-time">${getCurrentTime()}</span>
        ${!isWelcome ? pinHtml : ''}
      </div>
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
let thinkingInterval = null;

function showTyping(durationMs = 2000) {
  const typingIndicator = document.getElementById('typingIndicator');
  const thinkingText = document.getElementById('thinkingText');
  const ideaBulb = document.querySelector('.robot-idea-bulb');
  
  if (typingIndicator) {
    typingIndicator.style.display = 'flex';
    typingIndicator.classList.remove('fade-out');
  }
  
  scrollToBottom();

  if (!thinkingText) return;

  const phases = [
    "Analyzing Request...",
    "Understanding Intent...",
    "Accessing Knowledge Base...",
    "Generating Response...",
    "✓ Response Ready"
  ];
  
  let i = 0;
  thinkingText.textContent = phases[0];
  thinkingText.classList.remove('fade-out', 'idea-ready');
  if (ideaBulb) ideaBulb.classList.remove('show');
  
  clearInterval(thinkingInterval);
  
  // Distribute the 5 phases over the total duration
  const phaseTime = durationMs / phases.length;
  
  thinkingInterval = setInterval(() => {
    i++;
    if (i < phases.length) {
      thinkingText.classList.add('fade-out');
      setTimeout(() => {
        thinkingText.textContent = phases[i];
        thinkingText.classList.remove('fade-out');
        
        // Final phase: "Response Ready" -> Idea found!
        if (i === phases.length - 1) {
          thinkingText.classList.add('idea-ready');
          if (ideaBulb) ideaBulb.classList.add('show');
        }
      }, phaseTime * 0.3); // Wait for fade out
    } else {
      clearInterval(thinkingInterval);
    }
  }, phaseTime);
}

function hideTyping() {
  const typingIndicator = document.getElementById('typingIndicator');
  if (typingIndicator) {
    typingIndicator.classList.add('fade-out');
    setTimeout(() => {
      typingIndicator.style.display = 'none';
      typingIndicator.classList.remove('fade-out');
    }, 300); // 300ms fade transition
  }
  clearInterval(thinkingInterval);
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

  // Remove welcome panel if exists
  const welcomePanel = messagesContainer.querySelector('.welcome-panel');
  if (welcomePanel) {
    welcomePanel.remove();
  }

  // Smart Timing: Simple (< 30 chars) 1-2s, Complex (>= 30 chars) 2-4s
  const isComplex = text.length >= 30;
  const baseDelay = isComplex ? 2000 : 1000;
  const randDelay = isComplex ? Math.random() * 2000 : Math.random() * 1000;
  const totalDelay = baseDelay + randDelay;

  // Disable input & show typing
  setInputState(true);
  showTyping(totalDelay);

  try {
    const res = await fetch(`/api/chats/${currentChatId}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: text,
        language: localStorage.getItem('aria_language') || 'en',
        mode: ariaMode,
        is_voice: typeof isRecording !== 'undefined' ? isRecording : false
      }),
    });

    await new Promise(r => setTimeout(r, totalDelay));
    
    // Pause briefly to show the "✓ Response Ready" and Lightbulb
    await new Promise(r => setTimeout(r, 800));
    
    hideTyping();
    
    // Wait for the fade out transition before showing response
    await new Promise(r => setTimeout(r, 300));

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

    // Refresh chat list to update title if it was new
    loadChats();

  } catch (err) {
    hideTyping();
    const errEl = createBotMessage("I currently do not have information on that topic. Please ask something related to my supported knowledge areas.");
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

// Sidebar toggle (desktop) - Repurposed to Quick Access Menu
sidebarToggle?.addEventListener('click', (e) => {
  e.stopPropagation();
  const quickMenu = document.getElementById('quickAccessMenu');
  if (quickMenu) {
    quickMenu.classList.toggle('open');
  }
});

document.addEventListener('click', (e) => {
  const quickMenu = document.getElementById('quickAccessMenu');
  if (quickMenu && quickMenu.classList.contains('open') && !quickMenu.contains(e.target) && e.target !== sidebarToggle && (!sidebarToggle || !sidebarToggle.contains(e.target))) {
    quickMenu.classList.remove('open');
  }
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
const exportBtn = document.getElementById('exportBtn');
const exportMenu = document.getElementById('exportMenu');
const languageIndicatorBtn = document.getElementById('languageIndicatorBtn');
const languageHeaderMenu = document.getElementById('languageHeaderMenu');

exportBtn?.addEventListener('click', (e) => {
  e.stopPropagation();
  exportMenu.classList.toggle('open');
  settingsMenu?.classList.remove('open');
  languageHeaderMenu?.classList.remove('open');
});

languageIndicatorBtn?.addEventListener('click', (e) => {
  e.stopPropagation();
  languageHeaderMenu.classList.toggle('open');
  settingsMenu?.classList.remove('open');
  exportMenu?.classList.remove('open');
});

settingsBtn?.addEventListener('click', (e) => {
  e.stopPropagation();
  settingsMenu.classList.toggle('open');
  exportMenu?.classList.remove('open');
  languageHeaderMenu?.classList.remove('open');
});

document.addEventListener('click', (e) => {
  if (settingsMenu?.classList.contains('open') && !settingsMenu.contains(e.target) && e.target !== settingsBtn) {
    settingsMenu.classList.remove('open');
  }
  if (exportMenu?.classList.contains('open') && !exportMenu.contains(e.target) && e.target !== exportBtn) {
    exportMenu.classList.remove('open');
  }
  if (languageHeaderMenu?.classList.contains('open') && !languageHeaderMenu.contains(e.target) && e.target !== languageIndicatorBtn) {
    languageHeaderMenu.classList.remove('open');
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

// Language Switcher
const languageSelect = document.getElementById('languageSelect');
const headerLanguageText = document.getElementById('headerLanguageText');

const langNames = {
  en: 'English',
  ta: 'Tamil',
  hi: 'Hindi',
  te: 'Telugu',
  ml: 'Malayalam'
};

window.setLanguage = function(langCode) {
  localStorage.setItem('aria_language', langCode);
  if (headerLanguageText) {
    headerLanguageText.textContent = `Language: ${langNames[langCode] || 'English'}`;
  }
  if (languageSelect) {
    languageSelect.value = langCode;
  }
  languageHeaderMenu?.classList.remove('open');
}

languageSelect?.addEventListener('change', (e) => {
  setLanguage(e.target.value);
});

// Init language on load
const savedLang = localStorage.getItem('aria_language') || 'en';
setLanguage(savedLang);

// Privacy Mode Logic
function setPrivacyMode(enabled) {
  if (enabled) {
    messagesContainer.classList.add('privacy-mode');
    // Activate nav button
    if (privacyNavBtn) {
      privacyNavBtn.classList.add('active');
      const unlocked = privacyNavBtn.querySelector('.privacy-icon-unlocked');
      const locked   = privacyNavBtn.querySelector('.privacy-icon-locked');
      if (unlocked) unlocked.style.display = 'none';
      if (locked)   locked.style.display   = 'block';
    }
    // Show banner
    if (privateSessionBanner) privateSessionBanner.style.display = 'flex';
    // Toast notification
    if (privacyToast) {
      privacyToast.classList.add('show');
      setTimeout(() => privacyToast.classList.remove('show'), 3000);
    }
  } else {
    messagesContainer.classList.remove('privacy-mode');
    // Deactivate nav button
    if (privacyNavBtn) {
      privacyNavBtn.classList.remove('active');
      const unlocked = privacyNavBtn.querySelector('.privacy-icon-unlocked');
      const locked   = privacyNavBtn.querySelector('.privacy-icon-locked');
      if (unlocked) unlocked.style.display = 'block';
      if (locked)   locked.style.display   = 'none';
    }
    // Hide banner
    if (privateSessionBanner) privateSessionBanner.style.display = 'none';
    if (privacyToast) privacyToast.classList.remove('show');
  }
}

// Nav bar privacy button — one-click toggle
privacyNavBtn?.addEventListener('click', () => {
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

aboutDevBtn?.addEventListener('click', () => {
  closeModals(); // close settings
  const intro = document.getElementById('devIntroOverlay');
  if (intro) {
    intro.classList.add('show');
    // Start animation
    requestAnimationFrame(() => {
      intro.classList.add('animate');
    });
    // After 2 seconds, fade out overlay and open devModal
    setTimeout(() => {
      intro.classList.remove('show');
      intro.classList.remove('animate');
      
      openModal('devModal');
      // Add a slight delay to trigger the active class for float/glassmorphism
      const devM = document.getElementById('devModal');
      setTimeout(() => {
        if(devM) devM.classList.add('premium-active');
      }, 50);
    }, 2000);
  } else {
    openModal('devModal');
  }
});
aboutProjBtn?.addEventListener('click', () => openModal('projModal'));

const kmaSeriesBtn = document.getElementById('kmaSeriesBtn');
const v2Btn = document.getElementById('v2Btn');

kmaSeriesBtn?.addEventListener('click', () => openModal('kmaModal'));
v2Btn?.addEventListener('click', () => openModal('v2Modal'));

document.querySelectorAll('.modal-close, .preview-close-btn').forEach(btn => {
  btn.addEventListener('click', () => closeModals());
});

// Logo Preview Triggers
document.querySelectorAll('img[src*="kma2-logo.png"]').forEach(img => {
  if (img.id !== 'loadingLogo') {
    img.classList.add('clickable-logo');
    img.addEventListener('click', () => openModal('logoPreviewModal'));
  }
});


modalOverlay?.addEventListener('click', (e) => {
  if (e.target === modalOverlay) closeModals();
});

// ── Stats Dashboard Logic ─────────────────────────────────────
openStatsBtn?.addEventListener('click', async () => {
  openModal('statsModal');
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    if (dashChats) dashChats.textContent = data.chats || 0;
    if (dashMessages) dashMessages.textContent = data.messages || 0;
    if (dashPinned) dashPinned.textContent = data.pinned_messages || 0;
    if (dashDuration) dashDuration.textContent = data.duration || '0m 0s';
  } catch (err) {
    console.error("Error fetching stats:", err);
  }
});
closeStatsBtn?.addEventListener('click', () => closeModals());

// Legacy Mode Selector Removed

// ── Voice Input (Web Speech API) ──────────────────────────────
const micBtn = document.getElementById('micBtn');

(function initVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    // Browser doesn't support speech recognition
    if (micBtn) {
      micBtn.classList.add('not-supported');
      micBtn.title = 'Voice input not supported in this browser (use Chrome)';
      micBtn.disabled = true;
    }
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
  recognition.maxAlternatives = 1;

  let isRecording = false;
  let finalTranscript = '';

  function startRecording() {
    if (isWaitingResponse) return;
    isRecording = true;
    finalTranscript = '';

    micBtn.classList.add('recording');
    micBtn.title = 'Listening... (click to stop)';
    micBtn.querySelector('.mic-icon-default').style.display = 'none';
    micBtn.querySelector('.mic-icon-active').style.display = 'block';

    recognition.start();
  }

  function stopRecording() {
    isRecording = false;
    recognition.stop();

    micBtn.classList.remove('recording');
    micBtn.title = 'Voice Input';
    micBtn.querySelector('.mic-icon-default').style.display = 'block';
    micBtn.querySelector('.mic-icon-active').style.display = 'none';
  }

  micBtn?.addEventListener('click', () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  });

  recognition.addEventListener('result', (e) => {
    let interimTranscript = '';
    finalTranscript = '';

    for (let i = e.resultIndex; i < e.results.length; i++) {
      const transcript = e.results[i][0].transcript;
      if (e.results[i].isFinal) {
        finalTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }

    // Show interim text in input as the user speaks
    if (interimTranscript || finalTranscript) {
      messageInput.value = finalTranscript || interimTranscript;
      charCount.textContent = `${messageInput.value.length}/500`;
      sendBtn.disabled = messageInput.value.trim().length === 0;
      autoResizeTextarea();
    }
  });

  recognition.addEventListener('end', () => {
    if (isRecording) {
      // Auto-stop on silence
      stopRecording();
    }
    // Leave the final text in the input box so the user can edit before sending
    if (finalTranscript.trim()) {
      messageInput.value = finalTranscript.trim();
      charCount.textContent = `${messageInput.value.length}/500`;
      sendBtn.disabled = false;
      autoResizeTextarea();
      messageInput.focus();
    }
  });

  recognition.addEventListener('error', (e) => {
    stopRecording();
    let errorMsg = 'Voice input error.';
    if (e.error === 'not-allowed') {
      errorMsg = 'Microphone access denied. Please allow mic access in your browser.';
    } else if (e.error === 'no-speech') {
      errorMsg = 'No speech detected. Please try again.';
    } else if (e.error === 'network') {
      errorMsg = 'Network error with voice recognition. Please check your connection.';
    }
    // Show brief inline error
    const errEl = createBotMessage(`🎙️ ${errorMsg}`);
    messagesContainer.appendChild(errEl);
    scrollToBottom();
  });

})();

// ============================================================================
// MULTI-CHAT SYSTEM LOGIC
// ============================================================================

async function initMultiChat() {
  await loadChats();
  if (!currentChatId) {
    await createNewChat();
  }
}

async function loadChats() {
  try {
    const queryParam = currentSearchQuery ? `?q=${encodeURIComponent(currentSearchQuery)}` : '';
    const res = await fetch(`/api/chats${queryParam}`);
    const data = await res.json();
    
    chatList.innerHTML = '';
    
    if (data.chats.length === 0 && !currentSearchQuery) {
      currentChatId = null;
      return;
    }
    
    data.chats.forEach(chat => {
      const el = document.createElement('div');
      el.className = 'chat-item';
      if (chat.id === currentChatId) el.classList.add('active');
      
      el.innerHTML = `
        <div class="chat-item-header">
          <span class="chat-item-title">${escapeHtml(chat.title)}</span>
          <div style="display:flex; gap:4px;">
            <button class="chat-delete-btn" aria-label="Delete Chat" title="Delete Chat">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      `;
      
      el.addEventListener('click', async (e) => {
        if (e.target.closest('.chat-delete-btn')) {
          e.stopPropagation();
          deleteChat(chat.id);
        } else {
          switchChat(chat.id);
        }
      });
      
      chatList.appendChild(el);
    });
    
    if (!currentChatId && data.chats.length > 0 && !currentSearchQuery) {
      currentChatId = data.chats[0].id;
      loadChatHistory(currentChatId);
    }
  } catch (err) {
    console.error('Error loading chats:', err);
  }
}

// ── Search Logic ──────────────────────────────────────────────
let searchTimeout = null;
chatSearchInput?.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentSearchQuery = e.target.value;
    loadChats();
  }, 300); // 300ms debounce
});

async function createNewChat() {
  try {
    const res = await fetch('/api/chats', { method: 'POST' });
    const data = await res.json();
    currentChatId = data.id;
    messagesContainer.innerHTML = '';
    renderWelcomePanel();
    
    await loadChats();
  } catch (err) {
    console.error('Error creating chat:', err);
  }
}

async function switchChat(chatId) {
  if (currentChatId === chatId) return;
  currentChatId = chatId;
  
  // Update UI active state
  document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
  loadChats(); // re-render to set active
  
  await loadChatHistory(chatId);
  if (window.innerWidth <= 768) {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
  }
}

window.currentPinnedTexts = new Map();
async function fetchCurrentPinnedTexts(chatId) {
  try {
    const res = await fetch(`/api/messages/pinned?chat_id=${chatId}`);
    const data = await res.json();
    window.currentPinnedTexts.clear();
    (data.pinned_messages || []).forEach(msg => {
      window.currentPinnedTexts.set(msg.text, msg.id);
    });
  } catch (err) {
    console.error(err);
  }
}

async function loadChatHistory(chatId) {
  try {
    const res = await fetch(`/api/chats/${chatId}/history`);
    const data = await res.json();
    
    await fetchCurrentPinnedTexts(chatId);
    
    messagesContainer.innerHTML = '';
    if (data.history.length === 0) {
      renderWelcomePanel();
    } else {
      data.history.forEach(msg => {
        const role = msg.role || msg.sender;
        const content = msg.content || msg.text;
        const el = role === 'user' ? createUserMessage(content) : createBotMessage(content, false, true);
        messagesContainer.appendChild(el);
      });
    }
    scrollToBottom();
  } catch (err) {
    console.error('Error loading history:', err);
  }
}

async function deleteChat(chatId) {
  if (!confirm("Are you sure you want to delete this chat? You can recover it from the settings menu.")) return;
  try {
    await fetch(`/api/chats/${chatId}`, { method: 'DELETE' });
    if (currentChatId === chatId) {
      currentChatId = null;
      messagesContainer.innerHTML = '';
      await loadChats();
      if (!currentChatId) {
        await createNewChat();
      }
    } else {
      await loadChats();
    }
  } catch (err) {
    console.error('Error deleting chat:', err);
  }
}

if (newChatBtn) {
  newChatBtn.addEventListener('click', createNewChat);
}

// Recently Deleted Modal Logic
if (recentlyDeletedBtn) {
  recentlyDeletedBtn.addEventListener('click', () => {
    settingsMenu.classList.remove('open');
    loadDeletedChats();
    document.getElementById('deletedChatsModal').classList.add('active');
    modalOverlay.classList.add('show');
  });
}

async function loadDeletedChats() {
  try {
    const res = await fetch('/api/chats/deleted');
    const data = await res.json();
    
    deletedChatsContainer.innerHTML = '';
    const clearAllBtn = document.getElementById('clearAllDeletedBtn');
    
    if (data.deleted_chats.length === 0) {
      deletedChatsContainer.innerHTML = '<p class="no-deleted-chats">No recently deleted chats found.</p>';
      if (clearAllBtn) clearAllBtn.style.display = 'none';
      return;
    }
    
    if (clearAllBtn) clearAllBtn.style.display = 'block';
    
    data.deleted_chats.forEach(chat => {
      const el = document.createElement('div');
      el.className = 'deleted-chat-item';
      
      const date = new Date(chat.deleted_at).toLocaleString();
      
      el.innerHTML = `
        <div class="deleted-chat-info">
          <span class="deleted-chat-title">${escapeHtml(chat.title)}</span>
          <span class="deleted-chat-time">Deleted: ${date}</span>
        </div>
        <div class="deleted-chat-actions">
          <button class="recover-btn" onclick="recoverChat('${chat.id}')">Recover</button>
          <button class="perm-delete-btn" onclick="permanentDeleteChat('${chat.id}')">Delete</button>
        </div>
      `;
      deletedChatsContainer.appendChild(el);
    });
  } catch (err) {
    console.error('Error loading deleted chats:', err);
  }
}

window.recoverChat = async function(chatId) {
  try {
    await fetch(`/api/chats/${chatId}/recover`, { method: 'POST' });
    await loadDeletedChats();
    await loadChats();
    switchChat(chatId);
    document.getElementById('deletedChatsModal').classList.remove('show');
    modalOverlay.classList.remove('show');
  } catch (err) {
    console.error('Error recovering chat:', err);
  }
}

window.permanentDeleteChat = async function(chatId) {
  if (!confirm("Are you sure? This cannot be undone.")) return;
  try {
    await fetch(`/api/chats/${chatId}/permanent`, { method: 'DELETE' });
    await loadDeletedChats();
  } catch (err) {
    console.error('Error permanently deleting chat:', err);
  }
}

// Clear All Logic
const clearAllDeletedBtn = document.getElementById('clearAllDeletedBtn');
const clearAllConfirmModal = document.getElementById('clearAllConfirmModal');
const confirmClearAllBtn = document.getElementById('confirmClearAllBtn');

if (clearAllDeletedBtn) {
  clearAllDeletedBtn.addEventListener('click', () => {
    // Open confirm modal on top
    modalOverlay.classList.add('show');
    clearAllConfirmModal.classList.add('active');
  });
}

if (confirmClearAllBtn) {
  confirmClearAllBtn.addEventListener('click', async () => {
    try {
      await fetch('/api/chats/deleted/all', { method: 'DELETE' });
      clearAllConfirmModal.classList.remove('active');
      await loadDeletedChats();
    } catch (err) {
      console.error('Error clearing all deleted chats:', err);
    }
  });
}

// Export Chat Logic
window.exportChat = async function(format) {
  exportMenu?.classList.remove('open');
  if (!currentChatId) {
    alert("No conversation available to export.");
    return;
  }
  try {
    const res = await fetch(`/api/chats/${currentChatId}/export/${format}`);
    if (!res.ok) {
      if (res.status === 404) {
        alert("No conversation available to export.");
      } else {
        alert("Export failed.");
      }
      return;
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ARIA_Export.${format}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (err) {
    console.error('Export error:', err);
    alert("Failed to export. Please check your connection.");
  }
}

// ── Welcome Panel Logic ─────────────────────────────────────────
window.renderWelcomePanel = function() {
  if (messagesContainer.querySelector('.welcome-panel')) return;
  
  const html = `
    <div class="welcome-panel">
      <div class="welcome-header">
        <h2>Welcome to ARIA</h2>
        <p class="welcome-subtitle">Your Intelligent AI Assistant powered by the KMA² Intelligence Framework.</p>
      </div>
      
      <div class="welcome-intro">
        <p>Hello, I am ARIA.</p>
        <p>I am designed to help you learn, explore ideas, solve problems, and access knowledge across multiple domains.</p>
        <p>Whether you are interested in Artificial Intelligence, Programming, Machine Learning, Study Guidance, Motivation, Technology, or General Knowledge, I am ready to assist you.</p>
      </div>

      <div class="welcome-features">
        <div class="feature-card">✓ Artificial Intelligence</div>
        <div class="feature-card">✓ Python & Programming</div>
        <div class="feature-card">✓ Machine Learning</div>
        <div class="feature-card">✓ Study Tips</div>
        <div class="feature-card">✓ Motivation</div>
        <div class="feature-card">✓ General Knowledge</div>
        <div class="feature-card">✓ Multi-Language Support</div>
        <div class="feature-card">✓ PDF Export</div>
      </div>

      <div class="welcome-quickstart">
        <p><strong>Try asking:</strong></p>
        <div class="quickstart-buttons">
          <button onclick="handleQuickStart('What is Artificial Intelligence?')">• What is Artificial Intelligence?</button>
          <button onclick="handleQuickStart('Explain Python Basics')">• Explain Python Basics</button>
          <button onclick="handleQuickStart('Give me Study Tips')">• Give me Study Tips</button>
          <button onclick="handleQuickStart('Motivate Me')">• Motivate Me</button>
          <button onclick="handleQuickStart('Tell me about DecodeLabs')">• Tell me about DecodeLabs</button>
        </div>
      </div>

      <div class="welcome-footer">
        <p>Powered by KMA² Signature Series</p>
        <p>Running on the KMA² Intelligence Framework</p>
      </div>
    </div>
  `;
  messagesContainer.innerHTML = html;
}

window.handleQuickStart = function(text) {
  messageInput.value = text;
  autoResizeTextarea();
  sendMessage();
}

// ── Search & Pinned Modals Logic ───────────────────────────────
const searchModal = document.getElementById('searchModal');
const pinnedMessagesModal = document.getElementById('pinnedMessagesModal');
const settingsSearchBtn = document.getElementById('settingsSearchBtn');
const settingsPinnedBtn = document.getElementById('settingsPinnedBtn');
const searchResultsList = document.getElementById('searchResultsList');
const pinnedMessagesList = document.getElementById('pinnedMessagesList');
const modalChatSearchInput = document.getElementById('chatSearchInput');

settingsSearchBtn?.addEventListener('click', () => {
  closeModals();
  modalOverlay.classList.add('show');
  searchModal.classList.add('active');
  modalChatSearchInput?.focus();
});

modalChatSearchInput?.addEventListener('input', async (e) => {
  currentSearchQuery = e.target.value.trim();
  if (!currentSearchQuery) {
    searchResultsList.innerHTML = '<p style="color:var(--text-muted); font-size:0.85rem;">Type to search your previous conversations...</p>';
    await loadChats(); // refresh sidebar to show all
    return;
  }
  
  try {
    const res = await fetch(`/api/chats?q=${encodeURIComponent(currentSearchQuery)}`);
    const data = await res.json();
    
    searchResultsList.innerHTML = '';
    if (data.chats.length === 0) {
      searchResultsList.innerHTML = '<p style="color:var(--text-muted); font-size:0.85rem;">No matching chats found.</p>';
    } else {
      data.chats.forEach(chat => {
        const btn = document.createElement('button');
        btn.className = 'quick-btn';
        btn.textContent = chat.title;
        btn.onclick = () => {
          switchChat(chat.id);
          closeModals();
          currentSearchQuery = '';
          modalChatSearchInput.value = '';
        };
        searchResultsList.appendChild(btn);
      });
    }
    // Also filter the sidebar live
    await loadChats();
  } catch (err) {
    console.error('Search error:', err);
  }
});

settingsPinnedBtn?.addEventListener('click', async () => {
  closeModals();
  modalOverlay.classList.add('show');
  pinnedMessagesModal.classList.add('active');
  await loadPinnedMessages();
});

async function loadPinnedMessages() {
  try {
    const res = await fetch(`/api/messages/pinned?chat_id=${currentChatId}`);
    const data = await res.json();
    pinnedMessagesList.innerHTML = '';
    
    if (data.pinned_messages.length === 0) {
      pinnedMessagesList.innerHTML = '<p style="color:var(--text-muted); font-size:0.85rem;">No pinned messages yet.</p>';
      return;
    }
    
    data.pinned_messages.forEach(msg => {
      const el = document.createElement('div');
      el.className = 'pinned-msg-item';
      el.style.cssText = 'background: var(--bg-surface); padding: 12px; border-radius: 8px; border: 1px solid var(--border-color);';
      
      const date = new Date(msg.pinned_at).toLocaleString();
      
      el.innerHTML = `
        <div style="font-size: 0.85rem; color: var(--text-primary); margin-bottom: 8px;">${formatBotText(msg.text)}</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.7rem; color: var(--text-muted);">${date}</span>
          <button class="action-btn text-danger" onclick="unpinMessage('${msg.id}')" style="padding: 4px 8px; font-size: 0.75rem;">Unpin</button>
        </div>
      `;
      pinnedMessagesList.appendChild(el);
    });
  } catch (err) {
    console.error('Error loading pinned messages', err);
  }
}

window.togglePin = async function(btnEl) {
  const messageEl = btnEl.closest('.bot-message');
  if (!messageEl) return;
  const text = messageEl.getAttribute('data-raw-text') || messageEl.querySelector('.message-text').innerText;
  
  btnEl.disabled = true;
  
  try {
    if (window.currentPinnedTexts && window.currentPinnedTexts.has(text)) {
      // Unpin
      const msgId = window.currentPinnedTexts.get(text);
      if (msgId) {
        const res = await fetch(`/api/messages/unpin/${msgId}`, { method: 'DELETE' });
        if (res.ok) {
          window.currentPinnedTexts.delete(text);
          btnEl.textContent = '📍 Unpinned';
          btnEl.style.color = '';
          btnEl.style.borderColor = '';
          btnEl.classList.remove('is-pinned');
        }
      }
    } else {
      // Pin
      const res = await fetch('/api/messages/pin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, chat_id: currentChatId })
      });
      if (res.ok) {
        const data = await res.json();
        if (window.currentPinnedTexts) window.currentPinnedTexts.set(text, data.id);
        btnEl.textContent = '📌 Pinned';
        btnEl.style.color = '#4CAF50';
        btnEl.style.borderColor = '#4CAF50';
        btnEl.classList.add('is-pinned');
      } else {
        throw new Error('Failed to pin');
      }
    }
  } catch (err) {
    console.error(err);
  } finally {
    btnEl.disabled = false;
    loadPinnedMessages();
  }
}

window.unpinMessage = async function(msgId) {
  try {
    await fetch(`/api/messages/unpin/${msgId}`, { method: 'DELETE' });
    await loadPinnedMessages();
    await loadChatHistory(currentChatId);
  } catch (err) {
    console.error('Error unpinning message', err);
  }
}

// ── Mode Selector (+) Logic ────────────────────────────────────
const modePlusBtn = document.getElementById('modePlusBtn');
const modePlusMenu = document.getElementById('modePlusMenu');

modePlusBtn?.addEventListener('click', (e) => {
  e.stopPropagation();
  modePlusMenu.classList.toggle('open');
});

document.addEventListener('click', (e) => {
  if (responseModeMenu?.classList.contains('open') && !responseModeBtn.contains(e.target) && !responseModeMenu.contains(e.target)) {
    responseModeMenu.classList.remove('open');
  }
  if (typeof modePlusMenu !== 'undefined' && modePlusMenu?.classList.contains('open') && !modePlusBtn.contains(e.target) && !modePlusMenu.contains(e.target)) {
    modePlusMenu.classList.remove('open');
  }
});

// Quick Access Menu Modal Population Functions
window.showCurrentSession = function() {
  const lang = localStorage.getItem('aria_language') || 'en';
  const currentMode = (typeof ariaMode !== 'undefined') ? ariaMode : 'normal';
  
  const langNames = { en: 'English', ta: 'Tamil', hi: 'Hindi', te: 'Telugu', ml: 'Malayalam' };
  const modeNames = {
    'normal': 'STANDARD MODE',
    'fast': 'FAST MODE',
    'deep_thinking': 'DEEP THINKING MODE',
    'detailed': 'DETAILED EXPLANATION MODE',
    'interview': 'INTERVIEW MODE'
  };

  const messageCount = document.querySelectorAll('.user-message').length;
  if (!window.sessionStartTime) window.sessionStartTime = new Date().toLocaleTimeString();
  
  document.getElementById('qaModalTitle').innerHTML = '🕒 Current Session';
  document.getElementById('qaModalBody').innerHTML = `
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li style="margin-bottom: 12px;"><strong>Session Start:</strong> ${window.sessionStartTime}</li>
      <li style="margin-bottom: 12px;"><strong>Current Language:</strong> ${langNames[lang] ? langNames[lang].toUpperCase() : lang.toUpperCase()}</li>
      <li style="margin-bottom: 12px;"><strong>Current Mode:</strong> ${modeNames[currentMode] || 'STANDARD MODE'}</li>
      <li><strong>Total Chats:</strong> ${messageCount}</li>
    </ul>
  `;
  openModal('quickAccessInfoModal');
};

window.showActiveLanguage = function() {
  const lang = localStorage.getItem('aria_language') || 'en';
  const langNames = { en: 'English', ta: 'Tamil', hi: 'Hindi', te: 'Telugu', ml: 'Malayalam' };
  const langDesc = {
    en: "English is one of the most widely used international languages for technology, education, communication, and professional development.",
    ta: "Tamil is one of the world's oldest living classical languages with a rich literary and cultural heritage.",
    te: "Telugu is a major South Indian language known for its expressive vocabulary and cultural significance.",
    hi: "Hindi is one of India's most widely spoken languages and serves as an important medium of communication.",
    ml: "Malayalam is a classical language from Kerala known for its unique script and rich literary tradition."
  };
  
  document.getElementById('qaModalTitle').innerHTML = '🌐 Active Language';
  document.getElementById('qaModalBody').innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <div style="font-size: 2rem; margin-bottom: 10px;">${lang.toUpperCase()} - ${langNames[lang] || 'Unknown'}</div>
      <div style="color: var(--text-silver); font-size: 0.9rem; margin-top: 15px; text-align: left; background: var(--bg-surface); padding: 12px; border-radius: 8px;">${langDesc[lang] || ''}</div>
    </div>
  `;
  openModal('quickAccessInfoModal');
};

window.showActiveMode = function() {
  const modeNames = {
    'normal': 'STANDARD MODE',
    'fast': 'FAST MODE',
    'deep_thinking': 'DEEP THINKING MODE',
    'detailed': 'DETAILED EXPLANATION MODE',
    'interview': 'INTERVIEW MODE'
  };
  const modeDesc = {
    'normal': 'Balanced responses optimized for everyday learning and conversation.',
    'fast': 'Provides short and quick responses for rapid interaction.',
    'deep_thinking': 'Generates analytical responses with deeper reasoning and expanded insights.',
    'detailed': 'Provides comprehensive explanations with examples and structured breakdowns.',
    'interview': 'Simulates interview-style responses with focused, professional guidance.'
  };
  
  const currentMode = (typeof ariaMode !== 'undefined') ? ariaMode : 'normal';
  const displayMode = modeNames[currentMode] || 'STANDARD MODE';
  const displayDesc = modeDesc[currentMode] || modeDesc['normal'];
  
  document.getElementById('qaModalTitle').innerHTML = '🧠 Active Mode';
  document.getElementById('qaModalBody').innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <div style="font-size: 1.5rem; margin-bottom: 10px; color: var(--accent-gold);">${displayMode}</div>
      <div style="color: var(--text-silver); font-size: 0.9rem; margin-top: 15px; text-align: left; background: var(--bg-surface); padding: 12px; border-radius: 8px;">${displayDesc}</div>
    </div>
  `;
  openModal('quickAccessInfoModal');
};

window.showSystemHealth = function() {
  document.getElementById('qaModalTitle').innerHTML = '⚕️ System Health';
  document.getElementById('qaModalBody').innerHTML = `
    <ul style="list-style: none; padding: 0; margin: 0; background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
      <li style="margin-bottom: 12px; display: flex; justify-content: space-between;"><span>Online Status:</span> <span style="color: #4CAF50; font-weight: bold;">🟢 Optimal</span></li>
      <li style="margin-bottom: 12px; display: flex; justify-content: space-between;"><span>Memory Status:</span> <span style="color: #4CAF50; font-weight: bold;">🟢 Stable</span></li>
      <li style="margin-bottom: 12px; display: flex; justify-content: space-between;"><span>Export Status:</span> <span style="color: #4CAF50; font-weight: bold;">🟢 Ready</span></li>
      <li style="display: flex; justify-content: space-between;"><span>Language Engine:</span> <span style="color: #4CAF50; font-weight: bold;">🟢 Synchronized</span></li>
    </ul>
  `;
  openModal('quickAccessInfoModal');
};

// We override the old setResponseMode
window.setResponseMode = function(mode) {
  ariaMode = mode;
  localStorage.setItem('aria_mode', mode);
  
  // Update button UI if needed
  if (modePlusBtn) {
    modePlusBtn.style.color = mode === 'normal' ? 'var(--text-primary)' : 'var(--accent-gold)';
    modePlusBtn.style.borderColor = mode === 'normal' ? 'var(--border-color)' : 'var(--accent-gold)';
  }
  
  if (modePlusMenu) modePlusMenu.classList.remove('open');
  
  // Update mode display
  const modeDisplay = document.getElementById('activeModeDisplay');
  if (modeDisplay) {
    const modes = {
      'normal': '⚖️ Standard Mode',
      'fast': '⚡ Fast Mode',
      'deep_thinking': '🧠 Deep Thinking Mode',
      'detailed': '📚 Detailed Explanation Mode',
      'interview': '🎯 Interview Mode'
    };
    modeDisplay.textContent = '[' + (modes[mode] || '⚖️ Standard Mode') + ']';
    modeDisplay.style.color = mode === 'normal' ? 'var(--text-silver)' : '#ffd700';
  }
  
  // Show a small toast to confirm mode
  showToast(`Switched to ${mode.replace('_', ' ').toUpperCase()} MODE`);
}

function showToast(msg) {
  let toast = document.getElementById('ariaToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'ariaToast';
    toast.style.cssText = 'position:fixed; bottom:24px; left:50%; transform:translateX(-50%); background:var(--bg-surface); color:var(--text-primary); padding:10px 20px; border-radius:24px; border:1px solid var(--border-color); font-size:0.85rem; font-weight:600; z-index:1000; opacity:0; transition:opacity 0.3s ease; box-shadow:0 4px 12px rgba(0,0,0,0.2);';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  setTimeout(() => toast.style.opacity = '0', 2500);
}

// Init mode on load
setResponseMode(ariaMode);


