# ARIA Architecture Document
# DecodeLabs AI Project 1 — System Design

## Overview

ARIA implements a classic **rule-based expert system** — the historical foundation of AI research, dating back to LISP programs of the 1960s. Before neural networks dominated the field, all AI was programmed this way.

## Component Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        ARIA SYSTEM                             │
│                                                                │
│  ┌──────────┐     ┌─────────────┐     ┌──────────────────┐    │
│  │   User   │────►│  Interface  │────►│   ChatBot Engine │    │
│  │          │◄────│  (CLI/Web)  │◄────│   (brain.py)     │    │
│  └──────────┘     └─────────────┘     └──────────────────┘    │
│                          │                      │              │
│                          │             ┌─────────────────┐     │
│                          │             │  KnowledgeBase  │     │
│                          │             │  (Triggers +    │     │
│                          │             │   Responses)    │     │
│                          │             └─────────────────┘     │
│                          │                                     │
│                   ┌──────▼──────┐                              │
│                   │   Logger    │                              │
│                   │  (logs/)    │                              │
│                   └─────────────┘                              │
└────────────────────────────────────────────────────────────────┘
```

## Decision Flow

```
Input → Normalize → Match Rules (Priority Order) → Select Response → Return
```

### Rule Priority Rationale

1. **Empty input** (highest) — Must catch before any processing
2. **Username detection** — Should capture name before any other rule
3. **Farewell** — Safety: always let users exit cleanly
4. **Greeting** — Most common first message type
5. **How are you** — Common follow-up to greetings
6. **Identity** — Users want to know who they're talking to
7. **Help** — Meta command for discovery
8. **History** — Meta command for session review
9. **Time/Date** — Factual queries
10. **Math** — Computational queries
11. **AI/Python Knowledge** — Domain knowledge
12. **Weather** — External data redirect
13. **Jokes** — Entertainment
14. **Motivation** — Emotional support
15. **Thanks** — Gratitude acknowledgment
16. **DecodeLabs info** — Brand information
17. **Unknown** (lowest) — Default fallback

## Key Design Decisions

### 1. Substring Matching vs. Exact Match
Using `trigger in normalized_text` (substring) rather than exact match allows natural language flexibility:
- "can you tell me a joke please" → matches "joke"
- "I want some motivation" → matches "motivation"

### 2. Random Response Selection
Each category has multiple responses. `random.choice()` gives variety and prevents the bot from feeling robotic.

### 3. Return Tuple Pattern
`get_response()` returns `(response, category)` — the category enables:
- UI color coding
- Analytics tracking
- Farewell detection

### 4. Input Normalization Pipeline
```
raw → lowercase → remove_punctuation → collapse_whitespace → normalized
```
This handles: "Hello!!!" → "hello", "BYE." → "bye"

## Scalability Path

This architecture can be extended to:
1. **Intent Classification ML** → Replace if-else with a trained classifier
2. **Entity Recognition** → Extract structured data (dates, names, numbers)
3. **Dialogue State Tracking** → Multi-turn conversation context
4. **External APIs** → Real weather, news, database queries
5. **Large Language Models** → GPT-style generation as fallback
