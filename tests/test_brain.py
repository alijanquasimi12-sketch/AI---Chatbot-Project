"""
test_brain.py — Unit Tests for ARIA Chatbot Engine
===================================================
Tests all rule-based response categories to ensure
correct behavior of the if-else decision logic.

Run with: python -m pytest tests/ -v

Author: DecodeLabs AI Engineering Team
Project: AI Chatbot Project 1 - Rule-Based AI
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.brain import ChatBot, KnowledgeBase


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def bot():
    """Fresh chatbot instance for each test."""
    return ChatBot(name="ARIA")


@pytest.fixture
def kb():
    """KnowledgeBase instance."""
    return KnowledgeBase()


# ── Tests: KnowledgeBase ─────────────────────────────────────────────────────

class TestKnowledgeBase:
    """Test that the knowledge base contains required data."""

    def test_greeting_triggers_not_empty(self, kb):
        assert len(kb.GREETING_TRIGGERS) > 0

    def test_farewell_triggers_not_empty(self, kb):
        assert len(kb.FAREWELL_TRIGGERS) > 0

    def test_greeting_responses_not_empty(self, kb):
        assert len(kb.GREETING_RESPONSES) > 0

    def test_jokes_list_not_empty(self, kb):
        assert len(kb.JOKES) > 0

    def test_motivational_quotes_not_empty(self, kb):
        assert len(kb.MOTIVATIONAL_QUOTES) > 0

    def test_ai_responses_not_empty(self, kb):
        assert len(kb.AI_RESPONSES) > 0

    def test_help_response_contains_keywords(self, kb):
        assert "help" in kb.HELP_RESPONSE.lower()
        assert "bye" in kb.HELP_RESPONSE.lower()


# ── Tests: Greeting Responses ─────────────────────────────────────────────────

class TestGreetings:
    """Rule 3: Greetings should return greeting category."""

    @pytest.mark.parametrize("user_input", [
        "hello", "Hello!", "hi", "hey", "howdy", "greetings",
        "good morning", "good evening", "hiya", "namaste"
    ])
    def test_greeting_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "greeting", f"Expected 'greeting' for '{user_input}', got '{category}'"
        assert len(response) > 0

    def test_greeting_response_is_string(self, bot):
        response, _ = bot.get_response("hello")
        assert isinstance(response, str)


# ── Tests: Farewell Responses ─────────────────────────────────────────────────

class TestFarewells:
    """Rule 2: Farewells should return farewell category."""

    @pytest.mark.parametrize("user_input", [
        "bye", "goodbye", "exit", "quit", "see you later",
        "farewell", "take care", "goodnight"
    ])
    def test_farewell_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "farewell", f"Expected 'farewell' for '{user_input}', got '{category}'"

    def test_is_farewell_method_true(self, bot):
        assert bot.is_farewell("bye") is True
        assert bot.is_farewell("exit") is True

    def test_is_farewell_method_false(self, bot):
        assert bot.is_farewell("hello") is False
        assert bot.is_farewell("what is AI?") is False


# ── Tests: Small Talk ─────────────────────────────────────────────────────────

class TestSmallTalk:
    """Rule 4: 'How are you' type inputs."""

    @pytest.mark.parametrize("user_input", [
        "how are you", "how are you doing", "how do you do",
        "how's it going", "you good"
    ])
    def test_how_are_you_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "smalltalk"

    def test_response_is_not_empty(self, bot):
        response, _ = bot.get_response("how are you")
        assert len(response.strip()) > 0


# ── Tests: Identity ───────────────────────────────────────────────────────────

class TestIdentity:
    """Rule 5: Bot should identify itself correctly."""

    @pytest.mark.parametrize("user_input", [
        "what is your name", "who are you", "introduce yourself",
        "what are you called"
    ])
    def test_identity_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "identity"

    def test_name_in_response(self, bot):
        response, _ = bot.get_response("who are you")
        assert "ARIA" in response


# ── Tests: Help ───────────────────────────────────────────────────────────────

class TestHelp:
    """Rule 6: Help menu."""

    @pytest.mark.parametrize("user_input", ["help", "what can you do", "menu", "commands"])
    def test_help_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "help"

    def test_help_response_complete(self, bot):
        response, _ = bot.get_response("help")
        assert len(response) > 100   # Must be a substantive response


# ── Tests: Time & Date ────────────────────────────────────────────────────────

class TestTimeDate:
    """Rules 8 & 9: Time and date queries."""

    def test_time_query(self, bot):
        response, category = bot.get_response("what time is it")
        assert category == "time"
        assert len(response) > 0

    def test_date_query(self, bot):
        response, category = bot.get_response("what is today's date")
        assert category == "date"
        assert len(response) > 0


# ── Tests: Math ───────────────────────────────────────────────────────────────

class TestMath:
    """Rule 10: Math calculations."""

    @pytest.mark.parametrize("expression,expected", [
        ("what is 5 + 3", "8"),
        ("calculate 10 - 4", "6"),
        ("10 * 5", "50"),
        ("20 / 4", "5"),
    ])
    def test_math_calculation(self, bot, expression, expected):
        response, category = bot.get_response(expression)
        assert category == "math", f"Expected math category for '{expression}'"
        assert expected in response, f"Expected '{expected}' in response for '{expression}'"

    def test_division_by_zero(self, bot):
        response, _ = bot.get_response("calculate 10 / 0")
        assert "zero" in response.lower() or "undefined" in response.lower()


# ── Tests: AI Knowledge ───────────────────────────────────────────────────────

class TestAIKnowledge:
    """Rule 11: AI-related questions."""

    @pytest.mark.parametrize("user_input", [
        "what is ai", "tell me about ai", "explain artificial intelligence",
        "what is machine learning", "what is deep learning"
    ])
    def test_ai_knowledge_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "ai_knowledge"


# ── Tests: Python ─────────────────────────────────────────────────────────────

class TestPython:
    """Rule 12: Python-related questions."""

    def test_python_detected(self, bot):
        response, category = bot.get_response("tell me about python")
        assert category == "python"

    def test_python_for_ai(self, bot):
        response, category = bot.get_response("why use python for ai")
        assert category == "python"


# ── Tests: Jokes ──────────────────────────────────────────────────────────────

class TestJokes:
    """Rule 14: Jokes."""

    @pytest.mark.parametrize("user_input", [
        "tell me a joke", "joke", "make me laugh", "say something funny"
    ])
    def test_joke_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "joke"

    def test_joke_is_funny(self, bot):
        """Jokes should be at least 10 chars."""
        response, _ = bot.get_response("tell me a joke")
        assert len(response) > 10


# ── Tests: Motivation ─────────────────────────────────────────────────────────

class TestMotivation:
    """Rule 15: Motivational quotes."""

    @pytest.mark.parametrize("user_input", [
        "motivate me", "inspire me", "i need motivation"
    ])
    def test_motivation_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "motivation"


# ── Tests: Thanks ─────────────────────────────────────────────────────────────

class TestThanks:
    """Rule 16: Gratitude expressions."""

    @pytest.mark.parametrize("user_input", [
        "thank you", "thanks", "thank u", "appreciate it"
    ])
    def test_thanks_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "thanks"


# ── Tests: Username Detection ─────────────────────────────────────────────────

class TestUsernameDetection:
    """Rule 1: Bot should detect and remember user's name."""

    def test_name_detected_my_name_is(self, bot):
        response, category = bot.get_response("my name is Alice")
        assert category == "personal"
        assert bot.user_name == "Alice"

    def test_name_detected_i_am(self, bot):
        bot.get_response("i am Bob")
        assert bot.user_name == "Bob"

    def test_name_remembered_in_follow_up(self, bot):
        bot.get_response("my name is Charlie")
        assert bot.user_name == "Charlie"


# ── Tests: Unknown Input ──────────────────────────────────────────────────────

class TestUnknownInput:
    """Rule 17: Unrecognized inputs should return 'unknown' category."""

    @pytest.mark.parametrize("user_input", [
        "asdfghjkl", "xyzzy plugh", "qwerty random nonsense",
        "the color of sadness on a Tuesday"
    ])
    def test_unknown_detected(self, bot, user_input):
        response, category = bot.get_response(user_input)
        assert category == "unknown"
        assert len(response) > 0

    def test_empty_input(self, bot):
        response, category = bot.get_response("")
        assert category == "error"
        assert len(response) > 0

    def test_whitespace_only(self, bot):
        response, category = bot.get_response("   ")
        assert category == "error"


# ── Tests: Conversation History ───────────────────────────────────────────────

class TestConversationHistory:
    """Conversation logging and history tracking."""

    def test_history_grows_with_messages(self, bot):
        initial_len = len(bot.conversation_history)
        bot.get_response("hello")
        assert len(bot.conversation_history) > initial_len

    def test_message_count_increments(self, bot):
        assert bot.message_count == 0
        bot.get_response("hi")
        assert bot.message_count == 1
        bot.get_response("how are you")
        assert bot.message_count == 2

    def test_history_contains_user_and_bot(self, bot):
        bot.get_response("hello")
        roles = {entry["role"] for entry in bot.conversation_history}
        assert "user" in roles
        assert "bot" in roles


# ── Tests: Stats ──────────────────────────────────────────────────────────────

class TestStats:
    """Session statistics."""

    def test_stats_returns_dict(self, bot):
        stats = bot.get_stats()
        assert isinstance(stats, dict)

    def test_stats_has_required_keys(self, bot):
        stats = bot.get_stats()
        assert "messages" in stats
        assert "duration" in stats
        assert "user_name" in stats
        assert "session_start" in stats

    def test_stats_messages_increments(self, bot):
        bot.get_response("hi")
        bot.get_response("how are you")
        stats = bot.get_stats()
        assert stats["messages"] == 2


# ── Tests: Normalization ──────────────────────────────────────────────────────

class TestNormalization:
    """Input normalization should handle edge cases."""

    def test_uppercase_greeting(self, bot):
        response, category = bot.get_response("HELLO")
        assert category == "greeting"

    def test_mixed_case_farewell(self, bot):
        response, category = bot.get_response("BYE!")
        assert category == "farewell"

    def test_punctuation_stripped(self, bot):
        response, category = bot.get_response("Hello!!!")
        assert category == "greeting"

    def test_extra_whitespace(self, bot):
        response, category = bot.get_response("   hello   ")
        assert category == "greeting"


# ── Run tests standalone ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import subprocess
    subprocess.run([sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"])
