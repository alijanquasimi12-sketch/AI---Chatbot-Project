import os
import io
import sys
import uuid
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
from fpdf import FPDF

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

# Global in-memory storage for user sessions and their multiple chats
# Structure: { session_id: { "chats": { chat_id: {"bot": ChatBot, "title": str, "deleted": bool, "deleted_at": str} } } }
_user_sessions = {}

def get_session_data():
    """Get or create the multi-chat session data for the current user."""
    sid = session.get("session_id")
    if not sid:
        sid = f"web_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        session["session_id"] = sid
    if sid not in _user_sessions:
        _user_sessions[sid] = {
            "chats": {},
            "global_stats": {
                "pdf_exports": 0,
                "txt_exports": 0,
                "voice_queries": 0,
                "languages_used": {"en"},
                "session_start": datetime.now()
            },
            "pinned_messages": []
        }
    return _user_sessions[sid]

def generate_chat_title(user_message):
    """Generate a brief chat title from the first message."""
    words = user_message.split()
    if len(words) > 5:
        return " ".join(words[:5]) + "..."
    return user_message

# ==============================================================================
# ROUTES - VIEWS
# ==============================================================================

@app.route("/")
def index():
    """Serve the main chat interface."""
    _user_sessions.clear()
    return render_template("index.html")

# ==============================================================================
# ROUTES - MULTI CHAT API
# ==============================================================================

@app.route("/api/chats", methods=["GET"])
def get_chats():
    """List all active chats for the current user."""
    session_data = get_session_data()
    search_query = request.args.get("q", "").strip().lower()
    active_chats = []
    
    for cid, chat in session_data["chats"].items():
        if not chat.get("deleted"):
            bot = chat["bot"]
            
            # If search query provided, filter
            if search_query:
                title_match = search_query in chat["title"].lower()
                history_match = any(search_query in msg.get("content", msg.get("text", "")).lower() 
                                    for msg in bot.conversation_history)
                if not (title_match or history_match):
                    continue

            active_chats.append({
                "id": cid,
                "title": chat["title"],
                "created_at": chat.get("created_at"),
                "pinned": chat.get("pinned", False)
            })
    # Sort newest first, then we can group by pinned in the frontend
    active_chats.sort(key=lambda x: x["created_at"], reverse=True)
    return jsonify({"chats": active_chats})

@app.route("/api/chats", methods=["POST"])
def create_chat():
    """Create a new chat instance."""
    session_data = get_session_data()
    chat_id = str(uuid.uuid4())
    session_data["chats"][chat_id] = {
        "bot": ChatBot(name="ARIA"),
        "title": "New Chat",
        "created_at": datetime.now().isoformat(),
        "deleted": False,
        "deleted_at": None,
        "is_new": True,
        "pinned": False
    }
    return jsonify({"id": chat_id, "title": "New Chat"}), 201

@app.route("/api/chats/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    """Soft delete a chat."""
    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat:
        return jsonify({"error": "Chat not found"}), 404
    chat["deleted"] = True
    chat["deleted_at"] = datetime.now().isoformat()
    return jsonify({"status": "success"})

@app.route("/api/chats/deleted", methods=["GET"])
def get_deleted_chats():
    """List all recently deleted chats."""
    session_data = get_session_data()
    search_query = request.args.get("q", "").strip().lower()
    deleted_chats = []
    
    for cid, chat in session_data["chats"].items():
        if chat.get("deleted"):
            bot = chat["bot"]
            
            # If search query provided, filter
            if search_query:
                title_match = search_query in chat["title"].lower()
                history_match = any(search_query in msg.get("content", msg.get("text", "")).lower() 
                                    for msg in bot.conversation_history)
                if not (title_match or history_match):
                    continue

            deleted_chats.append({
                "id": cid,
                "title": chat["title"],
                "deleted_at": chat.get("deleted_at")
            })
    # Sort most recently deleted first
    deleted_chats.sort(key=lambda x: x["deleted_at"], reverse=True)
    return jsonify({"deleted_chats": deleted_chats})

@app.route("/api/chats/deleted/all", methods=["DELETE"])
def clear_all_deleted_chats():
    """Permanently delete all recently deleted chats."""
    session_data = get_session_data()
    to_delete = [cid for cid, chat in session_data["chats"].items() if chat.get("deleted")]
    for cid in to_delete:
        del session_data["chats"][cid]
    return jsonify({"status": "success", "cleared": len(to_delete)})

@app.route("/api/chats/<chat_id>/recover", methods=["POST"])
def recover_chat(chat_id):
    """Recover a deleted chat."""
    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat or not chat.get("deleted"):
        return jsonify({"error": "Chat not found or not deleted"}), 404
    chat["deleted"] = False
    chat["deleted_at"] = None
    return jsonify({"status": "success", "id": chat_id, "title": chat["title"]})

@app.route("/api/chats/<chat_id>/permanent", methods=["DELETE"])
def permanent_delete_chat(chat_id):
    """Permanently delete a chat from memory."""
    session_data = get_session_data()
    if chat_id in session_data["chats"]:
        del session_data["chats"][chat_id]
        return jsonify({"status": "success"})
    return jsonify({"error": "Chat not found"}), 404

@app.route("/api/messages/pin", methods=["POST"])
def pin_message():
    """Pin a specific bot message."""
    session_data = get_session_data()
    data = request.json or {}
    text = data.get("text", "").strip()
    chat_id = data.get("chat_id")
    if not text or not chat_id:
        return jsonify({"error": "No text or chat_id provided"}), 400
    
    chat = session_data["chats"].get(chat_id)
    if not chat:
        return jsonify({"error": "Chat not found"}), 404
        
    msg_id = str(uuid.uuid4())
    pinned_msg = {
        "id": msg_id,
        "text": text,
        "pinned_at": datetime.now().isoformat()
    }
    chat.setdefault("pinned_messages", []).append(pinned_msg)
    return jsonify({"status": "success", "id": msg_id})

@app.route("/api/messages/unpin/<msg_id>", methods=["DELETE"])
def unpin_message(msg_id):
    """Unpin a specific bot message."""
    session_data = get_session_data()
    for chat in session_data["chats"].values():
        pinned = chat.get("pinned_messages", [])
        original_len = len(pinned)
        chat["pinned_messages"] = [m for m in pinned if m["id"] != msg_id]
        if len(chat["pinned_messages"]) < original_len:
            break
    return jsonify({"status": "success"})

@app.route("/api/messages/pinned", methods=["GET"])
def get_pinned_messages():
    """Get all pinned messages."""
    session_data = get_session_data()
    chat_id = request.args.get("chat_id")
    if not chat_id:
        return jsonify({"pinned_messages": []})
        
    chat = session_data["chats"].get(chat_id)
    if not chat:
        return jsonify({"pinned_messages": []})
        
    pinned = chat.get("pinned_messages", [])
    pinned.sort(key=lambda x: x["pinned_at"], reverse=True)
    return jsonify({"pinned_messages": pinned})

@app.route("/api/chats/<chat_id>/history", methods=["GET"])
def get_chat_history(chat_id):
    """Get message history for a specific chat."""
    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat or chat.get("deleted"):
        return jsonify({"error": "Chat not found"}), 404
    bot = chat["bot"]
    return jsonify({"history": bot.conversation_history})

@app.route("/api/chats/<chat_id>/export/pdf", methods=["GET"])
def export_chat_pdf(chat_id):
    """Generate and return a PDF of the chat history."""
    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat or chat.get("deleted"):
        return jsonify({"error": "No conversation available to export."}), 404
        
    bot = chat["bot"]
    history = bot.conversation_history
    if not history:
        return jsonify({"error": "No conversation available to export."}), 404

    session_data["global_stats"]["pdf_exports"] += 1

    class CustomPDF(FPDF):
        def header(self):
            self.set_font("helvetica", "B", 16)
            self.cell(0, 8, "KMA² Signature Series".encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")
            self.set_font("helvetica", "B", 14)
            self.cell(0, 8, "ARIA Intelligence Framework", ln=True, align="C")
            self.set_font("helvetica", "I", 12)
            self.cell(0, 8, "Conversation Export Report", ln=True, align="C")
            self.ln(10)
            
        def footer(self):
            self.set_y(-25)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, "Generated by ARIA", ln=True, align="C")
            self.cell(0, 5, "Powered by KMA² Intelligence Framework".encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")
            self.cell(0, 5, "KMA² Signature Series".encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")

    pdf = CustomPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)
    
    MODE_MAP = {
        "normal": "Standard Mode",
        "fast": "Fast Mode",
        "deep_thinking": "Deep Thinking Mode",
        "detailed": "Detailed Explanation Mode",
        "interview": "Interview Mode"
    }
    LANG_MAP = {
        "en": "English",
        "ta": "Tamil",
        "te": "Telugu",
        "hi": "Hindi",
        "ml": "Malayalam"
    }

    entries = []
    user_msg = None
    for msg in history:
        role = msg.get("sender", msg.get("role", "Unknown")).upper()
        if role == "USER":
            user_msg = msg
        elif role == "BOT" and user_msg is not None:
            entries.append((user_msg, msg))
            user_msg = None

    for u_msg, b_msg in entries:
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, "--------------------------------------------", ln=True)
        pdf.ln(2)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 6, "USER QUESTION:", ln=True)
        pdf.set_font("helvetica", "", 10)
        u_content = u_msg.get("text", u_msg.get("content", ""))
        pdf.multi_cell(0, 5, u_content.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 6, "SELECTED MODE:", ln=True)
        pdf.set_font("helvetica", "", 10)
        mode_raw = b_msg.get("mode", "normal")
        pdf.cell(0, 6, MODE_MAP.get(mode_raw, mode_raw.title()), ln=True)
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 6, "SELECTED LANGUAGE:", ln=True)
        pdf.set_font("helvetica", "", 10)
        lang_raw = b_msg.get("language", "en")
        pdf.cell(0, 6, LANG_MAP.get(lang_raw, lang_raw.title()), ln=True)
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 11)
        lang_raw = b_msg.get("language", "en")
        if lang_raw != "en":
            pdf.cell(0, 6, "BOT RESPONSE (English Export Version):", ln=True)
            pdf.set_font("helvetica", "", 10)
            b_content = b_msg.get("english_content", b_msg.get("content", ""))
        else:
            pdf.cell(0, 6, "BOT RESPONSE:", ln=True)
            pdf.set_font("helvetica", "", 10)
            b_content = b_msg.get("content", "")
            
        pdf.multi_cell(0, 5, b_content.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 6, "DATE:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 6, b_msg.get("date", datetime.now().strftime("%Y-%m-%d")), ln=True)
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 6, "TIME:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 6, b_msg.get("timestamp", ""), ln=True)
        pdf.ln(2)
        
        pdf.set_font("helvetica", "", 11)
        pdf.cell(0, 6, "--------------------------------------------", ln=True)
        pdf.ln(6)
        
    pdf_output = pdf.output()
    return send_file(
        io.BytesIO(pdf_output),
        as_attachment=True,
        download_name=f"ARIA_Export.pdf",
        mimetype="application/pdf"
    )

@app.route("/api/chats/<chat_id>/export/txt", methods=["GET"])
def export_chat_txt(chat_id):
    """Generate and return a TXT file of the chat history."""
    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat or chat.get("deleted"):
        return jsonify({"error": "No conversation available to export."}), 404
        
    bot = chat["bot"]
    history = bot.conversation_history
    if not history:
        return jsonify({"error": "No conversation available to export."}), 404
        
    session_data["global_stats"]["txt_exports"] += 1

    lines = []
    lines.append("KMA2 Signature Series")
    lines.append("ARIA")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Chat Title: {chat['title']}")
    lines.append("-" * 40)
    
    for msg in history:
        role = msg.get("sender", msg.get("role", "Unknown")).upper()
        content = msg.get("text", msg.get("content", ""))
        lines.append(f"{role}:")
        lines.append(content)
        lines.append("")
        
    txt_output = "\n".join(lines).encode('utf-8')
    return send_file(
        io.BytesIO(txt_output),
        as_attachment=True,
        download_name=f"ARIA_Export.txt",
        mimetype="text/plain"
    )

@app.route("/api/chats/<chat_id>/message", methods=["POST"])
def send_message(chat_id):
    """Send a message to a specific chat."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"].strip()
    language = data.get("language", "en")
    mode = data.get("mode", "normal")
    is_voice = data.get("is_voice", False)
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    session_data = get_session_data()
    chat = session_data["chats"].get(chat_id)
    if not chat or chat.get("deleted"):
        return jsonify({"error": "Chat not found"}), 404
        
    # Update global stats
    if language != "en":
        session_data["global_stats"]["languages_used"].add(language)
    if is_voice:
        session_data["global_stats"]["voice_queries"] += 1

    # Update title if it's the first message
    if chat.get("is_new"):
        chat["title"] = generate_chat_title(user_message)
        chat["is_new"] = False

    bot = chat["bot"]
    response, category = bot.get_response(user_message, language=language, mode=mode)

    # Store mode, language, and date for export, and update bot content to translated response
    if len(bot.conversation_history) >= 2:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        # User message
        bot.conversation_history[-2]["mode"] = mode
        bot.conversation_history[-2]["language"] = language
        bot.conversation_history[-2]["date"] = date_str
        
        # Bot message
        raw_english = bot.conversation_history[-1]["content"]
        if mode != "normal":
            english_export = bot._format_by_mode(raw_english, mode, user_message, category)
        else:
            english_export = raw_english
            
        bot.conversation_history[-1]["mode"] = mode
        bot.conversation_history[-1]["language"] = language
        bot.conversation_history[-1]["date"] = date_str
        bot.conversation_history[-1]["english_content"] = english_export
        bot.conversation_history[-1]["content"] = response

    return jsonify({
        "response": response,
        "category": category,
        "timestamp": datetime.now().strftime("%H:%M"),
        "is_farewell": category == "farewell",
        "user_name": bot.user_name,
        "chat_title": chat["title"]
    })


# ==============================================================================
# LEGACY ROUTES (Maintained for UI compatibility if needed)
# ==============================================================================

@app.route("/api/stats", methods=["GET"])
def stats():
    """GET /api/stats — Return overall session statistics."""
    session_data = get_session_data()
    total_messages = 0
    total_chats = 0
    
    for chat in session_data["chats"].values():
        if not chat.get("deleted"):
            total_chats += 1
            total_messages += chat["bot"].message_count
                
    pinned_count = len(session_data.get("pinned_messages", []))
    g_stats = session_data["global_stats"]
    duration = datetime.now() - g_stats["session_start"]
    minutes = int(duration.total_seconds() // 60)
    seconds = int(duration.total_seconds() % 60)
    
    return jsonify({
        "messages": total_messages,
        "chats": total_chats,
        "pinned_messages": pinned_count,
        "duration": f"{minutes}m {seconds}s"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "ARIA Chatbot API", "version": "2.0.0"})

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("\n[ARIA] Multi-Chat Web Server Starting...")
    print("[URL]  http://localhost:5000")
    print("[STOP] Press Ctrl+C to stop\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

