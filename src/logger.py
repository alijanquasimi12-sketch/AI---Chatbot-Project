"""
logger.py - Conversation Logger & Analytics Module
===================================================
Handles saving conversation logs, session analytics,
and generating session reports.

Author: DecodeLabs AI Engineering Team
Project: AI Chatbot Project 1 - Rule-Based AI
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ConversationLogger:
    """
    Saves chat sessions to JSON and plain-text log files.
    Provides analytics on conversation patterns.
    """

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_session(self, history: list[dict], stats: dict) -> str:
        """Save conversation session to a JSON file."""
        session_data = {
            "session_id": self.session_id,
            "stats": stats,
            "conversation": history,
            "saved_at": datetime.now().isoformat(),
        }

        json_path = self.log_dir / f"session_{self.session_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        # Also save a readable text version
        txt_path = self.log_dir / f"session_{self.session_id}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"ARIA Chatbot — Session Log\n")
            f.write(f"{'=' * 50}\n")
            f.write(f"Session ID : {self.session_id}\n")
            f.write(f"Started at : {stats.get('session_start', 'N/A')}\n")
            f.write(f"Duration   : {stats.get('duration', 'N/A')}\n")
            f.write(f"User       : {stats.get('user_name', 'Unknown')}\n")
            f.write(f"Messages   : {stats.get('messages', 0)}\n")
            f.write(f"{'=' * 50}\n\n")
            for entry in history:
                role = "You " if entry["role"] == "user" else "ARIA"
                f.write(f"[{entry['timestamp']}] {role}: {entry['content']}\n\n")

        return str(json_path)

    def get_category_analytics(self, history: list[dict]) -> dict:
        """Analyze conversation patterns from history."""
        user_messages = [e["content"] for e in history if e["role"] == "user"]
        total = len(user_messages)
        if total == 0:
            return {}
        return {
            "total_messages": total,
            "avg_message_length": sum(len(m) for m in user_messages) // max(total, 1),
            "longest_message": max((len(m) for m in user_messages), default=0),
        }
