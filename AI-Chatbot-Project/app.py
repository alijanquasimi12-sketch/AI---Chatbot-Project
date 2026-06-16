"""
app.py - ARIA Web Interface (Flask Backend)
============================================
A beautiful web-based frontend for the ARIA chatbot.
Exposes a REST API consumed by the HTML/JS frontend.

Routes:
    GET  /              → Serves the chat UI
    POST /api/chat      → Receives user message, returns ARIA response
    GET  /api/stats     → Returns session statistics
    POST /api/reset     → Resets the session

Usage:
    python app.py
    Then open: http://localhost:5000

Author: DecodeLabs AI Engineering Team
Project: AI Chatbot Project 1 - Rule-Based AI
"""

import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.brain import ChatBot

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "web", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "web", "static"),
)
app.secret_key = "aria-decodelabs-2026-secret-key"
CORS(app)

# Global chatbot instance (per process; production would use sessions)
_bot_instances: dict[str, ChatBot] = {}


def get_bot() -> ChatBot:
    """Get or create a chatbot instance for the current session."""
    sid = session.get("session_id")
    if not sid:
        sid = f"web_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        session["session_id"] = sid
    if sid not in _bot_instances:
        _bot_instances[sid] = ChatBot(name="ARIA")
    return _bot_instances[sid]


# ==============================================================================
# ROUTES
# ==============================================================================

@app.route("/")
def index():
    """Serve the main chat interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    POST /api/chat
    Body: {"message": "user input text"}
    Returns: {"response": "...", "category": "...", "timestamp": "..."}
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    bot = get_bot()
    response, category = bot.get_response(user_message)

    return jsonify({
        "response": response,
        "category": category,
        "timestamp": datetime.now().strftime("%H:%M"),
        "is_farewell": category == "farewell",
        "user_name": bot.user_name,
    })


@app.route("/api/stats", methods=["GET"])
def stats():
    """GET /api/stats — Return current session statistics."""
    bot = get_bot()
    return jsonify(bot.get_stats())


@app.route("/api/reset", methods=["POST"])
def reset():
    """POST /api/reset — Reset the chatbot session."""
    sid = session.get("session_id")
    if sid and sid in _bot_instances:
        del _bot_instances[sid]
    session.pop("session_id", None)
    return jsonify({"status": "reset", "message": "Session reset successfully!"})


@app.route("/api/health", methods=["GET"])
def health():
    """GET /api/health — Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "ARIA Chatbot API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    })


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("\n[ARIA] Web Server Starting...")
    print("[URL]  http://localhost:5000")
    print("[STOP] Press Ctrl+C to stop\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
