# 🤖 ARIA — Artificial Rule-based Intelligent Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![DecodeLabs](https://img.shields.io/badge/DecodeLabs-Project%201-purple?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-60%2B%20cases-brightgreen?style=for-the-badge)

**A professional Rule-Based AI Chatbot — DecodeLabs AI Engineering Project 1, Batch 2026**

*"Before you build systems that learn on their own, you must master the art of teaching a machine through explicit if-else instructions."*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [CLI Mode](#-cli-mode)
- [Web Interface](#-web-interface)
- [Running Tests](#-running-tests)
- [How It Works](#-how-it-works)
- [Response Categories](#-response-categories)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Learning Outcomes](#-learning-outcomes)
- [About DecodeLabs](#-about-decodelabs)

---

## 🌟 Overview

**ARIA** (Artificial Rule-based Intelligent Assistant) is a **professional-grade rule-based AI chatbot** built for the DecodeLabs AI Engineering Industrial Training Program. It demonstrates how intelligent conversation can be engineered using **pure control flow and decision-making logic** — the foundation of all AI systems.

### What Makes This Special

| Feature | Description |
|---------|-------------|
| 🧠 **17 Distinct Rules** | Carefully crafted if-else decision tree |
| 🎨 **Dual Interface** | Beautiful CLI + Modern Web UI |
| 📊 **Session Analytics** | Conversation logging & statistics |
| 🧪 **60+ Unit Tests** | Full coverage of all response categories |
| 🌐 **REST API** | Flask-powered JSON API |
| ⚡ **Zero ML Dependencies** | Pure Python stdlib for core logic |

---

## ✨ Features

### Conversation Capabilities
- 👋 **Greetings & Farewells** — Intelligent welcome and exit handling
- 🧑 **Name Recognition** — Detects and remembers user's name
- 🤖 **AI Knowledge Base** — Explains AI, ML, Deep Learning, NLP
- 🐍 **Python Tips** — Shares Python programming knowledge
- 😄 **Jokes** — 8+ tech humor responses
- 💪 **Motivation** — 7+ inspirational quotes
- 🧮 **Math Calculator** — Handles +, -, *, / operations
- 🕐 **Time & Date** — Real-time clock and calendar queries
- 🌤 **Weather** — Smart redirect to weather APIs
- 🆘 **Help Menu** — Full capabilities overview
- 📜 **History** — View conversation log

### Technical Features
- ✅ Continuous conversation loop
- ✅ Input normalization (case, punctuation, whitespace)
- ✅ Pattern matching with trigger word lists
- ✅ Random response selection for variety
- ✅ Session logging (JSON + plain text)
- ✅ ANSI color terminal UI
- ✅ Typing animation (web UI)
- ✅ Mobile responsive design
- ✅ REST API with health endpoint

---

## 📁 Project Structure

```
AI-Chatbot-Project/
│
├── 📄 main.py                    # CLI chatbot entry point
├── 📄 app.py                     # Flask web server
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This file
│
├── 📂 src/                       # Core source code
│   ├── 📄 __init__.py
│   ├── 📄 brain.py               # ⭐ Rule-based AI engine (main logic)
│   └── 📄 logger.py              # Conversation logger & analytics
│
├── 📂 web/                       # Web interface
│   ├── 📂 templates/
│   │   └── 📄 index.html         # Chat UI template
│   └── 📂 static/
│       ├── 📂 css/
│       │   └── 📄 style.css      # Dark glassmorphism design
│       └── 📂 js/
│           └── 📄 chat.js        # Frontend interaction logic
│
├── 📂 tests/                     # Unit tests
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py
│   └── 📄 test_brain.py          # 60+ test cases
│
├── 📂 docs/                      # Documentation
│   └── 📄 ARCHITECTURE.md        # System design document
│
└── 📂 logs/                      # Auto-created session logs
    └── session_*.json            # (Generated at runtime)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** — [Download here](https://python.org/downloads)
- **pip** — comes with Python

### Installation

```bash
# 1. Navigate to the project folder
cd "AI-Chatbot-Project"

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 💻 CLI Mode

The simplest way to run ARIA — no browser needed!

```bash
# Basic run
python main.py

# With session logging (saves chat to logs/ folder)
python main.py --save

# Without ANSI colors (if your terminal doesn't support them)
python main.py --no-color
```

### CLI Usage

```
[HH:MM] You › hello
[HH:MM] 🤖 ARIA ›
──────────────────────────────────────
  Hello there! 👋 I'm ARIA (Artificial Rule-based Intelligent
  Assistant). How can I help you today?
──────────────────────────────────────

[HH:MM] You › what is AI?
[HH:MM] You › tell me a joke
[HH:MM] You › bye
```

**Special CLI Commands:**
| Command | Action |
|---------|--------|
| `help`    | Show help menu |
| `history` | View conversation history |
| `stats`   | Show session statistics |
| `clear`   | Clear screen |
| `bye`     | Exit chatbot |

---

## 🌐 Web Interface

A beautiful dark-themed web chatbot with real-time interactions.

```bash
# Start the Flask web server
python app.py
```

Then open your browser at: **http://localhost:5000**

### Web Features
- 💬 Real-time chat with typing animation
- 📱 Fully mobile responsive
- ⚡ Quick-topic shortcuts in sidebar
- 📊 Live session statistics
- 🔄 Session reset button
- 🎨 Dark glassmorphism design

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run a specific test class
python -m pytest tests/test_brain.py::TestGreetings -v

# Run tests matching a keyword
python -m pytest tests/ -v -k "farewell or greeting"
```

### Test Coverage

| Test Class | Cases | Description |
|------------|-------|-------------|
| `TestKnowledgeBase` | 7 | KB data validation |
| `TestGreetings` | 10 | Greeting detection |
| `TestFarewells` | 10 | Farewell/exit detection |
| `TestSmallTalk` | 5 | How-are-you patterns |
| `TestIdentity` | 5 | Bot self-identification |
| `TestHelp` | 5 | Help menu |
| `TestTimeDate` | 2 | Time/date queries |
| `TestMath` | 5 | Calculator logic |
| `TestAIKnowledge` | 5 | AI topic detection |
| `TestJokes` | 5 | Joke detection |
| `TestMotivation` | 3 | Motivation quotes |
| `TestThanks` | 4 | Gratitude detection |
| `TestUsernameDetection` | 3 | Name learning |
| `TestUnknownInput` | 5 | Edge cases |
| `TestConversationHistory` | 3 | Logging |
| `TestStats` | 3 | Statistics |
| `TestNormalization` | 4 | Input preprocessing |

---

## ⚙️ How It Works

### Core Architecture

ARIA uses a **linear rule evaluation pipeline**:

```
User Input
    │
    ▼
┌─────────────────────┐
│  Input Normalizer   │  → lowercase, strip punctuation & whitespace
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│   Rule Engine       │  17 if-else rules, evaluated in priority order
│   (brain.py)        │
│   ─────────────     │
│   Rule 0: Empty     │
│   Rule 1: Name      │
│   Rule 2: Farewell  │  ← Exit triggers checked EARLY (safety)
│   Rule 3: Greeting  │
│   Rule 4: How-r-u   │
│   Rule 5: Identity  │
│   Rule 6: Help      │
│   Rule 7: History   │
│   Rule 8: Time      │
│   Rule 9: Date      │
│   Rule 10: Math     │
│   Rule 11: AI Info  │
│   Rule 12: Python   │
│   Rule 13: Weather  │
│   Rule 14: Jokes    │
│   Rule 15: Motivate │
│   Rule 16: Thanks   │
│   Rule 17: Default  │  ← Unknown fallback
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Response Selector  │  → Random selection from matching pool
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Response + Category│  → Return tuple (text, category)
└─────────────────────┘
    │
    ▼
Display (CLI or Web)
```

### Input Normalization

```python
def _normalize(text: str) -> str:
    text = text.lower().strip()          # Lowercase
    text = re.sub(r"[^\w\s]", " ", text) # Remove punctuation
    text = re.sub(r"\s+", " ", text)     # Collapse whitespace
    return text
```

This ensures "Hello!!!" → "hello", "BYE!" → "bye", etc.

---

## 📊 Response Categories

| Category | Trigger Words | Example |
|----------|--------------|---------|
| `greeting` | hello, hi, hey, howdy... | "Hello! I'm ARIA..." |
| `farewell` | bye, exit, quit, goodbye... | "Goodbye! See you later!" |
| `smalltalk` | how are you, how do you do... | "Running at peak performance!" |
| `identity` | who are you, your name... | "I'm ARIA!" |
| `help` | help, commands, menu... | Full help menu |
| `time` | what time is it... | Current time |
| `date` | today's date, what day... | Current date |
| `math` | calculate, what is X+Y... | "5 + 3 = 8" |
| `ai_knowledge` | what is ai, machine learning... | AI explanation |
| `python` | python, python programming... | Python tips |
| `joke` | tell me a joke, funny... | Tech joke |
| `motivation` | motivate me, inspire... | Quote |
| `thanks` | thank you, thanks... | "My pleasure!" |
| `personal` | my name is X... | Name recognition |
| `weather` | weather, temperature... | Weather redirect |
| `unknown` | (unmatched input) | Help redirect |

---

## 🌐 API Reference

### POST `/api/chat`

Send a message to ARIA.

**Request:**
```json
{ "message": "hello" }
```

**Response:**
```json
{
  "response": "Hello there! 👋 I'm ARIA...",
  "category": "greeting",
  "timestamp": "14:32",
  "is_farewell": false,
  "user_name": null
}
```

### GET `/api/stats`

Get session statistics.

**Response:**
```json
{
  "messages": 5,
  "duration": "3m 24s",
  "user_name": "Alice",
  "session_start": "14:30:00"
}
```

### POST `/api/reset`

Reset the current session.

### GET `/api/health`

Health check endpoint.

---

## 🎓 Learning Outcomes

By completing this project, you have demonstrated:

1. **Control Flow Mastery** — Multi-level if-else decision trees
2. **String Processing** — Regex, normalization, pattern matching
3. **Object-Oriented Design** — Clean class architecture
4. **API Development** — RESTful Flask endpoints
5. **Frontend Development** — HTML/CSS/JavaScript
6. **Test-Driven Thinking** — 60+ unit test cases
7. **Project Organization** — Professional folder structure
8. **Documentation** — README, docstrings, inline comments

---

## 🏢 About DecodeLabs

DecodeLabs is an industrial training company focused on real-world tech skills.

- 🌐 **Website:** [www.decodelabs.tech](http://www.decodelabs.tech)
- 📍 **Location:** Greater Lucknow, India
- 📞 **Phone:** +91 89330 06408
- ✉ **Email:** decodelabs.tech@gmail.com

---

## 📄 License

This project is part of the DecodeLabs AI Engineering Industrial Training Program, Batch 2026.

---

<div align="center">

Made with ❤️ by the **DecodeLabs AI Engineering Team**

*Project 1 of the AI Engineering Track — Batch 2026*

</div>
