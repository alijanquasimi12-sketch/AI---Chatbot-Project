"""
brain.py - Rule-Based AI Chatbot Core Engine
=============================================
The central decision-making module of the chatbot.
Implements pure if-else / rule-based logic to simulate
intelligent conversation through programmatic decision-making.

Author: DecodeLabs AI Engineering Team
Project: AI Chatbot Project 1 - Rule-Based AI
Batch: 2026
"""

import random
import re
from datetime import datetime


# ==============================================================================
# KNOWLEDGE BASE — All rules and responses live here
# ==============================================================================

class KnowledgeBase:
    """
    Contains all predefined rules, patterns, and responses.
    This is the 'brain' of the rule-based AI system.
    """

    # ── Greeting patterns ──────────────────────────────────────────────────────
    # NOTE: Use only standalone words to avoid substring conflicts
    GREETING_TRIGGERS = [
        r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bhowdy\b", r"\bgreetings\b",
        r"\bsup\b", r"\bwhats up\b", r"\bhiya\b", r"\bnamaste\b", r"\bhola\b",
        r"\bgood morning\b", r"\bgood afternoon\b", r"\bgood evening\b",
    ]

    GREETING_RESPONSES = [
        "Hello there! 👋 I'm ARIA (Artificial Rule-based Intelligent Assistant). How can I help you today?",
        "Hi! Great to see you! 😊 I'm ARIA, your AI companion. What's on your mind?",
        "Hey! ARIA here, ready to assist! 🤖 Ask me anything!",
        "Greetings, human! 🌟 I'm ARIA. I'm here to help. What can I do for you?",
        "Hello! Welcome! 😄 I'm ARIA — let's have a great conversation!",
    ]

    # ── Farewell patterns ──────────────────────────────────────────────────────
    FAREWELL_TRIGGERS = [
        r"\bbye\b", r"\bgoodbye\b", r"\bexit\b", r"\bquit\b", r"\bsee you\b",
        r"\bfarewell\b", r"\btake care\b", r"\bcya\b", r"\badios\b",
        r"\bgoodnight\b", r"\bgood night\b", r"\bttyl\b", r"\bsigning off\b",
    ]

    FAREWELL_RESPONSES = [
        "Goodbye! 👋 It was wonderful chatting with you. Come back anytime!",
        "See you later! 🌟 Remember, I'm always here when you need me!",
        "Farewell! 😊 Stay curious and keep learning!",
        "Take care! 🤖 It was a pleasure being your AI assistant today!",
        "Bye bye! 👋 Come back soon — I'll be here, thinking in if-else! 😄",
    ]

    # ── How are you patterns ───────────────────────────────────────────────────
    HOW_ARE_YOU_TRIGGERS = [
        r"how are you", r"how do you do", r"how are you doing", r"how.?s it going",
        r"how r u", r"\byou okay\b", r"\byou good\b", r"feeling okay", r"doing well",
    ]

    HOW_ARE_YOU_RESPONSES = [
        "I'm doing fantastically well, thanks for asking! 😄 I've been processing millions of if-else statements — keeps me sharp!",
        "Running at peak performance! 🚀 Every decision tree is fully optimized today. How about you?",
        "I'm great! 🌟 Being a rule-based AI means I'm always consistent — never having a bad day!",
        "Excellent! 💡 I just learned 3 new response patterns. Growing smarter every conversation!",
    ]

    # ── Name / identity patterns ───────────────────────────────────────────────
    NAME_TRIGGERS = [
        r"what is your name", r"what.?s your name", r"\bwho are you\b",
        r"your name", r"tell me about yourself", r"introduce yourself",
        r"who made you", r"what are you called", r"what should i call you",
    ]

    NAME_RESPONSES = [
        "I'm ARIA — Artificial Rule-based Intelligent Assistant! 🤖 Built by DecodeLabs as Project 1 of the AI Engineering track.",
        "My name is ARIA! 🌟 I'm a rule-based AI chatbot created to demonstrate control flow, decision-making logic, and basic AI concepts.",
        "Call me ARIA! 😊 I'm a first-generation AI built with pure Python if-else logic — the foundation of all AI systems!",
    ]

    # ── AI / Technology knowledge ──────────────────────────────────────────────
    AI_TRIGGERS = [
        r"what is ai\b", r"artificial intelligence", r"machine learning",
        r"tell me about ai", r"explain ai", r"how does ai work", r"deep learning",
        r"neural network", r"\bnlp\b", r"natural language processing",
        r"what is a chatbot", r"how are chatbots made", r"rule.?based", r"decision tree",
    ]

    AI_RESPONSES = [
        (
            "🤖 Artificial Intelligence (AI) is the simulation of human intelligence by machines!\n\n"
            "Key branches:\n"
            "  • Rule-Based AI → Uses if-else logic (that's me! 😄)\n"
            "  • Machine Learning → Learns from data\n"
            "  • Deep Learning → Neural networks with layers\n"
            "  • NLP → Understanding human language\n\n"
            "I'm a Rule-Based AI — the very foundation layer of this pyramid!"
        ),
        (
            "💡 AI works by mimicking human decision-making!\n\n"
            "Rule-Based AI (like me) uses:\n"
            "  → Pattern matching\n"
            "  → If-else conditionals\n"
            "  → Predefined knowledge bases\n\n"
            "This approach is transparent, predictable, and powerful for structured domains!"
        ),
        (
            "🧠 Machine Learning is a subset of AI where systems LEARN from experience!\n\n"
            "Unlike me (rule-based), ML models:\n"
            "  • Train on thousands/millions of examples\n"
            "  • Find statistical patterns automatically\n"
            "  • Improve accuracy over time\n\n"
            "But before ML, every AI engineer must master if-else logic — that's why you're here!"
        ),
    ]

    # ── Python knowledge ───────────────────────────────────────────────────────
    PYTHON_TRIGGERS = [
        "python", "what is python", "learn python", "python programming",
        "python language", "why python", "python for ai"
    ]

    PYTHON_RESPONSES = [
        (
            "🐍 Python is the #1 language for AI engineering!\n\n"
            "Why Python for AI?\n"
            "  ✓ Simple, readable syntax\n"
            "  ✓ Massive ecosystem (NumPy, Pandas, TensorFlow, PyTorch)\n"
            "  ✓ Rapid prototyping\n"
            "  ✓ Huge community support\n\n"
            "Pro tip: Master Python fundamentals before jumping to AI libraries!"
        ),
    ]

    # ── Help / capabilities ────────────────────────────────────────────────────
    HELP_TRIGGERS = [
        r"\bhelp\b", r"what can you do", r"\bcommands\b", r"\bfeatures\b",
        r"\boptions\b", r"\bcapabilities\b", r"what do you know", r"\btopics\b",
        r"\bmenu\b",
    ]

    HELP_RESPONSE = (
        "🆘 ARIA Help Center\n"
        "═══════════════════════════════════\n"
        "Here's what I can chat about:\n\n"
        "  🤖 AI & Technology   → Ask about AI, ML, Deep Learning\n"
        "  🐍 Python            → Python tips and tricks\n"
        "  😄 Jokes             → Need a laugh? Just ask!\n"
        "  🌤  Weather          → Ask about weather\n"
        "  🕐 Time & Date       → Current time/date info\n"
        "  💬 Small Talk        → Greetings, how are you, etc.\n"
        "  🧮 Math              → Simple calculations\n"
        "  💡 Motivation        → Get inspired!\n\n"
        "Commands:\n"
        "  'help'    → Show this menu\n"
        "  'history' → View conversation history\n"
        "  'clear'   → Clear the screen\n"
        "  'bye'     → Exit the chatbot\n"
        "═══════════════════════════════════"
    )

    # ── Jokes ──────────────────────────────────────────────────────────────────
    JOKE_TRIGGERS = [
        r"tell me a joke", r"\bjoke\b", r"make me laugh", r"\bfunny\b",
        r"\bhumor\b", r"say something funny", r"entertain me",
    ]

    JOKES = [
        "Why do programmers prefer dark mode? 🌙\nBecause light attracts bugs! 🐛😄",
        "Why did the AI break up with the database? 💔\nBecause it found someone with better relations! 😄",
        "How many programmers does it take to change a light bulb? 💡\nNone — that's a hardware problem! 😂",
        "Why do Python programmers wear glasses? 👓\nBecause they can't C! 😄",
        "What did the chatbot say to the database? 🤖\n'You complete me... with SELECT *!' 💾",
        "Why was the AI so calm during the meeting? 🧘\nBecause it had already processed all the edge cases! 😄",
        "I told an AI a joke about UDP...\nI don't know if it got it. 📡😂",
        "What's an AI's favorite type of music? 🎵\nAlgo-rhythm! 🎶😄",
    ]

    # ── Motivation ─────────────────────────────────────────────────────────────
    MOTIVATION_TRIGGERS = [
        r"motivate me", r"\bmotivation\b", r"inspire me", r"\bquote\b",
        r"encouragement", r"feeling sad", r"feeling down", r"need motivation",
        r"keep going", r"don.?t give up",
    ]

    MOTIVATIONAL_QUOTES = [
        "💪 'The expert in anything was once a beginner.' — Helen Hayes\nYou're already on the right path — keep coding!",
        "🌟 'The best way to predict the future is to create it.' — Peter Drucker\nEvery line of code you write shapes the future!",
        "🚀 'Don't watch the clock; do what it does. Keep going.' — Sam Levenson\nYour AI journey is just beginning — amazing things ahead!",
        "💡 'Code is poetry.' — WordPress motto\nEvery function you write is an artistic expression of logic!",
        "🎯 'First, solve the problem. Then, write the code.' — John Johnson\nThinking before coding = the mark of a true engineer!",
        "🤖 'Artificial intelligence is the new electricity.' — Andrew Ng\nYou're learning to harness one of the most powerful technologies!",
        "⭐ 'The only way to do great work is to love what you do.' — Steve Jobs\nFall in love with problem-solving — it's the heart of AI!",
    ]

    # ── Time & Date ────────────────────────────────────────────────────────────
    TIME_TRIGGERS = [
        r"what time is it", r"current time", r"time now", r"what.?s the time",
        r"tell me the time",
    ]

    DATE_TRIGGERS = [
        r"today.?s date", r"what.?s today", r"current date",
        r"what day is it", r"day today", r"what is today",
    ]

    # ── Weather ────────────────────────────────────────────────────────────────
    WEATHER_TRIGGERS = [
        r"\bweather\b", r"what.?s the weather", r"\btemperature\b",
        r"is it raining", r"\bforecast\b", r"\bclimate\b",
    ]

    WEATHER_RESPONSES = [
        "🌤 I don't have live weather access, but I'd recommend checking weather.com or Google Weather!\nHere's a tip: 'python weather' apps use the OpenWeatherMap API — a great next project idea! 🚀",
        "⛅ I can't check real-time weather, but you can ask me how to BUILD a weather bot with Python! 🐍\nHint: It uses the requests library and a free weather API!",
    ]

    # ── Math ───────────────────────────────────────────────────────────────────
    MATH_TRIGGERS = [
        r"\bcalculate\b", r"\bcompute\b", r"\bmath\b",
        r"\bequals\b", r"\bplus\b", r"\bminus\b", r"\btimes\b", r"\bdivided\b",
        r"\d+\s*[\+\-\*\/x]\s*\d+",  # Direct expression like "5 + 3"
    ]

    # ── Gratitude ──────────────────────────────────────────────────────────────
    THANKS_TRIGGERS = [
        r"thank you", r"\bthanks\b", r"thank u\b", r"\bthx\b", r"\bty\b",
        r"appreciate it", r"\bcheers\b", r"nice one", r"good job", r"well done",
    ]

    THANKS_RESPONSES = [
        "You're welcome! 😊 Happy to help! Ask me anything else!",
        "My pleasure! 🌟 That's what I'm here for!",
        "Glad I could help! 🤖 Any other questions?",
        "Anytime! 😄 I'm always here for you!",
    ]

    # ── Unknown ────────────────────────────────────────────────────────────────
    UNKNOWN_RESPONSES = [
        "Hmm, I'm not sure I understand that. 🤔 Could you rephrase it?\nType 'help' to see what I can discuss!",
        "I don't quite get that yet! 🤖 My rule-base doesn't cover that topic.\nTry asking about AI, Python, jokes, or type 'help'!",
        "Interesting question! 🧐 But I haven't been programmed with a rule for that.\nAs a rule-based AI, I can only respond to known patterns. Type 'help' for options!",
        "That's beyond my current rule set! 💡 But it's a great idea — I could be expanded to handle it!\nFor now, type 'help' to see my capabilities.",
    ]


# ==============================================================================
# CHATBOT ENGINE
# ==============================================================================

class ChatBot:
    """
    ARIA — Artificial Rule-based Intelligent Assistant
    
    The main chatbot engine implementing rule-based conversation logic.
    Uses pattern matching with if-else control flow to generate responses.
    
    This is the foundational architecture before introducing ML/DL systems.
    """

    def __init__(self, name: str = "ARIA"):
        self.name = name
        self.kb = KnowledgeBase()
        self.conversation_history: list[dict] = []
        self.session_start = datetime.now()
        self.message_count = 0
        self.user_name: str | None = None

    def _normalize(self, text: str) -> str:
        """Convert input to lowercase and strip whitespace for matching.
        NOTE: We preserve digits and operators for math detection."""
        text = text.lower().strip()
        # Only strip standard punctuation, keep math operators
        text = re.sub(r"[^\w\s\+\-\*\/\.]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _contains_any(self, text: str, triggers: list[str]) -> bool:
        """Check if the text matches any trigger using regex search."""
        for trigger in triggers:
            if re.search(trigger, text, re.IGNORECASE):
                return True
        return False

    def _try_math(self, text: str) -> str | None:
        """Attempt to evaluate a simple mathematical expression from the input."""
        # Look for patterns like "what is 5 + 3" or "calculate 10 * 4"
        math_pattern = re.search(r"(\d+\.?\d*)\s*([\+\-\*\/x])\s*(\d+\.?\d*)", text)
        if math_pattern:
            a_str, op, b_str = math_pattern.groups()
            a, b = float(a_str), float(b_str)
            try:
                if op in ("+",):
                    result = a + b
                elif op == "-":
                    result = a - b
                elif op in ("*", "x"):
                    result = a * b
                elif op == "/":
                    if b == 0:
                        return "❌ Division by zero is undefined! Even for an AI that's a problem! 😄"
                    result = a / b
                else:
                    return None

                # Format nicely
                result_str = str(int(result)) if result == int(result) else f"{result:.4f}"
                return f"🧮 {a_str} {op} {b_str} = **{result_str}**\nMath is the language of the universe! 🌌"
            except Exception:
                return None
        return None

    def _check_user_name(self, text: str) -> str | None:
        """Detect if user is telling us their name."""
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"you can call me (\w+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).capitalize()
        return None

    def _log_message(self, role: str, message: str) -> None:
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

    def get_response(self, user_input: str) -> tuple[str, str]:
        """
        Core decision-making function.
        
        Implements the rule-based AI logic using if-else control flow.
        Returns a tuple of (response_text, category).
        
        This is the fundamental architecture of:
        1. Input normalization
        2. Pattern matching
        3. Rule lookup
        4. Response generation
        """
        raw_input = user_input
        normalized = self._normalize(user_input)
        self.message_count += 1

        # Log user input
        self._log_message("user", raw_input)

        # ── RULE 0: Empty input ────────────────────────────────────────────────
        if not normalized.strip():
            response = "I didn't catch that! 😊 Please type something. Type 'help' if you need guidance."
            self._log_message("bot", response)
            return response, "error"

        # ── RULE 1: Detect username ────────────────────────────────────────────
        detected_name = self._check_user_name(normalized)
        if detected_name:
            self.user_name = detected_name
            response = f"Nice to meet you, {detected_name}! 😊 I'll remember your name. How can I help you today?"
            self._log_message("bot", response)
            return response, "personal"

        # ── RULE 2: Farewells / Exit commands ─────────────────────────────────
        if self._contains_any(normalized, self.kb.FAREWELL_TRIGGERS):
            farewell = random.choice(self.kb.FAREWELL_RESPONSES)
            if self.user_name:
                farewell = farewell.replace("!", f", {self.user_name}!", 1)
            response = farewell
            self._log_message("bot", response)
            return response, "farewell"

        # ── RULE 3: Greetings ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.GREETING_TRIGGERS):
            greeting = random.choice(self.kb.GREETING_RESPONSES)
            if self.user_name:
                greeting = greeting.replace("there!", f", {self.user_name}!")
            response = greeting
            self._log_message("bot", response)
            return response, "greeting"

        # ── RULE 4: How are you ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HOW_ARE_YOU_TRIGGERS):
            response = random.choice(self.kb.HOW_ARE_YOU_RESPONSES)
            self._log_message("bot", response)
            return response, "smalltalk"

        # ── RULE 5: Name / Identity ────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.NAME_TRIGGERS):
            response = random.choice(self.kb.NAME_RESPONSES)
            self._log_message("bot", response)
            return response, "identity"

        # ── RULE 6: Help menu ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HELP_TRIGGERS):
            response = self.kb.HELP_RESPONSE
            self._log_message("bot", response)
            return response, "help"

        # ── RULE 7: Conversation history ───────────────────────────────────────
        if "history" in normalized:
            response = self._format_history()
            self._log_message("bot", response)
            return response, "meta"

        # ── RULE 8: Time query ─────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.TIME_TRIGGERS):
            now = datetime.now()
            response = (
                f"🕐 Current time: **{now.strftime('%I:%M:%S %p')}**\n"
                f"(System timezone — {now.strftime('%A, %d %B %Y')})"
            )
            self._log_message("bot", response)
            return response, "time"

        # ── RULE 9: Date query ─────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.DATE_TRIGGERS):
            now = datetime.now()
            response = (
                f"📅 Today is: **{now.strftime('%A, %d %B %Y')}**\n"
                f"Day {now.timetuple().tm_yday} of the year!"
            )
            self._log_message("bot", response)
            return response, "date"

        # ── RULE 10: Math calculation ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.MATH_TRIGGERS):
            math_result = self._try_math(normalized)
            if math_result:
                self._log_message("bot", math_result)
                return math_result, "math"

        # ── RULE 11: AI / Technology knowledge ────────────────────────────────
        if self._contains_any(normalized, self.kb.AI_TRIGGERS):
            response = random.choice(self.kb.AI_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 12: Python knowledge ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.PYTHON_TRIGGERS):
            response = random.choice(self.kb.PYTHON_RESPONSES)
            self._log_message("bot", response)
            return response, "python"

        # ── RULE 13: Weather ───────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.WEATHER_TRIGGERS):
            response = random.choice(self.kb.WEATHER_RESPONSES)
            self._log_message("bot", response)
            return response, "weather"

        # ── RULE 14: Jokes ─────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.JOKE_TRIGGERS):
            response = random.choice(self.kb.JOKES)
            self._log_message("bot", response)
            return response, "joke"

        # ── RULE 15: Motivation ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.MOTIVATION_TRIGGERS):
            response = random.choice(self.kb.MOTIVATIONAL_QUOTES)
            self._log_message("bot", response)
            return response, "motivation"

        # ── RULE 16: Thanks / Gratitude ────────────────────────────────────────
        if self._contains_any(normalized, self.kb.THANKS_TRIGGERS):
            response = random.choice(self.kb.THANKS_RESPONSES)
            self._log_message("bot", response)
            return response, "thanks"

        # ── RULE 17: DecodeLabs info ───────────────────────────────────────────
        if "decodelabs" in normalized or "decode labs" in normalized:
            response = (
                "🏢 DecodeLabs is an industrial training company focused on real-world tech skills!\n\n"
                "🌐 Website: www.decodelabs.tech\n"
                "📍 Location: Greater Lucknow, India\n"
                "📞 Phone: +91 89330 06408\n"
                "✉ Email: decodelabs.tech@gmail.com\n\n"
                "I'm ARIA — their AI Project 1! 🤖 Proud to represent DecodeLabs!"
            )
            self._log_message("bot", response)
            return response, "about"

        # ── DEFAULT: Unknown input ─────────────────────────────────────────────
        response = random.choice(self.kb.UNKNOWN_RESPONSES)
        self._log_message("bot", response)
        return response, "unknown"

    def _format_history(self) -> str:
        """Format conversation history for display."""
        if len(self.conversation_history) <= 2:
            return "📜 No conversation history yet — we're just getting started! 😊"
        
        lines = ["📜 Conversation History\n" + "═" * 40]
        count = 0
        for entry in self.conversation_history[-10:]:  # Last 10 messages
            role_icon = "👤 You" if entry["role"] == "user" else "🤖 ARIA"
            lines.append(f"[{entry['timestamp']}] {role_icon}: {entry['content'][:80]}...")
            count += 1
        lines.append(f"\nShowing last {count} messages of {len(self.conversation_history)} total.")
        return "\n".join(lines)

    def get_stats(self) -> dict:
        """Return session statistics."""
        duration = datetime.now() - self.session_start
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return {
            "messages": self.message_count,
            "duration": f"{minutes}m {seconds}s",
            "user_name": self.user_name or "Unknown",
            "session_start": self.session_start.strftime("%H:%M:%S"),
        }

    def is_farewell(self, user_input: str) -> bool:
        """Check if the user wants to exit the conversation."""
        normalized = self._normalize(user_input)
        return self._contains_any(normalized, self.kb.FAREWELL_TRIGGERS)
