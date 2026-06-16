"""
brain.py - KMA² Intelligence Framework — Rule-Based AI Core Engine
===================================================================
The central decision-making module of the chatbot.
Implements pure rule-based logic to simulate intelligent conversation
through programmatic decision-making and pattern matching.

Architecture: KMA² Signature Series
Framework:    KMA² Intelligence Framework v2.0
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
            "Key branches of AI:\n"
            "  Rule-Based AI → Uses if-else logic and predefined rules (that's me!)\n"
            "  Machine Learning → Systems that learn from data\n"
            "  Deep Learning → Neural networks with multiple layers\n"
            "  Natural Language Processing → Understanding human language\n"
            "  Computer Vision → Interpreting visual information\n\n"
            "AI is transforming every industry — from healthcare to finance to education!"
        ),
        (
            "AI (Artificial Intelligence) works by mimicking human decision-making processes.\n\n"
            "The AI hierarchy:\n"
            "  1. Rule-Based AI — Explicit programmed rules\n"
            "  2. Machine Learning — Statistical pattern recognition\n"
            "  3. Deep Learning — Multi-layered neural networks\n"
            "  4. AGI (future) — Human-level general intelligence\n\n"
            "Every great AI journey starts with understanding rule-based systems — exactly like me!"
        ),
        (
            "Artificial Intelligence is one of the most transformative technologies of our era!\n\n"
            "AI Timeline highlights:\n"
            "  1950 — Alan Turing proposes the 'Turing Test'\n"
            "  1956 — Term 'Artificial Intelligence' coined\n"
            "  1997 — Deep Blue defeats chess world champion\n"
            "  2012 — Deep Learning revolution begins\n"
            "  2022 — Generative AI becomes mainstream\n\n"
            "We're living in the most exciting era of AI development in history!"
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
            "Types of Machine Learning:\n"
            "  Supervised Learning → Learn from labeled data (e.g., spam detection)\n"
            "  Unsupervised Learning → Find patterns in unlabeled data (e.g., clustering)\n"
            "  Reinforcement Learning → Learn through rewards and penalties (e.g., game AI)\n\n"
            "ML powers everything from Netflix recommendations to self-driving cars!"
        ),
        (
            "Machine Learning allows computers to learn and improve from experience!\n\n"
            "The ML workflow:\n"
            "  1. Collect & clean data\n"
            "  2. Choose a model (algorithm)\n"
            "  3. Train on training data\n"
            "  4. Evaluate on test data\n"
            "  5. Deploy and monitor\n\n"
            "Popular ML algorithms include Linear Regression, Decision Trees, Random Forests, and SVMs."
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
            "Why Python?\n"
            "  Clean, readable syntax — perfect for beginners\n"
            "  Massive ecosystem: NumPy, Pandas, TensorFlow, PyTorch\n"
            "  Rapid prototyping and development\n"
            "  Huge community and job market\n"
            "  Cross-platform (Windows, Mac, Linux)\n\n"
            "Python Roadmap: Basics → OOP → Libraries → Projects → AI/ML"
        ),
        (
            "Python is the language of the future — and the present!\n\n"
            "Essential Python concepts:\n"
            "  Variables & Data Types (int, str, list, dict)\n"
            "  Control Flow (if/else, loops)\n"
            "  Functions & Modules\n"
            "  Object-Oriented Programming\n"
            "  File Handling & Exception Management\n\n"
            "Python tip: Practice daily. Even 30 minutes a day builds mastery in months!"
        ),
        (
            "Python powers some of the world's most important software!\n\n"
            "Python is used in:\n"
            "  Artificial Intelligence & Machine Learning\n"
            "  Web Development (Django, Flask)\n"
            "  Data Science & Analytics\n"
            "  Automation & Scripting\n"
            "  Scientific Research\n"
            "  Cybersecurity\n\n"
            "Start with: python.org tutorials, then move to real projects!"
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

    # ── Career Guidance: Software Engineer ────────────────────────────────────
    CAREER_SE_TRIGGERS = [
        r"how to become a software engineer", r"software engineer career",
        r"become a developer", r"software development career",
        r"how to get a job in tech", r"tech career", r"it career",
        r"career in programming", r"career in software",
    ]

    CAREER_SE_RESPONSES = [
        (
            "Here's a roadmap to becoming a Software Engineer:\n\n"
            "Step 1: Learn programming fundamentals (Python, Java, or C++)\n"
            "Step 2: Study Data Structures & Algorithms\n"
            "Step 3: Learn a web framework (Django, React, etc.)\n"
            "Step 4: Build 3-5 real projects for your portfolio\n"
            "Step 5: Learn Git & version control\n"
            "Step 6: Start applying and prepare for interviews\n\n"
            "Timeline: 6-12 months of focused learning can get you interview-ready!\n"
            "Key insight: Projects matter more than certificates. Build. Build. Build."
        ),
    ]

    # ── Career in AI / ML ─────────────────────────────────────────────────────
    CAREER_AI_TRIGGERS = [
        r"career in ai", r"career in machine learning", r"ai engineer",
        r"ml engineer", r"how to become an ai engineer", r"ai job",
        r"machine learning career", r"how to get into ai",
    ]

    CAREER_AI_RESPONSES = [
        (
            "Breaking into AI is one of the best career moves you can make!\n\n"
            "AI Career Roadmap:\n"
            "  Foundation: Python, Mathematics (Linear Algebra, Statistics, Calculus)\n"
            "  Machine Learning: Scikit-learn, supervised/unsupervised learning\n"
            "  Deep Learning: TensorFlow or PyTorch\n"
            "  Specialization: NLP, Computer Vision, or Reinforcement Learning\n"
            "  Portfolio: Kaggle competitions, GitHub projects, research papers\n\n"
            "Top certifications:\n"
            "  Google TensorFlow Developer Certificate\n"
            "  AWS Machine Learning Specialty\n"
            "  DeepLearning.AI courses (Coursera)"
        ),
    ]

    # ── Interview Preparation ─────────────────────────────────────────────────
    INTERVIEW_TRIGGERS = [
        r"interview prep", r"interview preparation", r"coding interview",
        r"technical interview", r"how to prepare for interview",
        r"interview tips", r"job interview", r"crack interview",
    ]

    INTERVIEW_RESPONSES = [
        (
            "Cracking technical interviews requires strategic preparation!\n\n"
            "Interview prep strategy:\n"
            "  DSA Practice: LeetCode, HackerRank, GeeksforGeeks\n"
            "  System Design: Learn scalable architecture concepts\n"
            "  Behavioral: STAR method (Situation, Task, Action, Result)\n"
            "  Mock Interviews: Practice with peers or Pramp\n\n"
            "Focus areas:\n"
            "  Arrays, Strings, Linked Lists, Trees, Graphs\n"
            "  Dynamic Programming, Recursion\n"
            "  OOP concepts, Design Patterns\n\n"
            "Golden rule: Solve 150+ LeetCode problems consistently!"
        ),
    ]

    # ── Resume Tips ───────────────────────────────────────────────────────────
    RESUME_TRIGGERS = [
        r"resume tips", r"how to write a resume", r"cv tips", r"resume advice",
        r"improve my resume", r"resume for fresher", r"resume format",
    ]

    RESUME_RESPONSES = [
        (
            "A strong resume is your ticket to the interview room!\n\n"
            "Resume essentials:\n"
            "  Keep it to 1 page (for freshers/early career)\n"
            "  Use action verbs: Built, Developed, Implemented, Improved\n"
            "  Quantify achievements: 'Improved performance by 40%'\n"
            "  Tailor for each job application\n"
            "  Include: Projects, Skills, Education, Certifications\n\n"
            "Resume tips:\n"
            "  No spelling errors — proofread 3 times!\n"
            "  Use a clean, ATS-friendly format\n"
            "  GitHub link is a MUST for developers\n"
            "  LinkedIn profile should match your resume"
        ),
    ]

    # ── LinkedIn Tips ─────────────────────────────────────────────────────────
    LINKEDIN_TRIGGERS = [
        r"linkedin tips", r"how to use linkedin", r"linkedin profile",
        r"linkedin for students", r"linkedin advice", r"build linkedin",
    ]

    LINKEDIN_RESPONSES = [
        (
            "LinkedIn is the world's largest professional network — use it wisely!\n\n"
            "LinkedIn profile must-haves:\n"
            "  Professional headshot\n"
            "  Compelling headline (not just 'Student')\n"
            "  Detailed About section telling your story\n"
            "  All experience and projects listed\n"
            "  Skills endorsed by connections\n\n"
            "Growth strategy:\n"
            "  Connect with industry professionals\n"
            "  Post your project updates and learnings\n"
            "  Engage with relevant content\n"
            "  Join AI/Tech groups\n"
            "  Reach out to recruiters professionally"
        ),
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

    # ── KMA² Info ──────────────────────────────────────────────────────────────
    KMA_TRIGGERS = [
        r"\bkma\b", r"kma2", r"kma squared", r"kma signature",
        r"kma intelligence", r"about kma", r"what is kma",
        r"what does k.?m.?a.? mean", r"what is the logo",
        r"who owns k.?m.?a", r"explain k.?m.?a"
    ]

    KMA_RESPONSES = [
        "K. M. A² is the signature project identity used across technology, software, and AI projects. It represents innovation, engineering excellence, creativity, continuous learning, and modern software development.",
        "The K. M. A² identity is the hallmark of premium digital solutions. It stands for a commitment to engineering excellence, cutting-edge artificial intelligence, and innovative software architecture.",
        "K. M. A² represents a continuous journey of learning and development in modern software engineering, encapsulating the drive for creating intelligent, practical, and highly optimized technology solutions."
    ]

    # ── Developer Info ─────────────────────────────────────────────────────────
    DEVELOPER_TRIGGERS = [
        r"who is the developer", r"who developed you", r"who created you",
        r"tell me about your developer", r"who built this chatbot", r"who is behind this project",
        r"tell me about asjad", r"who is asjad", r"who is behind this chatbot",
        r"\basjad\b"
    ]

    DEVELOPER_RESPONSES = [
        "This chatbot was developed by Asjad, an aspiring AI-focused software developer and technology enthusiast. He is passionate about Artificial Intelligence, Data Science, Software Engineering, Automation, and building practical technology solutions. This chatbot is part of his project portfolio demonstrating modern chatbot development, user experience design, and intelligent software systems.",
        "This chatbot was developed by Asjad, a technology enthusiast with a strong interest in Artificial Intelligence, Data Science, Software Engineering, Automation, and modern digital technologies. He focuses on building practical software projects that improve problem-solving skills and real-world development experience.\n\nHis interests include AI-powered applications, chatbot development, web technologies, intelligent systems, data-driven solutions, and user-centered software design. Through project-based learning, he continuously explores new technologies and works on developing modern software solutions that combine functionality, usability, and innovation.\n\nThis chatbot project demonstrates experience in Python development, chatbot architecture, user interface design, knowledge-base systems, and practical software engineering concepts.",
        "Asjad built this chatbot! He is an enthusiastic software developer focused on Artificial Intelligence and intelligent systems. By building projects like this, he showcases his skills in Python, backend logic, and frontend design, bringing modern and accessible tech solutions to life."
    ]

    # ── DecodeLabs Info ────────────────────────────────────────────────────────
    DECODELABS_TRIGGERS = [
        r"what is decodelabs", r"have you heard of decodelabs", r"tell me about decodelabs",
        r"explain decodelabs", r"\bdecode labs\b", r"\bdecodelabs\b"
    ]

    DECODELABS_RESPONSES = [
        "DecodeLabs is a technology-focused learning and project development platform that emphasizes practical, hands-on learning through software, AI, and engineering projects. It encourages learners to strengthen technical skills through real-world project implementation, structured assignments, problem-solving activities, and industry-oriented development practices.",
        "DecodeLabs provides a technology-oriented learning environment where students tackle practical assignments. By prioritizing project-based skill development over purely theoretical study, it ensures participants gain real software and AI learning opportunities.",
        "At its core, DecodeLabs is about engineering-focused project experience. It's a platform that helps aspiring developers and engineers build a robust portfolio through structured, hands-on software development and AI challenges."
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
        "I don't have specific information on that topic yet, but I can help with AI, Python, technology, programming, career guidance, study tips, productivity, and general knowledge. Type 'help' to see everything I cover!",
        "That's an interesting question! I don't have a specific answer for that yet, but my expertise covers artificial intelligence, programming languages, computer science concepts, career guidance, and learning strategies. What else can I help with?",
        "I don't have detailed information on that particular topic, but I can guide you through AI concepts, Python, web development, data science, career advice, and much more. Shall we explore one of those areas?",
        "That topic isn't in my current knowledge base, but I'd love to help with something I do know well — AI, machine learning, programming, career development, study techniques, or even just a good joke! Type 'help' for the full list.",
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
        """Convert input to lowercase and strip whitespace for matching."""
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

    def get_response(self, user_input: str) -> tuple[str, str]:
        """
        Core decision-making function.
        Implements rule-based AI logic using priority-ordered if-else control flow.
        Returns a tuple of (response_text, category).
        """
        raw_input = user_input
        normalized = self._normalize(user_input)
        self.message_count += 1
        self._log_message("user", raw_input)

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

        # ── RULE 7: KMA² Info ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.KMA_TRIGGERS):
            response = random.choice(self.kb.KMA_RESPONSES)
            self._log_message("bot", response)
            return response, "about"

        # ── RULE 7.1: Developer Info ───────────────────────────────────────────
        if self._contains_any(normalized, self.kb.DEVELOPER_TRIGGERS):
            response = random.choice(self.kb.DEVELOPER_RESPONSES)
            self._log_message("bot", response)
            return response, "developer"

        # ── RULE 7.2: DecodeLabs Info ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.DECODELABS_TRIGGERS):
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

        # ── RULE 32: Career — Software Engineer ───────────────────────────────
        if self._contains_any(normalized, self.kb.CAREER_SE_TRIGGERS):
            response = random.choice(self.kb.CAREER_SE_RESPONSES)
            self._log_message("bot", response)
            return response, "career"

        # ── RULE 33: Career — AI/ML ───────────────────────────────────────────
        if self._contains_any(normalized, self.kb.CAREER_AI_TRIGGERS):
            response = random.choice(self.kb.CAREER_AI_RESPONSES)
            self._log_message("bot", response)
            return response, "career"

        # ── RULE 34: Interview Prep ───────────────────────────────────────────
        if self._contains_any(normalized, self.kb.INTERVIEW_TRIGGERS):
            response = random.choice(self.kb.INTERVIEW_RESPONSES)
            self._log_message("bot", response)
            return response, "career"

        # ── RULE 35: Resume Tips ──────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.RESUME_TRIGGERS):
            response = random.choice(self.kb.RESUME_RESPONSES)
            self._log_message("bot", response)
            return response, "career"

        # ── RULE 36: LinkedIn Tips ────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.LINKEDIN_TRIGGERS):
            response = random.choice(self.kb.LINKEDIN_RESPONSES)
            self._log_message("bot", response)
            return response, "career"

        # ── RULE 37: Study Tips ───────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.STUDY_TRIGGERS):
            response = random.choice(self.kb.STUDY_RESPONSES)
            self._log_message("bot", response)
            return response, "education"

        # ── RULE 38: Time Management ──────────────────────────────────────────
        if self._contains_any(normalized, self.kb.TIME_MGMT_TRIGGERS):
            response = random.choice(self.kb.TIME_MGMT_RESPONSES)
            self._log_message("bot", response)
            return response, "education"

        # ── RULE 39: Motivation ────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.MOTIVATION_TRIGGERS):
            response = random.choice(self.kb.MOTIVATIONAL_QUOTES)
            self._log_message("bot", response)
            return response, "motivation"

        # ── RULE 40: General Knowledge / Fun Facts ────────────────────────────
        if self._contains_any(normalized, self.kb.GEN_KNOWLEDGE_TRIGGERS):
            response = random.choice(self.kb.GEN_KNOWLEDGE_RESPONSES)
            self._log_message("bot", response)
            return response, "knowledge"

        # ── RULE 41: Internet & Technology ────────────────────────────────────
        if self._contains_any(normalized, self.kb.INTERNET_TRIGGERS):
            response = random.choice(self.kb.INTERNET_RESPONSES)
            self._log_message("bot", response)
            return response, "technology"

        # ── RULE 42: Riddles ──────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.RIDDLE_TRIGGERS):
            response = random.choice(self.kb.RIDDLES)
            self._log_message("bot", response)
            return response, "entertainment"

        # ── RULE 43: Jokes ─────────────────────────────────────────────────────
        if self._contains_any(normalized, self.kb.JOKE_TRIGGERS):
            response = random.choice(self.kb.JOKES)
            self._log_message("bot", response)
            return response, "joke"

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

        # ── DEFAULT: Professional unknown input fallback ───────────────────────
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
