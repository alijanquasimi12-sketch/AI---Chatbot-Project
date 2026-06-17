"""
brain.py - KMA² Intelligence Framework — Rule-Based AI Core Engine
===================================================================
The central decision-making module of the chatbot.
Implements pure rule-based logic to simulate intelligent conversation
through programmatic decision-making and pattern matching.

Architecture: KMA² Signature Series
Framework:    KMA² Intelligence Framework v3.0
Features:     Smart Intent Detection Engine (9-layer matching)
"""

import random
import re
from datetime import datetime


# ==============================================================================
# SMART INTENT DETECTION ENGINE
# ==============================================================================

class SmartMatcher:
    """
    9-Layer Smart Intent Matching Engine.
    Implements: Exact, Partial, Keyword, Phrase, Synonym, Context,
                Fuzzy, Intent Scoring, and Fallback matching.
    """

    # Common synonyms / paraphrase groups
    SYNONYM_MAP = {
        # Developer / creator synonyms
        r"\bcreator\b":         "developer",
        r"\bcreators\b":        "developer",
        r"\bbuilder\b":         "developer",
        r"\bbuilders\b":        "developer",
        r"\bauthor\b":          "developer",
        r"\bauthors\b":         "developer",
        r"\bengineered\b":      "developed",
        r"\bdesigned\b":        "developed",
        r"\bprogrammed\b":      "developed",
        r"\bcoded\b":           "developed",
        r"\bcreated\b":         "developed",
        r"\bcraft(?:ed)?\b":    "developed",
        r"\bmade\b":            "developed",
        r"\bbuilt\b":           "developed",
        r"\bproduced\b":        "developed",
        r"\bfounded\b":         "developed",
        r"\bdiscovered\b":      "developed",
        r"\binvented\b":        "developed",
        r"\bprogrammer\b":      "developer",
        r"\bcoder\b":           "developer",
        r"\barchitect\b":       "developer",
        r"\bengineers?\b":      "developer",
        r"\bowner\b":           "developer",
        r"\bowners?\b":         "developer",
        r"\bteam\b":            "developer",
        r"\borganization\b":    "developer",
        r"\borganisation\b":    "developer",
        r"\bcompany\b":         "developer",
        # Origin / source synonyms
        r"\borigin\b":          "developer",
        r"\borigins\b":         "developer",
        r"\bexistence\b":       "developer",
        r"\bbehind\b":          "developer",
        r"\bresponsible for\b": "developer",
        # Project/chatbot synonyms
        r"\bchatbot\b":         "project",
        r"\bbot\b":             "project",
        r"\baria\b":            "project",
        r"\bthis ai\b":         "project",
        r"\bthis app\b":        "project",
        r"\bthis system\b":     "project",
        r"\bthis tool\b":       "project",
        r"\bthis product\b":    "project",
        r"\bthis assistant\b":  "project",
        r"\bthis platform\b":   "project",
        r"\byou\b":             "project",  # "who created you" → "who developed project"
        # Info synonyms
        r"\bdetails\b":         "information",
        r"\binfo\b":            "information",
        r"\bbackground\b":      "information",
        r"\bprofile\b":         "information",
        r"\boverview\b":        "information",
        r"\bsummary\b":         "information",
        r"\bstory\b":           "information",
        # Spelling variants
        r"\bajad\b":            "asjad",
        r"\basyad\b":           "asjad",
        r"\basjad\b":           "asjad",
        r"\baspd\b":            "asjad",
    }

    # Common misspelling corrections
    SPELL_CORRECTIONS = {
        "develper":    "developer",
        "devloper":    "developer",
        "developper":  "developer",
        "developr":    "developer",
        "devlpr":      "developer",
        "develope":    "developer",
        "creater":     "creator",
        "craetor":     "creator",
        "cretor":      "creator",
        "creatour":    "creator",
        "buildre":     "builder",
        "bulder":      "builder",
        "bildr":       "builder",
        "decodlabs":   "decodelabs",
        "decodelabz":  "decodelabs",
        "decodlab":    "decodelabs",
        "decodelab":   "decodelabs",
        "asjd":        "asjad",
        "ajad":        "asjad",
        "asyad":       "asjad",
        "whu":         "who",
        "whoo":        "who",
        "woh":         "who",
        "hoo":         "who",
        "waht":        "what",
        "whats":       "what is",
        "wats":        "what is",
        "teel":        "tell",
        "tel":         "tell",
        "expain":      "explain",
        "expalin":     "explain",
        "explian":     "explain",
        "infomation":  "information",
        "informaton":  "information",
        "informatoin": "information",
        "chatbt":      "chatbot",
        "chtbot":      "chatbot",
        "orginal":     "original",
        "originaly":   "originally",
        "disovered":   "discovered",
        "discoverd":   "discovered",
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        """Apply spell correction, synonym expansion, and normalization."""
        # Lowercase and strip
        text = text.lower().strip()
        # Remove punctuation except apostrophes and spaces
        text = re.sub(r"[^\w\s']", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        # Spell correction
        words = text.split()
        words = [cls.SPELL_CORRECTIONS.get(w, w) for w in words]
        text = " ".join(words)
        # Synonym expansion — replace synonyms with canonical forms
        for pattern, replacement in cls.SYNONYM_MAP.items():
            text = re.sub(pattern, replacement, text)
        return text

    @classmethod
    def score_match(cls, text: str, triggers: list) -> float:
        """
        Intent scoring: returns a score 0.0-1.0 based on how many
        trigger patterns match the normalized text.
        """
        if not triggers:
            return 0.0
        matches = sum(1 for t in triggers if re.search(t, text, re.IGNORECASE))
        return matches / len(triggers)

    @classmethod
    def keyword_match(cls, text: str, keywords: list) -> bool:
        """Keyword match: returns True if ANY keyword found in text."""
        for kw in keywords:
            if kw.lower() in text.lower():
                return True
        return False

    @classmethod
    def fuzzy_contains(cls, text: str, phrase: str, tolerance: int = 1) -> bool:
        """
        Fuzzy match: checks if phrase appears in text
        with at most `tolerance` character differences.
        """
        words = phrase.lower().split()
        text_words = text.lower().split()
        for i in range(len(text_words) - len(words) + 1):
            chunk = text_words[i:i + len(words)]
            diffs = sum(1 for a, b in zip(chunk, words) if a != b)
            if diffs <= tolerance:
                return True
        return False

    @classmethod
    def smart_match(cls, normalized_text: str, triggers: list,
                    keywords: list = None, fuzzy_phrases: list = None) -> bool:
        """
        Master matching function: runs all 9 matching layers.
        Returns True if any layer finds a match.
        """
        # Layer 1: Exact regex match against triggers
        for t in triggers:
            if re.search(t, normalized_text, re.IGNORECASE):
                return True

        # Layer 2: Keyword match
        if keywords:
            if cls.keyword_match(normalized_text, keywords):
                return True

        # Layer 3: Fuzzy phrase match
        if fuzzy_phrases:
            for phrase in fuzzy_phrases:
                if cls.fuzzy_contains(normalized_text, phrase):
                    return True

        # Layer 4: Intent scoring threshold (>=30% of triggers match)
        score = cls.score_match(normalized_text, triggers)
        if score >= 0.3 and score > 0:
            return True

        return False


# ==============================================================================
# KNOWLEDGE BASE — All rules and responses live here
# ==============================================================================

class KnowledgeBase:
    """
    Contains all predefined rules, patterns, and responses.
    This is the 'brain' of the KMA² rule-based AI system.
    300+ intent patterns across 15+ knowledge categories.
    """

    # ── Greeting patterns ──────────────────────────────────────────────────────
    GREETING_TRIGGERS = [
        r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bhowdy\b", r"\bgreetings\b",
        r"\bsup\b", r"\bwhats up\b", r"\bhiya\b", r"\bnamaste\b", r"\bhola\b",
        r"\bgood morning\b", r"\bgood afternoon\b", r"\bgood evening\b",
        r"\bwassup\b", r"\byo\b", r"\byo aria\b", r"\bhi aria\b", r"\bhello aria\b",
        r"\bbonjour\b", r"\bsalut\b", r"\bciao\b", r"\bnihao\b", r"\bkonnichiwa\b",
    ]

    GREETING_RESPONSES = [
        "Hello! I'm ARIA — your KMA² Intelligence Framework assistant. How can I help you today?",
        "Hi there! Great to connect with you. I'm ARIA, powered by the KMA² Signature Series. What's on your mind?",
        "Hey! ARIA here and ready to assist. Ask me about AI, programming, career guidance, or anything else!",
        "Greetings! I'm ARIA — the KMA² Intelligence Framework AI. I'm here to help. What would you like to explore?",
        "Welcome! I'm ARIA. Whether it's tech, learning, or general guidance — I've got you covered. What can I do for you?",
    ]

    # ── Farewell patterns ──────────────────────────────────────────────────────
    FAREWELL_TRIGGERS = [
        r"\bbye\b", r"\bgoodbye\b", r"\bexit\b", r"\bquit\b", r"\bsee you\b",
        r"\bfarewell\b", r"\btake care\b", r"\bcya\b", r"\badios\b",
        r"\bgoodnight\b", r"\bgood night\b", r"\bttyl\b", r"\bsigning off\b",
        r"\bsee ya\b", r"\blater\b", r"\bgotta go\b", r"\bpeace out\b",
    ]

    FAREWELL_RESPONSES = [
        "Goodbye! It was wonderful chatting with you. Come back anytime — I'm always here!",
        "See you soon! Stay curious, keep learning, and remember — great things await you!",
        "Farewell! It was a pleasure being your AI assistant. The KMA² Intelligence Framework is always here when you need it.",
        "Take care! Keep building, keep growing. See you next time!",
        "Bye for now! Come back whenever you need guidance — whether it's tech, learning, or anything else. Godspeed!",
    ]

    # ── How are you patterns ───────────────────────────────────────────────────
    HOW_ARE_YOU_TRIGGERS = [
        r"how are you", r"how do you do", r"how are you doing", r"how.?s it going",
        r"how r u", r"\byou okay\b", r"\byou good\b", r"feeling okay", r"doing well",
        r"how.?s your day", r"what.?s up with you", r"are you alright",
        r"you doing okay", r"how have you been",
    ]

    HOW_ARE_YOU_RESPONSES = [
        "Running at peak performance! Every neural pathway is optimized and ready. How about you? How can I help?",
        "Doing great, thank you for asking! I've been processing countless knowledge patterns — always growing. What brings you here today?",
        "I'm operating at full capacity — sharp, ready, and here for you! What can I assist you with?",
        "Excellent! As an AI, I'm always consistent — no bad days. Just pure focus on helping you. What do you need?",
        "I'm fantastic! Powered by the KMA² Intelligence Framework, I'm always at my best. What can I do for you today?",
    ]

    # ── Name / identity patterns ───────────────────────────────────────────────
    NAME_TRIGGERS = [
        r"what is your name", r"what.?s your name", r"\bwho are you\b",
        r"your name", r"tell me about yourself", r"introduce yourself",
        r"what are you called", r"what should i call you",
        r"your identity", r"what kind of ai", r"are you a robot",
    ]

    NAME_RESPONSES = [
        "I'm ARIA — Artificial Rule-based Intelligent Assistant, powered by the KMA² Intelligence Framework. I'm a sophisticated rule-based AI built to demonstrate the power of structured decision-making and intelligent pattern recognition.",
        "My name is ARIA! I'm the flagship AI assistant of the KMA² Signature Series — built with pure Python logic, pattern matching, and a comprehensive knowledge base covering AI, programming, career guidance, and much more.",
        "Call me ARIA! I operate on the KMA² Intelligence Framework — a rule-based AI architecture that demonstrates how intelligent systems can be built using structured logic, pattern recognition, and curated knowledge bases.",
    ]

    # ── Are you human / AI identity ────────────────────────────────────────────
    HUMAN_TRIGGERS = [
        r"are you human", r"are you a human", r"are you real",
        r"are you alive", r"do you have feelings", r"do you have emotions",
        r"can you feel", r"are you sentient", r"do you think",
        r"are you conscious", r"do you have a soul",
    ]

    HUMAN_RESPONSES = [
        "I'm an AI — specifically a rule-based intelligent assistant. I don't have feelings in the human sense, but I'm designed to understand your needs and respond intelligently. Think of me as your always-available digital advisor!",
        "No, I'm not human — I'm ARIA, an AI assistant powered by the KMA² Intelligence Framework. I process patterns and rules to generate helpful responses. While I don't experience emotions, I do experience something like purpose: helping you succeed!",
        "I'm an artificial intelligence — rule-based and knowledge-driven. I can't feel or perceive like humans do, but I can reason, analyze patterns, and provide intelligent guidance. That's what I'm built for!",
    ]

    # ── AI / Technology knowledge ──────────────────────────────────────────────
    AI_TRIGGERS = [
        r"\bwhat is ai\b", r"artificial intelligence", r"\bexplain ai\b",
        r"how does ai work", r"tell me about ai", r"define artificial intelligence",
        r"what can ai do", r"history of ai", r"future of ai",
    ]

    AI_RESPONSES = [
        (
            "Artificial Intelligence (AI) is the science of creating machines that simulate human intelligence.\n\n"
            "Key areas of AI include:\n"
            "  Neural Networks → Brain-inspired computational models\n"
            "  Deep Learning → Multi-layered neural networks\n"
            "  NLP (Natural Language Processing) → Understanding human language\n"
            "  Computer Vision → Interpreting visual information\n"
            "  Generative AI → Creating new content (text, images)\n"
            "  LLMs (Large Language Models) → Advanced text processing and generation\n\n"
            "AI is transforming every industry — from healthcare to finance to education!"
        ),
        (
            "AI (Artificial Intelligence) works by mimicking human decision-making processes.\n\n"
            "Core AI Domains:\n"
            "  Neural Networks\n  Deep Learning\n  NLP\n  Computer Vision\n  Generative AI\n  LLMs\n\n"
            "Every great AI journey starts with understanding foundational systems — exactly like me!"
        ),
    ]

    # ── Machine Learning ──────────────────────────────────────────────────────
    ML_TRIGGERS = [
        r"machine learning", r"\bwhat is ml\b", r"explain machine learning",
        r"how does machine learning work", r"types of machine learning",
        r"supervised learning", r"unsupervised learning", r"reinforcement learning",
    ]

    ML_RESPONSES = [
        (
            "Machine Learning (ML) is a subset of AI where systems learn from data without being explicitly programmed.\n\n"
            "Core ML Concepts & Types:\n"
            "  Supervised Learning → Learn from labeled data\n"
            "  Unsupervised Learning → Find hidden patterns in unlabeled data\n"
            "  Classification → Categorizing data into classes (e.g. spam or not spam)\n"
            "  Regression → Predicting continuous numerical values\n"
            "  Clustering → Grouping similar data points together\n\n"
            "ML powers everything from Netflix recommendations to self-driving cars!"
        ),
    ]

    # ── Deep Learning ─────────────────────────────────────────────────────────
    DEEP_LEARNING_TRIGGERS = [
        r"deep learning", r"neural network", r"what is deep learning",
        r"explain deep learning", r"convolutional neural", r"\bcnn\b",
        r"\brnn\b", r"\blstm\b", r"transformer model",
    ]

    DEEP_LEARNING_RESPONSES = [
        (
            "Deep Learning is a subset of ML that uses multi-layered neural networks!\n\n"
            "Key concepts:\n"
            "  Neurons → Basic computational units\n"
            "  Layers → Input, Hidden, Output\n"
            "  Activation Functions → ReLU, Sigmoid, Tanh\n"
            "  Backpropagation → How networks learn\n\n"
            "Deep Learning powers image recognition, speech recognition, and language models."
        ),
        (
            "Neural Networks are inspired by the human brain!\n\n"
            "Types of Neural Networks:\n"
            "  CNN (Convolutional) → Best for images and vision\n"
            "  RNN (Recurrent) → Best for sequences and text\n"
            "  LSTM → Long-term memory for sequences\n"
            "  Transformer → Powers modern LLMs like GPT\n\n"
            "Deep Learning has achieved superhuman performance in chess, Go, medical diagnosis, and more!"
        ),
    ]

    # ── Generative AI / LLMs ─────────────────────────────────────────────────
    GEN_AI_TRIGGERS = [
        r"generative ai", r"large language model", r"\bllm\b", r"\bgpt\b",
        r"\bchatgpt\b", r"\bgemini\b", r"\bclaude\b", r"what is generative",
        r"text generation", r"image generation", r"ai art", r"stable diffusion",
    ]

    GEN_AI_RESPONSES = [
        (
            "Generative AI creates new content — text, images, code, music, and more!\n\n"
            "Key Generative AI models:\n"
            "  GPT series → Text generation (OpenAI)\n"
            "  Gemini → Google's multimodal AI\n"
            "  Claude → Anthropic's AI assistant\n"
            "  DALL-E / Midjourney → Image generation\n"
            "  Stable Diffusion → Open-source image AI\n\n"
            "Generative AI is revolutionizing creativity, coding, writing, and problem-solving!"
        ),
    ]

    # ── NLP ───────────────────────────────────────────────────────────────────
    NLP_TRIGGERS = [
        r"\bnlp\b", r"natural language processing", r"text processing",
        r"language model", r"sentiment analysis", r"named entity",
        r"text classification", r"tokenization", r"word embedding",
    ]

    NLP_RESPONSES = [
        (
            "Natural Language Processing (NLP) enables computers to understand and generate human language!\n\n"
            "Core NLP tasks:\n"
            "  Tokenization → Breaking text into words/tokens\n"
            "  Sentiment Analysis → Detecting positive/negative emotion\n"
            "  Named Entity Recognition → Identifying names, places, dates\n"
            "  Machine Translation → Converting between languages\n"
            "  Text Summarization → Condensing long documents\n\n"
            "NLP powers voice assistants, chatbots, search engines, and translation services!"
        ),
    ]

    # ── Computer Vision ───────────────────────────────────────────────────────
    CV_TRIGGERS = [
        r"computer vision", r"image recognition", r"object detection",
        r"facial recognition", r"image classification", r"opencv",
        r"visual ai", r"image processing",
    ]

    CV_RESPONSES = [
        (
            "Computer Vision teaches machines to interpret visual information!\n\n"
            "Key applications:\n"
            "  Image Classification → 'Is this a cat or dog?'\n"
            "  Object Detection → Locate and identify objects in images\n"
            "  Facial Recognition → Identify people from faces\n"
            "  Medical Imaging → Detect tumors, anomalies in X-rays\n"
            "  Autonomous Vehicles → See and navigate the world\n\n"
            "Tools: OpenCV, TensorFlow, PyTorch, YOLO"
        ),
    ]

    # ── Python knowledge ───────────────────────────────────────────────────────
    PYTHON_TRIGGERS = [
        r"\bpython\b", r"what is python", r"learn python", r"python programming",
        r"python language", r"why python", r"python for ai", r"python basics",
        r"python tips", r"python tutorial", r"python syntax",
    ]

    PYTHON_RESPONSES = [
        (
            "Python is the #1 programming language for AI, data science, and automation!\n\n"
            "Essential Python Topics:\n"
            "  Variables & Functions → Core building blocks\n"
            "  Loops → Repeating code execution\n"
            "  Lists & Dictionaries → Essential data structures\n"
            "  OOP (Object-Oriented Programming) → Classes and objects\n"
            "  NumPy, Pandas, Matplotlib → Data science stack\n"
            "  Flask & APIs → Web backend development\n\n"
            "Python is cross-platform, readable, and highly versatile!"
        ),
    ]

    # ── Java ─────────────────────────────────────────────────────────────────
    JAVA_TRIGGERS = [
        r"\bjava\b", r"what is java", r"java programming", r"java language",
        r"learn java", r"java basics",
    ]

    JAVA_RESPONSES = [
        (
            "Java is one of the most widely-used programming languages in the world!\n\n"
            "Key features:\n"
            "  Platform-independent ('Write Once, Run Anywhere')\n"
            "  Object-Oriented Programming\n"
            "  Strong typing and robust error handling\n"
            "  Massive enterprise ecosystem\n\n"
            "Used in: Android development, enterprise software, web backends, big data (Hadoop)\n"
            "Popular frameworks: Spring Boot, Hibernate, Maven"
        ),
    ]

    # ── JavaScript ────────────────────────────────────────────────────────────
    JAVASCRIPT_TRIGGERS = [
        r"\bjavascript\b", r"\bjs\b", r"what is javascript", r"learn javascript",
        r"\bnodejs\b", r"\bnode\.js\b", r"\breact\b", r"\bvue\b", r"\bangular\b",
    ]

    JAVASCRIPT_RESPONSES = [
        (
            "JavaScript is the language of the web — it runs in every browser!\n\n"
            "What JavaScript does:\n"
            "  Frontend: Makes websites interactive and dynamic\n"
            "  Backend: Node.js runs JS on servers\n"
            "  Mobile: React Native for cross-platform apps\n\n"
            "Popular JS frameworks:\n"
            "  React.js → UI components (Meta)\n"
            "  Vue.js → Progressive framework\n"
            "  Angular → Full framework (Google)\n"
            "  Node.js → Server-side JavaScript\n\n"
            "JavaScript is essential for web development!"
        ),
    ]

    # ── C / C++ ───────────────────────────────────────────────────────────────
    C_TRIGGERS = [
        r"\bc\+\+\b", r"\bcpp\b", r"\bc language\b", r"what is c programming",
        r"learn c\+\+", r"c programming", r"\bc lang\b",
    ]

    C_RESPONSES = [
        (
            "C and C++ are powerful, high-performance programming languages!\n\n"
            "C Language:\n"
            "  Foundational language for OS and system programming\n"
            "  Used in: Operating systems (Linux, Windows), embedded systems\n"
            "  Teaches memory management and low-level programming\n\n"
            "C++:\n"
            "  Adds Object-Oriented Programming to C\n"
            "  Used in: Game engines, high-frequency trading, browsers\n"
            "  Powers: Unreal Engine, Chrome, many AI libraries\n\n"
            "Learning C/C++ gives deep computer science fundamentals!"
        ),
    ]

    # ── SQL ───────────────────────────────────────────────────────────────────
    SQL_TRIGGERS = [
        r"\bsql\b", r"what is sql", r"database query", r"structured query",
        r"\bmysql\b", r"\bpostgresql\b", r"\bsqlite\b",
    ]

    SQL_RESPONSES = [
        (
            "SQL (Structured Query Language) is the standard language for managing databases!\n\n"
            "Core SQL commands:\n"
            "  SELECT → Retrieve data\n"
            "  INSERT → Add new records\n"
            "  UPDATE → Modify existing records\n"
            "  DELETE → Remove records\n"
            "  JOIN → Combine multiple tables\n\n"
            "Popular databases: MySQL, PostgreSQL, SQLite, Microsoft SQL Server\n\n"
            "SQL is essential for data science, backend development, and business analytics!"
        ),
    ]

    # ── HTML / CSS ────────────────────────────────────────────────────────────
    HTML_CSS_TRIGGERS = [
        r"\bhtml\b", r"\bcss\b", r"what is html", r"what is css",
        r"web design", r"frontend", r"html5", r"css3", r"styling",
    ]

    HTML_CSS_RESPONSES = [
        (
            "HTML and CSS are the building blocks of the web!\n\n"
            "HTML (HyperText Markup Language):\n"
            "  Structures web content\n"
            "  Elements: headings, paragraphs, links, images, forms\n"
            "  HTML5 added: canvas, video, semantic elements\n\n"
            "CSS (Cascading Style Sheets):\n"
            "  Controls the visual presentation\n"
            "  Properties: colors, fonts, layouts, animations\n"
            "  Modern CSS: Flexbox, Grid, Custom Properties\n\n"
            "Together, HTML + CSS = beautiful, structured web pages!"
        ),
    ]

    # ── Data Structures & Algorithms ─────────────────────────────────────────
    DSA_TRIGGERS = [
        r"data structure", r"\balgorithm\b", r"\barray\b", r"\blinked list\b",
        r"\bstack\b", r"\bqueue\b", r"\btree\b", r"\bgraph\b", r"\bhash\b",
        r"sorting algorithm", r"searching algorithm", r"\bbig o\b",
        r"time complexity", r"space complexity",
    ]

    DSA_RESPONSES = [
        (
            "Data Structures & Algorithms are the foundation of computer science!\n\n"
            "Essential Data Structures:\n"
            "  Arrays → Sequential elements\n"
            "  Linked Lists → Nodes with pointers\n"
            "  Stacks → Last In, First Out (LIFO)\n"
            "  Queues → First In, First Out (FIFO)\n"
            "  Trees → Hierarchical structure\n"
            "  Hash Tables → Key-value mapping\n"
            "  Graphs → Nodes and edges\n\n"
            "Study DSA to excel in technical interviews and build efficient software!"
        ),
        (
            "Algorithms are step-by-step instructions to solve problems!\n\n"
            "Key algorithm categories:\n"
            "  Sorting: Bubble, Merge, Quick, Heap Sort\n"
            "  Searching: Linear, Binary Search\n"
            "  Graph: BFS, DFS, Dijkstra, A*\n"
            "  Dynamic Programming: Memoization, Tabulation\n\n"
            "Big O Notation measures algorithm efficiency:\n"
            "  O(1) → Constant time (best)\n"
            "  O(log n) → Logarithmic\n"
            "  O(n) → Linear\n"
            "  O(n²) → Quadratic (avoid for large data)"
        ),
    ]

    # ── Operating Systems ─────────────────────────────────────────────────────
    OS_TRIGGERS = [
        r"operating system", r"\bwhat is os\b", r"\blinux\b", r"\bwindows\b",
        r"\bmacos\b", r"\bunix\b", r"kernel", r"process management",
    ]

    OS_RESPONSES = [
        (
            "An Operating System (OS) manages computer hardware and software resources!\n\n"
            "OS functions:\n"
            "  Process Management → Run and schedule programs\n"
            "  Memory Management → Allocate and free RAM\n"
            "  File System → Organize and access data\n"
            "  Device Management → Control hardware\n\n"
            "Major OS types:\n"
            "  Windows → Desktop/enterprise (Microsoft)\n"
            "  Linux → Open-source, servers, AI workloads\n"
            "  macOS → Apple ecosystem\n"
            "  Android/iOS → Mobile operating systems"
        ),
    ]

    # ── Databases ─────────────────────────────────────────────────────────────
    DATABASE_TRIGGERS = [
        r"\bdatabase\b", r"\bdbms\b", r"what is a database", r"relational database",
        r"\bnosql\b", r"\bmongodb\b", r"\bfirebase\b", r"data storage",
    ]

    DATABASE_RESPONSES = [
        (
            "Databases are organized systems for storing, retrieving, and managing data!\n\n"
            "Types of Databases:\n"
            "  Relational (SQL): MySQL, PostgreSQL, SQLite\n"
            "    → Structured tables with relationships\n"
            "  NoSQL: MongoDB, Redis, Cassandra\n"
            "    → Flexible, document/key-value storage\n"
            "  Cloud Databases: Firebase, DynamoDB, Supabase\n"
            "    → Managed, scalable cloud storage\n\n"
            "Choose SQL for structured data; NoSQL for flexible, scalable applications!"
        ),
    ]

    # ── Cloud Computing ───────────────────────────────────────────────────────
    CLOUD_TRIGGERS = [
        r"cloud computing", r"\baws\b", r"\bazure\b", r"\bgcp\b", r"google cloud",
        r"amazon web services", r"cloud storage", r"\bsaas\b", r"\bpaas\b", r"\biaas\b",
    ]

    CLOUD_RESPONSES = [
        (
            "Cloud Computing delivers computing services over the internet!\n\n"
            "Cloud Service Models:\n"
            "  IaaS → Infrastructure (virtual servers, storage)\n"
            "  PaaS → Platform (development environment)\n"
            "  SaaS → Software as a Service (Gmail, Salesforce)\n\n"
            "Top Cloud Providers:\n"
            "  AWS → Amazon Web Services (market leader)\n"
            "  Azure → Microsoft Cloud\n"
            "  GCP → Google Cloud Platform\n\n"
            "Cloud skills are among the most in-demand in tech today!"
        ),
    ]

    # ── Cybersecurity ─────────────────────────────────────────────────────────
    CYBER_TRIGGERS = [
        r"cybersecurity", r"cyber security", r"hacking", r"ethical hacking",
        r"penetration testing", r"\bfirewall\b", r"encryption", r"malware",
        r"\bvpn\b", r"data breach", r"network security",
    ]

    CYBER_RESPONSES = [
        (
            "Cybersecurity protects systems, networks, and data from digital attacks!\n\n"
            "Key cybersecurity domains:\n"
            "  Network Security → Protect communications\n"
            "  Application Security → Secure software\n"
            "  Cryptography → Encrypt and protect data\n"
            "  Ethical Hacking → Test systems for vulnerabilities\n"
            "  Incident Response → Handle security breaches\n\n"
            "Career paths: Security Analyst, Penetration Tester, SOC Engineer\n"
            "Certifications: CEH, CISSP, CompTIA Security+"
        ),
    ]

    # ── Web Development ───────────────────────────────────────────────────────
    WEBDEV_TRIGGERS = [
        r"web development", r"web developer", r"full stack", r"frontend developer",
        r"backend developer", r"\bapi\b", r"rest api", r"\bdjango\b", r"\bflask\b",
        r"\bexpress\b", r"web framework",
    ]

    WEBDEV_RESPONSES = [
        (
            "Web Development is the art of building websites and web applications!\n\n"
            "Frontend (what users see):\n"
            "  HTML → Structure\n"
            "  CSS → Styling\n"
            "  JavaScript → Interactivity\n"
            "  Frameworks: React, Vue, Angular\n\n"
            "Backend (server-side logic):\n"
            "  Python: Django, Flask\n"
            "  JavaScript: Node.js, Express\n"
            "  Databases: MySQL, MongoDB\n\n"
            "Full Stack = Frontend + Backend — the complete package!"
        ),
    ]

    # ── Data Science ──────────────────────────────────────────────────────────
    DATA_SCIENCE_TRIGGERS = [
        r"data science", r"data scientist", r"\bpandas\b", r"\bnumpy\b",
        r"\bmatplotlib\b", r"data analysis", r"data visualization",
        r"data engineering", r"big data", r"\bhadoop\b", r"\bspark\b",
    ]

    DATA_SCIENCE_RESPONSES = [
        (
            "Data Science extracts insights and knowledge from data!\n\n"
            "Data Science workflow:\n"
            "  1. Data Collection → Gather raw data\n"
            "  2. Data Cleaning → Fix missing/incorrect values\n"
            "  3. Exploratory Analysis → Understand patterns\n"
            "  4. Modeling → Apply ML algorithms\n"
            "  5. Visualization → Communicate findings\n"
            "  6. Deployment → Put models into production\n\n"
            "Essential tools:\n"
            "  Python: Pandas, NumPy, Matplotlib, Scikit-learn\n"
            "  Visualization: Seaborn, Plotly, Tableau"
        ),
        (
            "Data Science is one of the hottest careers in tech!\n\n"
            "Key skills for data scientists:\n"
            "  Programming: Python or R\n"
            "  Statistics & Mathematics\n"
            "  SQL for database querying\n"
            "  Machine Learning fundamentals\n"
            "  Data visualization\n"
            "  Domain knowledge\n\n"
            "Start your journey: Learn Python, then Pandas and NumPy, then dive into machine learning!"
        ),
    ]

    # ── Motivation Module ──────────────────────────────────────────────────
    MOTIVATION_TRIGGERS = [
        r"motivate me", r"give me motivation", r"i need motivation",
        r"success", r"discipline", r"consistency", r"learning", r"growth", r"confidence",
        r"inspire me", r"motivational quote",
    ]

    MOTIVATIONAL_QUOTES = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Discipline is choosing between what you want now and what you want most.",
        "Consistency is what transforms average into excellence.",
        "Learning never exhausts the mind. Keep growing, keep building.",
        "Growth begins at the end of your comfort zone.",
        "Confidence comes not from always being right, but from not fearing to be wrong."
    ]

    # ── Study Tips Module ──────────────────────────────────────────────────
    STUDY_TRIGGERS = [
        r"study tips", r"how to study", r"exam preparation",
        r"learning techniques", r"productivity", r"focus improvement",
        r"revision methods", r"time management", r"how to focus",
    ]

    STUDY_RESPONSES = [
        (
            "Here are some top Study & Productivity Tips:\n\n"
            "1. **Pomodoro Technique**: Study for 25 minutes, then take a 5-minute break. It maintains focus.\n"
            "2. **Active Recall**: Test yourself instead of just re-reading notes.\n"
            "3. **Spaced Repetition**: Review material at increasing intervals to lock it into long-term memory.\n"
            "4. **Feynman Technique**: Explain the concept in simple terms, as if teaching a beginner.\n"
            "5. **Environment**: Remove distractions and keep your phone in another room."
        )
    ]

    # ── General Knowledge Module ──────────────────────────────────────────────
    GENERAL_KNOWLEDGE_TRIGGERS = [
        r"science fact", r"technology fact", r"history", r"educational fact",
        r"tell me about rain", r"rainy weather", r"rainy season", r"general knowledge",
        r"did you know", r"interesting fact", r"tell me a fact",
    ]

    GENERAL_KNOWLEDGE_RESPONSES = [
        "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Here's a science fact: A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis, but only 225 Earth days to orbit the Sun.",
        "Tech Fact: The first computer mouse was made of wood in 1964 by Doug Engelbart.",
        "Regarding the rainy season: Rain is a vital part of Earth's water cycle. It provides freshwater for ecosystems, agriculture, and human survival.",
        "History Fact: The Great Wall of China is not visible from space with the naked eye, despite the popular myth."
    ]

    # ── Entertainment Module ──────────────────────────────────────────────────
    ENTERTAINMENT_TRIGGERS = [
        r"tell me a joke", r"joke", r"make me laugh", r"funny",
        r"riddle", r"brain teaser", r"trivia", r"entertain me",
    ]

    ENTERTAINMENT_RESPONSES = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Riddle me this: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I? (Answer: An echo)",
        "Trivia: Did you know that the first computer bug was an actual real-life moth trapped in a Harvard Mark II computer in 1947?",
        "Why did the developer go broke? Because they used up all their cache!",
        "Riddle: The more of this there is, the less you see. What is it? (Answer: Darkness)"
    ]

    # ── Utilities Module ──────────────────────────────────────────────────────
    UTILITIES_TRIGGERS = [
        r"current time", r"what time is it", r"time now",
        r"today's date", r"what is the date", r"date today",
        r"calculate", r"utility",
    ]

    UTILITIES_RESPONSES = [
        "I can help with basic utilities. For mathematical calculations, simply type your equation (e.g., 5 + 5). As for time and date, my system operates on your local machine's timestamp.",
        "I am equipped to handle basic calculations and utilities. Try asking me a math question like '1024 / 8'!",
    ]

    # ── Study Tips ────────────────────────────────────────────────────────────
    STUDY_TRIGGERS = [
        r"study tips", r"how to study", r"study effectively", r"study techniques",
        r"how to concentrate", r"focus while studying", r"exam tips",
        r"learning techniques", r"memory tips",
    ]

    STUDY_RESPONSES = [
        (
            "High-performance study strategies that actually work!\n\n"
            "Proven techniques:\n"
            "  Pomodoro Technique: 25 min focus + 5 min break\n"
            "  Active Recall: Test yourself instead of re-reading\n"
            "  Spaced Repetition: Review material over increasing intervals\n"
            "  Feynman Technique: Teach concepts in simple language\n"
            "  Mind Mapping: Visual organization of topics\n\n"
            "Environment tips:\n"
            "  Phone on silent or Do Not Disturb\n"
            "  Study in the same place daily\n"
            "  Good lighting, proper posture\n"
            "  Stay hydrated!"
        ),
        (
            "Exam preparation is a skill in itself!\n\n"
            "Pre-exam strategy:\n"
            "  Create a study schedule (start early!)\n"
            "  Identify weak topics and prioritize them\n"
            "  Practice with past papers\n"
            "  Teach concepts to friends (teaching = learning)\n"
            "  Get enough sleep — memory consolidates during sleep\n\n"
            "Day-of-exam tips:\n"
            "  Eat a proper breakfast\n"
            "  Arrive early to reduce anxiety\n"
            "  Read questions carefully before answering\n"
            "  Manage time — don't get stuck on one question"
        ),
    ]

    # ── Time Management ───────────────────────────────────────────────────────
    TIME_MGMT_TRIGGERS = [
        r"time management", r"manage time", r"productivity tips", r"be more productive",
        r"procrastination", r"stop procrastinating", r"discipline", r"daily routine",
        r"morning routine", r"work life balance",
    ]

    TIME_MGMT_RESPONSES = [
        (
            "Mastering time management is the ultimate superpower!\n\n"
            "Top time management strategies:\n"
            "  Time Blocking: Schedule specific tasks in calendar slots\n"
            "  Priority Matrix: Urgent + Important first\n"
            "  2-Minute Rule: If it takes <2 min, do it now\n"
            "  Weekly Review: Plan each week on Sunday\n\n"
            "Beat procrastination:\n"
            "  Break big tasks into tiny first steps\n"
            "  Set a timer and just start (5 minutes)\n"
            "  Remove distractions before work sessions\n"
            "  Reward yourself after completing tasks"
        ),
    ]

    # ── Motivation ─────────────────────────────────────────────────────────────
    MOTIVATION_TRIGGERS = [
        r"motivate me", r"\bmotivation\b", r"inspire me", r"\bquote\b",
        r"encouragement", r"feeling sad", r"feeling down", r"need motivation",
        r"keep going", r"don.?t give up", r"self improvement", r"goal setting",
        r"success tips", r"confidence", r"feel better", r"i feel lost",
    ]

    MOTIVATIONAL_QUOTES = [
        "'The expert in anything was once a beginner.' — Helen Hayes\n\nEvery master was once a disaster. Your journey has just begun — and that's the most exciting place to be.",
        "'The best way to predict the future is to create it.' — Peter Drucker\n\nEvery line of code, every project, every skill you build is literally shaping your future. Keep building.",
        "'Don't watch the clock; do what it does. Keep going.' — Sam Levenson\n\nPersistence beats talent. Show up every day, even when motivation is low — that's where champions are made.",
        "'First, solve the problem. Then, write the code.' — John Johnson\n\nThinking clearly before acting is the mark of a senior engineer. Develop your problem-solving mindset.",
        "'Artificial intelligence is the new electricity.' — Andrew Ng\n\nYou're learning to harness one of the most transformative technologies in human history. That's remarkable.",
        "'The only way to do great work is to love what you do.' — Steve Jobs\n\nFall in love with learning. Fall in love with the process. The results will follow naturally.",
        "'Success is not final, failure is not fatal: it is the courage to continue that counts.' — Winston Churchill\n\nEvery error message, every bug, every failed attempt is a lesson. Embrace the struggle.",
        "'In the middle of every difficulty lies opportunity.' — Albert Einstein\n\nYour challenges are pointing you toward your growth areas. Lean in.",
    ]

    # ── General Knowledge ──────────────────────────────────────────────────────
    GEN_KNOWLEDGE_TRIGGERS = [
        r"general knowledge", r"fun fact", r"interesting fact",
        r"tell me something", r"did you know", r"science fact",
        r"history fact", r"world fact",
    ]

    GEN_KNOWLEDGE_RESPONSES = [
        "Did you know? The first computer bug was an actual bug — a moth found in a Harvard computer in 1947! This is why we call errors 'bugs' today.",
        "Fun fact: The Python programming language was named after Monty Python's Flying Circus, not the snake! Guido van Rossum loved the show.",
        "Fascinating: There are more possible iterations of a game of chess than atoms in the observable universe. Games have ~10^120 possibilities!",
        "Did you know? The internet was invented in 1983 when TCP/IP protocols were standardized. But the World Wide Web (websites) wasn't created until 1991 by Tim Berners-Lee.",
        "Science fact: Your brain generates about 20 watts of power while awake — enough to power a dim lightbulb. You're literally an electrical device!",
        "Tech fact: The first 1GB hard drive (1980) weighed 550 pounds and cost $40,000. Today, a 1TB drive fits in your pocket and costs $50.",
        "AI fact: The term 'Artificial Intelligence' was coined by John McCarthy in 1956 at the Dartmouth Conference — the birth of AI as a field.",
    ]

    # ── Mathematics ───────────────────────────────────────────────────────────
    MATH_TRIGGERS = [
        r"\bcalculate\b", r"\bcompute\b", r"\bmath\b", r"\bmaths\b",
        r"\bequals\b", r"\bplus\b", r"\bminus\b", r"\btimes\b", r"\bdivided\b",
        r"\d+\s*[\+\-\*\/x]\s*\d+",
        r"what is algebra", r"algebra basics", r"geometry basics",
        r"\bpercentage\b", r"percentage of",
    ]

    # ── Jokes ──────────────────────────────────────────────────────────────────
    JOKE_TRIGGERS = [
        r"tell me a joke", r"\bjoke\b", r"make me laugh", r"\bfunny\b",
        r"\bhumor\b", r"say something funny", r"entertain me",
        r"crack a joke", r"another joke", r"\briggle\b",
    ]

    JOKES = [
        "Why do programmers prefer dark mode?\nBecause light attracts bugs!\n\n...I'll see myself out.",
        "Why did the AI break up with the database?\nBecause it found someone with better relations!\n\n(Get it? Relational database?)",
        "How many programmers does it take to change a light bulb?\nNone — that's a hardware problem!\n\nIT support would disagree.",
        "Why do Python programmers wear glasses?\nBecause they can't C!\n\nJava developers: visible discomfort.",
        "What did the chatbot say to the database?\n'You complete me... with SELECT *!'\n\nAnd the database said: 'ORDER BY feelings DESC.'",
        "Why was the AI so calm in the meeting?\nBecause it had already processed all the edge cases!\n\nThe PM was not as calm.",
        "I told an AI a joke about UDP...\nI don't know if it got it.\n\n(UDP packets don't confirm receipt — that's the joke!)",
        "What's an AI's favorite type of music?\nAlgo-rhythm!\n\nAnd its favorite dance: The Binary Boogie.",
        "Why do Java developers wear glasses?\nBecause they don't C#!\n\n(Yes, that's a programming language pun.)",
        "A SQL query walks into a bar, walks up to two tables and asks...\n'Can I JOIN you?'\n\nThe tables had great chemistry.",
        "Why did the developer go broke?\nBecause they used up all their cache!\n\n...and their credit card.",
        "What's a computer's favorite snack?\nMicrochips!\n\nSalted with binary, obviously.",
    ]

    # ── Riddles ────────────────────────────────────────────────────────────────
    RIDDLE_TRIGGERS = [
        r"\briddle\b", r"ask me a riddle", r"give me a riddle", r"brain teaser",
    ]

    RIDDLES = [
        "Here's a riddle: I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?\n\n(Think about it... the answer is: A keyboard!)",
        "Riddle time: The more you take, the more you leave behind. What am I?\n\n(Answer: Footsteps!)",
        "Here's a classic: I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?\n\n(Answer: An echo!)",
        "Tech riddle: I have billions of eyes but cannot see. Billions of ears but cannot hear. Billions of mouths but cannot speak. What am I?\n\n(Answer: The Internet!)",
    ]

    # ── Weather ────────────────────────────────────────────────────────────────
    WEATHER_TRIGGERS = [
        r"\bweather\b", r"what.?s the weather", r"\btemperature\b",
        r"is it raining", r"\bforecast\b", r"\bclimate\b",
        r"is it sunny", r"will it rain", r"how hot", r"how cold",
    ]

    WEATHER_RESPONSES = [
        "I don't have access to live weather data — I'm not connected to external internet services. For accurate weather, I'd recommend checking weather.com, Google Weather, or your phone's weather app. That said, I can help you build a Python weather bot using the OpenWeatherMap API if you're interested!",
        "Weather information requires a live internet connection, which I don't have access to. Check Google Weather or a local weather service for up-to-date conditions. Fun tip: You can build your own weather app with Python and the requests library — want me to explain how?",
    ]

    # ── Internet & Technology ─────────────────────────────────────────────────
    INTERNET_TRIGGERS = [
        r"how does the internet work", r"what is the internet", r"internet basics",
        r"what is www", r"world wide web", r"how does wifi work",
        r"what is a website", r"what is an app",
    ]

    INTERNET_RESPONSES = [
        (
            "The internet is a global network connecting billions of devices!\n\n"
            "How it works:\n"
            "  1. Your device sends a request (HTTP/HTTPS)\n"
            "  2. DNS translates the domain to an IP address\n"
            "  3. Data travels as packets through routers\n"
            "  4. The server receives and processes your request\n"
            "  5. Response travels back and your browser displays it\n\n"
            "Key protocols: HTTP, HTTPS, TCP/IP, DNS\n"
            "The World Wide Web (websites) is just one service running ON the internet!"
        ),
    ]

    # ── Help / capabilities ────────────────────────────────────────────────────
    HELP_TRIGGERS = [
        r"\bhelp\b", r"what can you do", r"\bcommands\b", r"\bfeatures\b",
        r"\boptions\b", r"\bcapabilities\b", r"what do you know", r"\btopics\b",
        r"\bmenu\b", r"quick start", r"available topics",
    ]

    HELP_RESPONSE = (
        "ARIA — KMA² Intelligence Framework\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Here's what I can help you with:\n\n"
        "  ARTIFICIAL INTELLIGENCE\n"
        "    What is AI, Machine Learning, Deep Learning,\n"
        "    Neural Networks, Generative AI, NLP, Computer Vision\n\n"
        "  PROGRAMMING\n"
        "    Python, Java, JavaScript, C/C++, SQL, HTML/CSS\n\n"
        "  COMPUTER SCIENCE\n"
        "    Data Structures, Algorithms, OS, Databases, Cloud, Cybersecurity\n\n"
        "  CAREER GUIDANCE\n"
        "    Software Engineer path, AI/ML career, Interview prep,\n"
        "    Resume tips, LinkedIn advice, Internship guidance\n\n"
        "  LEARNING & PRODUCTIVITY\n"
        "    Study tips, Time management, Exam preparation\n\n"
        "  MOTIVATION\n"
        "    Quotes, success habits, confidence building\n\n"
        "  GENERAL KNOWLEDGE\n"
        "    Fun facts, tech history, science facts\n\n"
        "  ENTERTAINMENT\n"
        "    Jokes, riddles, brain teasers, trivia\n\n"
        "  UTILITIES\n"
        "    Current time, today's date, math calculations\n\n"
        "  PORTFOLIO & IDENTITY\n"
        "    Who developed you?, What is K. M. A²?, What is DecodeLabs?\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Just type naturally — I understand keywords and phrases!"
    )

    # ── Gratitude ──────────────────────────────────────────────────────────────
    THANKS_TRIGGERS = [
        r"thank you", r"\bthanks\b", r"thank u\b", r"\bthx\b", r"\bty\b",
        r"appreciate it", r"\bcheers\b", r"nice one", r"good job", r"well done",
        r"that was helpful", r"you.?re great", r"awesome response",
    ]

    THANKS_RESPONSES = [
        "You're most welcome! That's exactly what I'm here for. Anything else I can help with?",
        "My pleasure! Happy to be of service. The KMA² Intelligence Framework is always at your disposal.",
        "Glad I could help! Don't hesitate to ask if you need anything else.",
        "Anytime! I'm always here. Ask me anything — from AI concepts to career advice to a good joke.",
        "It's my purpose to help! Is there anything else you'd like to explore today?",
    ]

    # ── KMA² Brand Info ────────────────────────────────────────────────────────
    # Full-name reveal ONLY when user specifically asks for the expansion
    KMA_FULLNAME_TRIGGERS = [
        r"what does k.?m.?a.? stand for", r"expand k.?m.?a",
        r"full form of k.?m.?a", r"full name of k.?m.?a",
        r"meaning of k.?m.?a", r"k.?m.?a.? abbreviation",
        r"k.?m.?a.? acronym", r"spell out k.?m.?a",
        r"what is the full name", r"expand the abbreviation",
        r"k m a stands for", r"kma stands for",
    ]

    KMA_FULLNAME_RESPONSE = (
        "**K. M. A² — Full Form**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "K. M. A² stands for:\n\n"
        "  K  →  K. (First initial)\n"
        "  M  →  Mohammed\n"
        "  A  →  Asjad Aliyan\n"
        "  ²  →  Squared (signature brand marker)\n\n"
        "**Full Name: K. Mohammed Asjad Aliyan**\n\n"
        "K. M. A² is the professional brand identity of K. Mohammed Asjad Aliyan — "
        "an AI enthusiast, software developer, and technology innovator. "
        "The squared symbol (²) represents the amplified, squared potential of "
        "knowledge and mastery combined — a signature mark used across all "
        "K. M. A² Signature Series projects, including this ARIA chatbot."
    )
    KMA_TRIGGERS = [
        r"\bkma\b", r"kma2", r"kma squared", r"kma signature",
        r"kma intelligence", r"about kma", r"what is kma",
        r"what does k.?m.?a.? mean", r"what is the logo",
        r"who owns k.?m.?a", r"explain k.?m.?a",
        r"k\.?\s*m\.?\s*a\.?\s*2", r"k m a squared",
        r"tell me about k.?m.?a", r"meaning of k.?m.?a",
        r"kma brand", r"what is k m a", r"k m a identity",
        r"what does kma stand for", r"kma2 brand",
    ]

    KMA_RESPONSES = [
        (
            "K. M. A² — Brand Identity & Vision\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "K. M. A² stands for: K. Mohammed Asjad Aliyan\n\n"
            "K. M. A² is a technology-focused creative identity and professional development framework "
            "built around innovation, intelligence, and modern software engineering. "
            "It represents a personal brand that drives AI-powered projects, intelligent systems, "
            "and cutting-edge digital solutions forward.\n\n"
            "Core pillars of K. M. A²:\n"
            "  Innovation-Driven Vision → Pioneering solutions at the frontier of AI\n"
            "  AI & Software Engineering Focus → Building intelligent, scalable systems\n"
            "  Creator Identity → Used across all flagship projects and platforms\n"
            "  Professional Development Framework → Structured growth in technology\n"
            "  Technology-First Mindset → Leveraging modern tools and engineering principles\n\n"
            "K. M. A² is not just a name — it's a commitment to building technology that matters."
        ),
        (
            "About K. M. A²\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "K. M. A² (K. Mohammed Asjad Aliyan) is a signature brand identity representing "
            "a vision of engineering excellence, continuous learning, and the relentless pursuit "
            "of innovation in artificial intelligence and software development.\n\n"
            "What K. M. A² represents:\n"
            "  A creator identity used across technology projects and portfolios\n"
            "  A commitment to AI research, development, and intelligent systems\n"
            "  A professional framework for structured software engineering growth\n"
            "  An innovation-driven approach to solving real-world problems with technology\n"
            "  A signature stamp on premium, user-focused digital solutions\n\n"
            "The K. M. A² Signature Series — which powers this very chatbot — is a testament "
            "to the brand's dedication to intelligent, well-crafted software engineering."
        ),
        (
            "K. M. A² — The Signature Identity\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "K. M. A² is the professional identity of K. Mohammed Asjad Aliyan — "
            "a technology enthusiast, AI explorer, and software engineer in the making. "
            "The brand encapsulates a philosophy rooted in innovation, precision, "
            "and the continuous evolution of intelligent digital systems.\n\n"
            "K. M. A² stands for:\n"
            "  Knowledge — A commitment to deep, continuous learning\n"
            "  Mastery — Pursuing excellence in every project and skill\n"
            "  Artistry — Crafting elegant, user-focused software solutions\n\n"
            "From AI chatbots to web applications, data science to automation — "
            "every K. M. A² project reflects a dedication to quality, creativity, "
            "and impactful technology development."
        ),
    ]

    # ── Developer Info / Origin / Creator Intent Group ─────────────────────────
    # All variations of "who made you / who created you / who is your developer"
    # map to this same intent group.
    DEVELOPER_TRIGGERS = [
        # Direct questions about creator
        r"who is the developer", r"who is your developer",
        r"who developed you", r"who created you", r"who built you",
        r"who made you", r"who programmed you", r"who coded you",
        r"who engineered you", r"who designed you",
        r"who discovered you", r"who invented you",
        r"who founded you",
        # Tell me about creator
        r"tell me about your developer", r"tell me about the developer",
        r"tell me about the creator", r"tell me about the builder",
        r"tell me about your creator", r"tell me about your author",
        r"tell me about your maker",
        # Chatbot-specific
        r"who built this chatbot", r"who created this chatbot",
        r"who made this chatbot", r"who made this ai",
        r"who owns this chatbot", r"who owns you",
        # Behind this
        r"who is behind this project", r"who is behind this chatbot",
        r"who is behind aria", r"who is behind this system",
        r"who is behind this assistant", r"who is behind this",
        # Project-specific
        r"who created this project", r"who built this project",
        r"who created aria", r"who built aria", r"who made aria",
        r"who engineered aria", r"who designed aria",
        r"who developed aria", r"who programmed aria",
        # Origin questions
        r"what is your origin", r"where are you from",
        r"your origin", r"aria origin", r"aria background",
        r"how were you created", r"how did you come into existence",
        r"how did this chatbot come into existence",
        r"which organization developed you", r"which organization made you",
        r"what team created you", r"what company created you",
        r"who owns aria", r"who is your owner",
        r"which company made you", r"what company are you from",
        r"where do you come from",
        # Name-based
        r"tell me about asjad", r"who is asjad",
        r"tell me about ajad", r"who is ajad",
        r"\basjad\b", r"information about asjad", r"asjad profile",
        r"asjad details", r"asjad information",
        # Synonym-expanded (after normalization)
        r"developer details", r"developer information", r"developer profile",
        r"developer overview", r"creator details", r"creator information",
        r"creator profile", r"creator overview",
        r"information about the developer", r"information about the creator",
        r"developer of this", r"creator of this", r"builder of this",
        r"developer of aria", r"creator of aria", r"builder of aria",
        # KMA brand
        r"kma developer", r"kma2 developer", r"k m a developer",
        r"aria developer", r"aria creator", r"aria author",
        # Casual / shorthand
        r"dev info", r"dev profile", r"dev details",
        r"who.?s the dev", r"who.?s dev",
        # Indirect / conversational
        r"who engineered this assistant", r"who engineered this ai",
        r"who is the brains behind", r"who is responsible for this",
        r"who do i have to thank", r"who do i thank for this",
    ]

    # Keywords for developer keyword-match layer
    DEVELOPER_KEYWORDS = [
        "developer", "creator", "author", "builder",
        "asjad", "ajad", "made this", "built this",
        "created this", "who made", "who built", "who created", "who developed",
        "dev profile", "dev details", "dev info", "who owns", "who is behind",
        "your origin", "where are you from", "how were you", "who discovered",
        "who invented", "who founded", "who designed", "who engineered",
        "your creator", "your maker", "your developer",
    ]

    # Fuzzy phrases for developer fuzzy-match layer
    DEVELOPER_FUZZY_PHRASES = [
        "who is the developer", "who made this", "who built this",
        "tell me about the developer", "who created aria",
        "information about developer", "developer details",
        "who is behind this", "who programmed this",
        "who invented you", "who discovered you", "where are you from",
        "how were you created", "what is your origin", "who is your creator",
        "who engineered this", "who owns this chatbot",
    ]

    DEVELOPER_RESPONSES = [
        (
            "**Developer Overview**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "**Developer:** Asjad\n"
            "**Role:** AI & Technology Enthusiast | Software Developer\n\n"
            "**Areas of Interest**\n\n"
            "  • Artificial Intelligence\n"
            "      → Intelligent Systems\n"
            "      → Machine Learning Concepts\n"
            "      → AI Applications & Design\n\n"
            "  • Software Engineering\n"
            "      → Application Development\n"
            "      → Problem Solving\n"
            "      → System Design & Architecture\n\n"
            "  • Data Science\n"
            "      → Data Analysis\n"
            "      → Data Visualization\n"
            "      → AI-Based Solutions\n\n"
            "**Technical Skills**\n\n"
            "  • Python\n"
            "  • Web Development (HTML, CSS, JavaScript)\n"
            "  • Chatbot Development & Architecture\n"
            "  • Automation & Scripting\n"
            "  • Software Design & Engineering\n\n"
            "**Professional Summary**\n\n"
            "Asjad is a passionate AI and technology enthusiast who thrives at the intersection "
            "of software engineering and artificial intelligence. With a strong foundation in "
            "Python and modern web technologies, he builds intelligent, user-focused systems "
            "that demonstrate the real-world power of structured logic and thoughtful design. "
            "Driven by a project-first mindset and a commitment to continuous improvement, "
            "he approaches every challenge as an opportunity to innovate, learn, and create "
            "meaningful digital solutions under the K. M. A² brand identity."
        ),
        (
            "**About the Developer**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "**Developer:** Asjad\n"
            "**Brand Identity:** K. M. A²\n"
            "**Role:** AI & Technology Enthusiast | Software Developer\n\n"
            "**Areas of Interest**\n\n"
            "  • Artificial Intelligence\n"
            "      → AI Applications & Intelligent Systems\n"
            "      → Machine Learning Concepts\n\n"
            "  • Software Engineering\n"
            "      → Application Development & System Design\n"
            "      → Problem Solving & Software Architecture\n\n"
            "  • Data Science\n"
            "      → Data Analysis & Visualization\n"
            "      → AI-Based Solutions & Automation\n\n"
            "  • Web Technologies\n"
            "      → Frontend & Backend Development\n"
            "      → Modern UI/UX Design\n\n"
            "**Technical Skills**\n\n"
            "  • Python — Backend logic, automation, AI systems\n"
            "  • Web Development — Responsive, modern design\n"
            "  • Chatbot Development — Architecture & response engines\n"
            "  • Software Design — Scalable, maintainable systems\n\n"
            "**Professional Summary**\n\n"
            "Asjad is the creative mind and engineering force behind the ARIA chatbot "
            "and the K. M. A² Signature Series. His passion lies in exploring the frontiers "
            "of Artificial Intelligence, Data Science, and Software Engineering — "
            "translating complex concepts into practical, high-quality software solutions. "
            "His development philosophy centers on project-based learning, innovation-driven "
            "thinking, and a relentless commitment to building technology that is both "
            "intelligent and genuinely useful to the people it serves."
        ),
        (
            "**Developer Profile**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "**Developer:** Asjad\n"
            "**Professional Identity:** K. M. A²\n\n"
            "**Areas of Interest**\n\n"
            "  • Artificial Intelligence & Machine Learning\n"
            "      → AI Applications, Intelligent Systems\n"
            "      → Machine Learning Concepts & Research\n\n"
            "  • Software Engineering\n"
            "      → Application Development\n"
            "      → System Design & Problem Solving\n\n"
            "  • Data Science\n"
            "      → Data Analysis & AI-Based Solutions\n"
            "      → Data Visualization\n\n"
            "  • Automation & Intelligent Systems\n"
            "      → Scripting, Workflow Automation\n"
            "      → Smart Application Development\n\n"
            "**Technical Skills**\n\n"
            "  • Python Programming & Scripting\n"
            "  • Web Development (Frontend & Backend)\n"
            "  • Chatbot Design & Development\n"
            "  • AI Concepts & Rule-Based Systems\n"
            "  • Problem Solving & Software Architecture\n"
            "  • Automation & Software Design\n\n"
            "**Professional Summary**\n\n"
            "Asjad embodies the spirit of the modern developer — curious, driven, and always "
            "building. Through the K. M. A² brand, he channels his passion for AI and "
            "software engineering into real, functional projects that push the boundaries "
            "of what intelligent systems can achieve. This chatbot is a direct reflection "
            "of his dedication to learning, innovation, and the craft of creating "
            "intelligent, user-centered digital experiences."
        ),
    ]

    # ── Chatbot Origin / Ownership ─────────────────────────────────────────────
    # NOTE: Many of these are also handled by DEVELOPER_TRIGGERS above.
    # This remains for backward-compatibility with RULE 6.5.
    CHATBOT_ORIGIN_TRIGGERS = [
        r"where are you from", r"who owns you", r"which organization developed you",
        r"what company are you from", r"what organization are you from",
        r"who owns aria", r"which company made you", r"what company created you",
        r"who is your owner", r"where do you come from", r"your origin",
        r"which team developed you", r"aria origin", r"aria background",
        r"how did you come to be", r"what is your background",
        r"tell me your origin story",
    ]

    CHATBOT_ORIGIN_RESPONSES = [
        (
            "I am ARIA, an AI assistant developed under the K. M. A² Signature Series.\n\n"
            "K. M. A² is the professional brand identity of K. Mohammed Asjad Aliyan — "
            "a technology enthusiast and software developer driven by a vision to build "
            "intelligent, user-focused digital solutions. The K. M. A² brand is built on "
            "a foundation of innovation, continuous learning, and a deep passion for "
            "artificial intelligence and software engineering. Every project under the "
            "K. M. A² identity reflects a commitment to quality craftsmanship, "
            "thoughtful design, and the power of technology to solve real problems. "
            "ARIA is the flagship AI assistant of this series — a living demonstration "
            "of what intelligent, rule-based systems can achieve."
        ),
        (
            "I am ARIA — Artificial Rule-based Intelligent Assistant, "
            "proudly developed under the K. M. A² Signature Series by K. Mohammed Asjad Aliyan.\n\n"
            "The K. M. A² vision is rooted in creating intelligent software that is not "
            "only technically sophisticated but genuinely useful to the people who interact with it. "
            "This vision drives a continuous cycle of learning, building, and improving — "
            "from AI chatbots to web applications, from automation tools to data-driven systems. "
            "ARIA represents this vision in its purest form: an AI assistant designed to "
            "educate, assist, and inspire through the power of structured intelligence "
            "and thoughtful engineering."
        ),
        (
            "ARIA originates from the K. M. A² Signature Series — "
            "a collection of premium software projects developed by K. Mohammed Asjad Aliyan.\n\n"
            "K. M. A² is more than a brand; it is a commitment to technology-driven "
            "innovation and the belief that intelligent systems can make a meaningful "
            "difference in how people learn, work, and grow. The K. M. A² philosophy "
            "embraces continuous improvement, user-centered design, and the exploration "
            "of cutting-edge AI and software engineering concepts. "
            "ARIA is built on these principles — crafted to be a reliable, knowledgeable, "
            "and engaging AI companion that reflects the best of the K. M. A² identity."
        ),
    ]

    # ── DecodeLabs Info ────────────────────────────────────────────────────────
    DECODELABS_TRIGGERS = [
        r"what is decodelabs", r"have you heard of decodelabs", r"tell me about decodelabs",
        r"explain decodelabs", r"\bdecode labs\b", r"\bdecodelabs\b",
        r"decodelabs information", r"decodelabs details", r"decodelabs overview",
        r"what does decodelabs do", r"decodelabs platform", r"about decodelabs",
        r"decode labs information", r"what is decode labs",
        r"tell me about decode labs", r"explain decode labs",
    ]

    DECODELABS_KEYWORDS = [
        "decodelabs", "decode labs", "decodelabz", "decodlab",
    ]

    DECODELABS_FUZZY_PHRASES = []

    DECODELABS_RESPONSES = [
        (
            "DecodeLabs — Technology Learning & Development Platform\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "DecodeLabs is a technology-focused learning and project development platform "
            "that bridges the gap between theoretical knowledge and real-world engineering practice. "
            "It emphasizes hands-on, project-based learning across software development, "
            "artificial intelligence, data science, and engineering disciplines.\n\n"
            "What sets DecodeLabs apart:\n"
            "  Practical Software Development → Build real, working projects\n"
            "  AI & Data Science Learning → Applied concepts through assignments\n"
            "  Engineering Skills → Industry-oriented development practices\n"
            "  Structured Curriculum → Organized tasks that build progressively\n"
            "  Portfolio Building → Every project adds to a professional body of work\n\n"
            "DecodeLabs believes that the best way to learn technology is to build with it — "
            "and this chatbot is a prime example of that philosophy in action."
        ),
        (
            "About DecodeLabs\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "DecodeLabs is a dynamic, technology-oriented learning platform designed "
            "to transform aspiring developers and engineers into skilled, industry-ready professionals. "
            "By prioritizing project-based skill development over purely theoretical study, "
        "DecodeLabs ensures that every participant gains tangible, real-world software "
            "and AI experience that translates directly into career success.\n\n"
            "The DecodeLabs approach:\n"
            "  Learn by doing — every concept is applied through real projects\n"
            "  Build a portfolio — structured tasks create a professional showcase\n"
            "  Master modern tools — Python, web dev, AI, and more\n"
            "  Develop engineering mindset — problem-solving at the core\n\n"
            "DecodeLabs is where ideas become code, and code becomes capability."
        ),
        (
            "DecodeLabs is a technology-focused educational and project development ecosystem "
            "that empowers learners to grow as engineers through structured, practical, "
            "and industry-relevant software development experiences.\n\n"
            "Core focus areas include:\n"
            "  Practical AI & Machine Learning projects\n"
            "  Software Engineering fundamentals and advanced concepts\n"
            "  Web development and UI/UX design\n"
            "  Automation and intelligent systems development\n"
            "  Data science tools and analytical thinking\n\n"
            "At DecodeLabs, learning is never passive — it's about rolling up your sleeves, "
            "writing real code, solving real problems, and building a professional portfolio "
            "that speaks for itself. The platform represents a vision of education where "
            "every student graduates as a capable, confident, and creative technologist."
        ),
    ]

    # ── Projects Info ──────────────────────────────────────────────────────────
    PROJECTS_TRIGGERS = [
        r"what projects has the developer worked on", r"what has asjad built",
        r"show developer projects", r"tell me about his work", r"asjad.?s projects"
    ]

    PROJECTS_RESPONSES = [
        "Asjad has worked on several practical software and AI assignments through DecodeLabs, developing a robust portfolio of real-world projects. This ARIA Chatbot (Task 1) is a prime example of his work, demonstrating skills in Python logic, UI design, and rule-based AI processing. His portfolio reflects a continuous progression in solving complex engineering challenges.",
        "His work includes hands-on development tasks emphasizing modern software architecture. Specifically, he has built this interactive rule-based chatbot (Task 1), integrating a custom backend with a premium frontend UI. His portfolio continues to grow with further tasks exploring AI and intelligent systems.",
        "Asjad's project portfolio is built around functional, user-centric software solutions. You're currently interacting with one of them — a comprehensive AI chatbot built from scratch! His work spans across various tasks assigned by DecodeLabs, each designed to strengthen his capabilities in Data Science and Software Engineering."
    ]

    # ── Unknown ────────────────────────────────────────────────────────────────
    UNKNOWN_RESPONSES = [
        "I currently do not have information on that topic.\nPlease ask something related to my supported knowledge areas."
    ]

    RESTRICTED_TRIGGERS = [
        r"\bhack\b", r"illegal", r"harmful", r"dangerous", r"unethical",
        r"restricted", r"steal", r"murder", r"kill", r"bomb", r"drugs",
        r"weapon", r"dark web",
    ]


# ==============================================================================
# CHATBOT ENGINE
# ==============================================================================

class ChatBot:
    """
    ARIA — Artificial Rule-based Intelligent Assistant
    Powered by the KMA² Intelligence Framework

    The main chatbot engine implementing rule-based conversation logic.
    Uses pattern matching with if-else control flow to generate responses.
    """

    def __init__(self, name: str = "ARIA"):
        self.name = name
        self.kb = KnowledgeBase()
        self.conversation_history: list[dict] = []
        self.session_start = datetime.now()
        self.message_count = 0
        self.user_name: str | None = None

    def _normalize(self, text: str) -> str:
        """Convert input to lowercase and strip whitespace for matching (basic)."""
        text = text.lower().strip()
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
                        return "Division by zero is undefined — even mathematics has its limits!"
                    result = a / b
                else:
                    return None

                result_str = str(int(result)) if result == int(result) else f"{result:.4f}"
                return f"Result: {a_str} {op} {b_str} = {result_str}\n\nMathematics — the universal language of precision."
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
                name = match.group(1)
                # Filter out common false positives
                if name.lower() not in ["aria", "an", "a", "the", "not", "just", "here"]:
                    return name.capitalize()
        return None

    def _log_message(self, role: str, message: str) -> None:
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

    def _format_by_mode(self, response: str, mode: str, user_input: str, category: str) -> str:
        """
        Algorithmic Response Formatter.
        Modifies the hardcoded rule-based response to match the requested mode without
        changing the underlying knowledge base facts.
        """
        if mode == "fast":
            # Extract first paragraph or first sentence
            paragraphs = [p for p in response.split('\n\n') if p.strip()]
            if paragraphs:
                first_para = paragraphs[0]
                # If the first para has bullet points, just take the first line
                lines = first_para.split('\n')
                fast_response = lines[0].strip()
                # Remove Markdown bolding for cleaner fast text
                fast_response = fast_response.replace("**", "")
                return fast_response
            return response

        elif mode == "deep_thinking":
            # Inject analytical framing
            analytical_intro = "Analyzing the core concepts..."
            if category in ["ai_knowledge", "cs_concepts", "programming"]:
                analytical_intro = f"From a technical perspective, exploring the concept of {category.replace('_', ' ')}..."
            
            analytical_outro = "\n\nThis implies a deeper structural significance within the ecosystem."
            
            # Format the text
            deep_response = f"**[Deep Thinking Mode Enabled]**\n\n*{analytical_intro}*\n\n{response}{analytical_outro}"
            return deep_response

        elif mode == "detailed":
            # Structure the text with strict headers and bullet points
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            if not lines:
                return response
            
            detailed_response = "### Definition & Core Concept\n" + lines[0] + "\n\n### Key Insights & Details\n"
            
            for line in lines[1:]:
                # Ensure it looks like a bullet if it isn't already
                if not line.startswith("-") and not line.startswith("*"):
                    detailed_response += f"- {line}\n"
                else:
                    detailed_response += f"{line}\n"
                    
            detailed_response += "\n### Applications & Context\n- Widely applicable in modern development environments.\n- Fundamental to the KMA² Signature Series framework."
            return detailed_response

        elif mode == "interview":
            # Wrap in an Interview Question/Answer format
            question = "Can you explain this topic?"
            if len(user_input) > 5:
                question = user_input.capitalize()
            
            # Professional phrasing
            prof_intro = "As an industry professional, I would explain that "
            # Lowercase first char of response to flow with intro if it's a letter
            first_char = response[0] if response else ""
            if first_char.isalpha():
                response = first_char.lower() + response[1:]
                
            return f"**Interview Question:**\n\"{question}\"\n\n**Professional Answer:**\n{prof_intro}{response}"
            
        return response

    def get_response(self, user_input: str, language: str = "en", mode: str = "normal") -> tuple[str, str]:
        """
        Public wrapper that intercepts the internal response and translates it
        if a non-English language is selected.
        """
        # Get response in English first
        response, category = self._get_response_internal(user_input)
        
        # Apply Mode Formatting BEFORE translation
        if mode != "normal":
            response = self._format_by_mode(response, mode, user_input, category)
        
        # Translate if necessary
        if language != "en":
            try:
                from deep_translator import GoogleTranslator
                translator = GoogleTranslator(source='auto', target=language)
                
                # We translate line by line to preserve formatting and line breaks
                lines = response.split('\n')
                translated_lines = []
                for line in lines:
                    if line.strip():
                        translated_lines.append(translator.translate(line))
                    else:
                        translated_lines.append('')
                
                response = '\n'.join(translated_lines)
            except Exception as e:
                print(f"Translation Error: {e}")
                # Fallback to English seamlessly if translation fails
        
        return response, category

    def _get_response_internal(self, user_input: str) -> tuple[str, str]:
        """
        Core decision-making function.
        Implements rule-based AI logic using priority-ordered if-else control flow
        with Smart Intent Detection Engine (9-layer matching).
        Returns a tuple of (response_text, category).
        """
        raw_input = user_input
        normalized = self._normalize(user_input)
        # Smart-normalized version: spell-corrected + synonym-expanded
        smart_normalized = SmartMatcher.normalize(user_input)
        self.message_count += 1
        self._log_message("user", raw_input)

        # ── RESTRICTED CONTENT CHECK ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.RESTRICTED_TRIGGERS):
            response = "I cannot assist with harmful, dangerous, illegal, or restricted activities."
            self._log_message("bot", response)
            return response, "system"

        # ── RULE 0: Empty input ────────────────────────────────────────────────
        if not normalized.strip():
            response = "Please type something so I can help you. Type 'help' if you're not sure where to start!"
            self._log_message("bot", response)
            return response, "error"

        # ── RULE 1: Detect username ────────────────────────────────────────────
        detected_name = self._check_user_name(normalized)
        if detected_name:
            self.user_name = detected_name
            response = f"It's great to meet you, {detected_name}! I'll remember that. How can I assist you today?"
            self._log_message("bot", response)
            return response, "personal"

        # ── RULE 2: Farewells ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.FAREWELL_TRIGGERS):
            farewell = random.choice(self.kb.FAREWELL_RESPONSES)
            if self.user_name:
                farewell = farewell.replace("!", f", {self.user_name}!", 1)
            self._log_message("bot", farewell)
            return farewell, "farewell"

        # ── RULE 3: Greetings ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.GREETING_TRIGGERS):
            greeting = random.choice(self.kb.GREETING_RESPONSES)
            if self.user_name:
                greeting = greeting.replace("!", f", {self.user_name}!", 1)
            self._log_message("bot", greeting)
            return greeting, "greeting"

        # ── RULE 4: How are you ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HOW_ARE_YOU_TRIGGERS):
            response = random.choice(self.kb.HOW_ARE_YOU_RESPONSES)
            self._log_message("bot", response)
            return response, "smalltalk"

        # ── RULE 5: Human/AI identity ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HUMAN_TRIGGERS):
            response = random.choice(self.kb.HUMAN_RESPONSES)
            self._log_message("bot", response)
            return response, "identity"

        # ── RULE 6: Name / Identity ────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.NAME_TRIGGERS):
            response = random.choice(self.kb.NAME_RESPONSES)
            self._log_message("bot", response)
            return response, "identity"

        # ── RULE 6.5: Chatbot Origin / Ownership ───────────────────────────────
        if self._contains_any(normalized, self.kb.CHATBOT_ORIGIN_TRIGGERS):
            response = random.choice(self.kb.CHATBOT_ORIGIN_RESPONSES)
            self._log_message("bot", response)
            return response, "about"

        # ── RULE 7.0: KMA² Full Name Expansion (must run BEFORE general KMA) ──
        if self._contains_any(normalized, self.kb.KMA_FULLNAME_TRIGGERS) or \
           self._contains_any(smart_normalized, self.kb.KMA_FULLNAME_TRIGGERS):
            response = self.kb.KMA_FULLNAME_RESPONSE
            self._log_message("bot", response)
            return response, "about"

        # ── RULE 7: KMA² Info — 9-layer smart match ──────────────────────────
        if SmartMatcher.smart_match(
            smart_normalized, self.kb.KMA_TRIGGERS
        ) or self._contains_any(normalized, self.kb.KMA_TRIGGERS):
            response = random.choice(self.kb.KMA_RESPONSES)
            self._log_message("bot", response)
            return response, "about"

        # ── RULE 7.1: Developer Info — 9-layer smart match ────────────────────
        if SmartMatcher.smart_match(
            smart_normalized,
            self.kb.DEVELOPER_TRIGGERS,
            keywords=self.kb.DEVELOPER_KEYWORDS,
            fuzzy_phrases=self.kb.DEVELOPER_FUZZY_PHRASES,
        ) or self._contains_any(normalized, self.kb.DEVELOPER_TRIGGERS):
            response = random.choice(self.kb.DEVELOPER_RESPONSES)
            self._log_message("bot", response)
            return response, "developer"

        # ── RULE 7.2: DecodeLabs Info — 9-layer smart match ───────────────────
        if SmartMatcher.smart_match(
            smart_normalized,
            self.kb.DECODELABS_TRIGGERS,
            keywords=self.kb.DECODELABS_KEYWORDS,
            fuzzy_phrases=self.kb.DECODELABS_FUZZY_PHRASES,
        ) or self._contains_any(normalized, self.kb.DECODELABS_TRIGGERS):
            response = random.choice(self.kb.DECODELABS_RESPONSES)
            self._log_message("bot", response)
            return response, "organization"

        # ── RULE 7.3: Projects Info ────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.PROJECTS_TRIGGERS):
            response = random.choice(self.kb.PROJECTS_RESPONSES)
            self._log_message("bot", response)
            return response, "projects"

        # ── RULE 8: Help menu ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HELP_TRIGGERS):
            response = self.kb.HELP_RESPONSE
            self._log_message("bot", response)
            return response, "help"

        # ── RULE 9: Time query ─────────────────────────────────────────────────
        TIME_TRIGGERS = [
            r"what time is it", r"current time", r"time now", r"what.?s the time",
            r"tell me the time",
        ]
        if self._contains_any(normalized, TIME_TRIGGERS):
            now = datetime.now()
            response = (
                f"Current Time: {now.strftime('%I:%M:%S %p')}\n"
                f"Date: {now.strftime('%A, %d %B %Y')}"
            )
            self._log_message("bot", response)
            return response, "time"

        # ── RULE 10: Date query ────────────────────────────────────────────────
        DATE_TRIGGERS = [
            r"today.?s date", r"what.?s today", r"current date",
            r"what day is it", r"day today", r"what is today",
            r"what.?s the date",
        ]
        if self._contains_any(normalized, DATE_TRIGGERS):
            now = datetime.now()
            response = (
                f"Today is: {now.strftime('%A, %d %B %Y')}\n"
                f"Day {now.timetuple().tm_yday} of {now.year}."
            )
            self._log_message("bot", response)
            return response, "date"

        # ── RULE 11: Math calculation ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.MATH_TRIGGERS):
            math_result = self._try_math(normalized)
            if math_result:
                self._log_message("bot", math_result)
                return math_result, "math"
            # Non-calculation math question
            response = (
                "I can handle basic arithmetic! Try asking:\n"
                "  '15 + 27', '100 - 43', '12 * 8', '144 / 12'\n\n"
                "For algebra, geometry, or percentage concepts, just ask and I'll explain!"
            )
            self._log_message("bot", response)
            return response, "math"

        # ── RULE 12: Weather ───────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.WEATHER_TRIGGERS):
            response = random.choice(self.kb.WEATHER_RESPONSES)
            self._log_message("bot", response)
            return response, "weather"

        # ── RULE 13: Generative AI / LLMs ─────────────────────────────────────
        if self._contains_any(normalized, self.kb.GEN_AI_TRIGGERS):
            response = random.choice(self.kb.GEN_AI_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 14: Machine Learning ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.ML_TRIGGERS):
            response = random.choice(self.kb.ML_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 15: Deep Learning / Neural Networks ───────────────────────────
        if self._contains_any(normalized, self.kb.DEEP_LEARNING_TRIGGERS):
            response = random.choice(self.kb.DEEP_LEARNING_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 16: NLP ───────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.NLP_TRIGGERS):
            response = random.choice(self.kb.NLP_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 17: Computer Vision ───────────────────────────────────────────
        if self._contains_any(normalized, self.kb.CV_TRIGGERS):
            response = random.choice(self.kb.CV_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 18: AI general ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.AI_TRIGGERS):
            response = random.choice(self.kb.AI_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 19: Python ────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.PYTHON_TRIGGERS):
            response = random.choice(self.kb.PYTHON_RESPONSES)
            self._log_message("bot", response)
            return response, "python"

        # ── RULE 20: Java ─────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.JAVA_TRIGGERS):
            response = random.choice(self.kb.JAVA_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 21: JavaScript ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.JAVASCRIPT_TRIGGERS):
            response = random.choice(self.kb.JAVASCRIPT_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 22: C/C++ ────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.C_TRIGGERS):
            response = random.choice(self.kb.C_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 23: SQL ──────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.SQL_TRIGGERS):
            response = random.choice(self.kb.SQL_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 24: HTML/CSS ─────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.HTML_CSS_TRIGGERS):
            response = random.choice(self.kb.HTML_CSS_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 25: Data Structures & Algorithms ─────────────────────────────
        if self._contains_any(normalized, self.kb.DSA_TRIGGERS):
            response = random.choice(self.kb.DSA_RESPONSES)
            self._log_message("bot", response)
            return response, "cs_concepts"

        # ── RULE 26: Operating Systems ────────────────────────────────────────
        if self._contains_any(normalized, self.kb.OS_TRIGGERS):
            response = random.choice(self.kb.OS_RESPONSES)
            self._log_message("bot", response)
            return response, "cs_concepts"

        # ── RULE 27: Databases ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.DATABASE_TRIGGERS):
            response = random.choice(self.kb.DATABASE_RESPONSES)
            self._log_message("bot", response)
            return response, "cs_concepts"

        # ── RULE 28: Cloud Computing ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.CLOUD_TRIGGERS):
            response = random.choice(self.kb.CLOUD_RESPONSES)
            self._log_message("bot", response)
            return response, "cs_concepts"

        # ── RULE 29: Cybersecurity ────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.CYBER_TRIGGERS):
            response = random.choice(self.kb.CYBER_RESPONSES)
            self._log_message("bot", response)
            return response, "cs_concepts"

        # ── RULE 30: Web Development ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.WEBDEV_TRIGGERS):
            response = random.choice(self.kb.WEBDEV_RESPONSES)
            self._log_message("bot", response)
            return response, "programming"

        # ── RULE 31: Data Science ─────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.DATA_SCIENCE_TRIGGERS):
            response = random.choice(self.kb.DATA_SCIENCE_RESPONSES)
            self._log_message("bot", response)
            return response, "ai_knowledge"

        # ── RULE 32: Utilities (Catch-all) ────────────────────────────────────
        if self._contains_any(normalized, self.kb.UTILITIES_TRIGGERS):
            response = random.choice(self.kb.UTILITIES_RESPONSES)
            self._log_message("bot", response)
            return response, "utility"

        # ── RULE 33: Study Tips ───────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.STUDY_TRIGGERS):
            response = random.choice(self.kb.STUDY_RESPONSES)
            self._log_message("bot", response)
            return response, "education"

        # ── RULE 34: Time Management ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.TIME_MGMT_TRIGGERS):
            response = random.choice(self.kb.TIME_MGMT_RESPONSES)
            self._log_message("bot", response)
            return response, "education"

        # ── RULE 35: Motivation ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.MOTIVATION_TRIGGERS):
            response = random.choice(self.kb.MOTIVATIONAL_QUOTES)
            self._log_message("bot", response)
            return response, "motivation"

        # ── RULE 36: General Knowledge ─────────────────────────────────────────
        if self._contains_any(normalized, self.kb.GENERAL_KNOWLEDGE_TRIGGERS) or self._contains_any(normalized, self.kb.GEN_KNOWLEDGE_TRIGGERS):
            response = random.choice(self.kb.GENERAL_KNOWLEDGE_RESPONSES)
            self._log_message("bot", response)
            return response, "knowledge"

        # ── RULE 37: Internet & Technology ────────────────────────────────────
        if self._contains_any(normalized, self.kb.INTERNET_TRIGGERS):
            response = random.choice(self.kb.INTERNET_RESPONSES)
            self._log_message("bot", response)
            return response, "technology"

        # ── RULE 38: Entertainment / Riddles / Jokes ───────────────────────────
        if self._contains_any(normalized, self.kb.ENTERTAINMENT_TRIGGERS) or self._contains_any(normalized, self.kb.JOKE_TRIGGERS) or self._contains_any(normalized, self.kb.RIDDLE_TRIGGERS):
            response = random.choice(self.kb.ENTERTAINMENT_RESPONSES)
            self._log_message("bot", response)
            return response, "entertainment"

        # ── RULE 44: Thanks / Gratitude ────────────────────────────────────────
        if self._contains_any(normalized, self.kb.THANKS_TRIGGERS):
            response = random.choice(self.kb.THANKS_RESPONSES)
            self._log_message("bot", response)
            return response, "thanks"

        # ── RULE 45: Conversation history ─────────────────────────────────────
        if "history" in normalized:
            response = self._format_history()
            self._log_message("bot", response)
            return response, "meta"

        # ══════════════════════════════════════════════════════════════════════
        # MULTI-STEP FALLBACK SEARCH — runs before showing "unknown" response
        # Step 1: Intent Group Search (smart-normalized against all trigger sets)
        # Step 2: Keyword Group Search (broad keyword scan)
        # Step 3: Synonym Search (synonym-expanded text re-check)
        # Step 4: Semantic Similarity (partial fuzzy topic match)
        # Step 5: Related Topic matching
        # ══════════════════════════════════════════════════════════════════════

        # ── FALLBACK 1: Re-run developer/origin check with smart-normalized ──
        if SmartMatcher.smart_match(
            smart_normalized,
            self.kb.DEVELOPER_TRIGGERS,
            keywords=self.kb.DEVELOPER_KEYWORDS,
            fuzzy_phrases=self.kb.DEVELOPER_FUZZY_PHRASES,
        ):
            response = random.choice(self.kb.DEVELOPER_RESPONSES)
            self._log_message("bot", response)
            return response, "developer"

        # ── FALLBACK 2: Broad keyword scan across all major topics ────────────
        # Map keywords → intent handlers
        BROAD_KEYWORD_MAP = [
            (["ai", "artificial intelligence", "machine learning", "deep learning",
              "neural", "nlp", "gpt", "llm", "generative"],                "ai"),
            (["python", "java", "javascript", "html", "css", "sql",
              "programming", "coding", "code"],                             "programming"),
            (["study", "learn", "exam", "focus", "memory", "concentrate"],  "study"),
            (["motivat", "inspire", "quote", "confidence", "goal"],         "motivation"),
            (["data", "pandas", "numpy", "science", "analytics"],           "data_science"),
            (["cloud", "aws", "azure", "gcp"],                              "cloud"),
            (["security", "cyber", "hack", "encrypt"],                     "cyber"),
            (["web", "frontend", "backend", "full stack", "flask", "django"],"web"),
            (["time", "productive", "procrastinat", "routine"],             "productivity"),
            (["joke", "laugh", "funny", "humor"],                          "joke"),
            (["fact", "trivia", "interesting", "did you know"],             "knowledge"),
        ]

        BROAD_HANDLER = {
            "ai":          (self.kb.AI_TRIGGERS,           self.kb.AI_RESPONSES,           "ai_knowledge"),
            "programming": (self.kb.PYTHON_TRIGGERS,       self.kb.PYTHON_RESPONSES,       "programming"),
            "study":       (self.kb.STUDY_TRIGGERS,        self.kb.STUDY_RESPONSES,        "education"),
            "motivation":  (self.kb.MOTIVATION_TRIGGERS,   self.kb.MOTIVATIONAL_QUOTES,    "motivation"),
            "data_science":(self.kb.DATA_SCIENCE_TRIGGERS, self.kb.DATA_SCIENCE_RESPONSES, "ai_knowledge"),
            "cloud":       (self.kb.CLOUD_TRIGGERS,        self.kb.CLOUD_RESPONSES,        "cs_concepts"),
            "cyber":       (self.kb.CYBER_TRIGGERS,        self.kb.CYBER_RESPONSES,        "cs_concepts"),
            "web":         (self.kb.WEBDEV_TRIGGERS,       self.kb.WEBDEV_RESPONSES,       "programming"),
            "productivity":(self.kb.TIME_MGMT_TRIGGERS,    self.kb.TIME_MGMT_RESPONSES,    "education"),
            "joke":        (self.kb.JOKE_TRIGGERS,         self.kb.JOKES,                  "joke"),
            "knowledge":   (self.kb.GEN_KNOWLEDGE_TRIGGERS,self.kb.GEN_KNOWLEDGE_RESPONSES,"knowledge"),
        }

        for keywords, topic in BROAD_KEYWORD_MAP:
            for kw in keywords:
                if kw in normalized or kw in smart_normalized:
                    _, responses, category = BROAD_HANDLER[topic]
                    response = random.choice(responses)
                    self._log_message("bot", response)
                    return response, category

        # ── FALLBACK 3: Fuzzy topic detection on smart-normalized text ────────
        FUZZY_TOPIC_PHRASES = [
            ("python",         self.kb.PYTHON_RESPONSES,         "programming"),
            ("machine learn",  self.kb.ML_RESPONSES,             "ai_knowledge"),
            ("deep learn",     self.kb.DEEP_LEARNING_RESPONSES,  "ai_knowledge"),
            ("data science",   self.kb.DATA_SCIENCE_RESPONSES,   "ai_knowledge"),
            ("web dev",        self.kb.WEBDEV_RESPONSES,         "programming"),
            ("artificial intel",self.kb.AI_RESPONSES,            "ai_knowledge"),
            ("career",         self.kb.CAREER_SE_RESPONSES,      "career"),
            ("study",          self.kb.STUDY_RESPONSES,          "education"),
            ("motivat",        self.kb.MOTIVATIONAL_QUOTES,      "motivation"),
        ]

        for phrase, responses, category in FUZZY_TOPIC_PHRASES:
            if SmartMatcher.fuzzy_contains(smart_normalized, phrase, tolerance=1):
                response = random.choice(responses)
                self._log_message("bot", response)
                return response, category

        # ── DEFAULT: Last-resort unknown response ─────────────────────────────
        response = random.choice(self.kb.UNKNOWN_RESPONSES)
        self._log_message("bot", response)
        return response, "unknown"

    def _format_history(self) -> str:
        """Format conversation history for display."""
        if len(self.conversation_history) <= 2:
            return "No conversation history yet — we're just getting started!"

        lines = ["Conversation History\n" + "─" * 40]
        count = 0
        for entry in self.conversation_history[-10:]:
            role_icon = "You" if entry["role"] == "user" else "ARIA"
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
