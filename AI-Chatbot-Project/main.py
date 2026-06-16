"""
main.py - ARIA CLI Chatbot Entry Point
=======================================
Beautiful terminal-based interface for ARIA (Artificial Rule-based
Intelligent Assistant). Implements a continuous conversation loop
with rich formatting and session analytics.

Usage:
    python main.py
    python main.py --no-color   (disable colors)
    python main.py --save       (auto-save session log)

Author: DecodeLabs AI Engineering Team
Project: AI Chatbot Project 1 - Rule-Based AI
Batch: 2026
"""

import os
import sys
import time
import argparse
import textwrap
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.brain import ChatBot
from src.logger import ConversationLogger


# ==============================================================================
# TERMINAL COLORS (ANSI escape codes)
# ==============================================================================

class Colors:
    """ANSI color codes for beautiful terminal output."""
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    
    # Foreground colors
    RED      = "\033[91m"
    GREEN    = "\033[92m"
    YELLOW   = "\033[93m"
    BLUE     = "\033[94m"
    MAGENTA  = "\033[95m"
    CYAN     = "\033[96m"
    WHITE    = "\033[97m"
    GRAY     = "\033[90m"
    
    # Background colors
    BG_BLUE  = "\033[44m"
    BG_CYAN  = "\033[46m"
    BG_GREEN = "\033[42m"

    @classmethod
    def disable(cls):
        """Disable all colors (for non-color terminals)."""
        for attr in dir(cls):
            if not attr.startswith("_") and isinstance(getattr(cls, attr), str):
                setattr(cls, attr, "")


C = Colors()


# ==============================================================================
# DISPLAY UTILITIES
# ==============================================================================

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_slowly(text: str, delay: float = 0.008):
    """Print text character by character for a typing effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def print_separator(char: str = "─", width: int = 65, color: str = ""):
    """Print a styled separator line."""
    print(f"{color}{char * width}{C.RESET}")


def wrap_text(text: str, width: int = 60, indent: str = "  ") -> str:
    """Word-wrap long response text."""
    lines = text.split("\n")
    wrapped = []
    for line in lines:
        if len(line) > width:
            wrapped.extend(textwrap.wrap(line, width, subsequent_indent=indent))
        else:
            wrapped.append(line)
    return "\n".join(wrapped)


def print_banner():
    """Print the ARIA welcome banner."""
    clear_screen()
    banner = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║   {C.WHITE}  █████╗ ██████╗ ██╗ █████╗ {C.CYAN}                              ║
  ║   {C.WHITE} ██╔══██╗██╔══██╗██║██╔══██╗{C.CYAN}                              ║
  ║   {C.WHITE} ███████║██████╔╝██║███████║{C.CYAN}                              ║
  ║   {C.WHITE} ██╔══██║██╔══██╗██║██╔══██║{C.CYAN}                              ║
  ║   {C.WHITE} ██║  ██║██║  ██║██║██║  ██║{C.CYAN}                              ║
  ║   {C.WHITE} ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝{C.CYAN}                             ║
  ║                                                              ║
  ║   {C.YELLOW}Artificial Rule-based Intelligent Assistant{C.CYAN}                 ║
  ║   {C.GREEN}Rule-Based AI Chatbot • DecodeLabs Project 1{C.CYAN}               ║
  ║   {C.GRAY}Batch 2026 • AI Engineering Track{C.CYAN}                           ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝
{C.RESET}"""
    print(banner)


def print_user_prompt(user_name: str | None = None) -> str:
    """Display and get user input with a styled prompt."""
    name_display = f"{C.GREEN}{user_name}{C.RESET}" if user_name else f"{C.GREEN}You{C.RESET}"
    timestamp = f"{C.GRAY}[{datetime.now().strftime('%H:%M')}]{C.RESET}"
    print(f"\n{timestamp} {C.BOLD}{name_display}{C.RESET}{C.GREEN} ›{C.RESET} ", end="")
    return input()


def print_bot_response(response: str, category: str):
    """Display the bot's response with category-based styling."""
    # Choose color based on category
    category_colors = {
        "greeting":     C.CYAN,
        "farewell":     C.MAGENTA,
        "smalltalk":    C.YELLOW,
        "identity":     C.BLUE,
        "help":         C.WHITE,
        "ai_knowledge": C.CYAN,
        "python":       C.GREEN,
        "joke":         C.YELLOW,
        "motivation":   C.MAGENTA,
        "math":         C.GREEN,
        "time":         C.CYAN,
        "date":         C.CYAN,
        "weather":      C.BLUE,
        "thanks":       C.GREEN,
        "about":        C.CYAN,
        "unknown":      C.GRAY,
        "error":        C.RED,
        "meta":         C.WHITE,
        "personal":     C.YELLOW,
    }
    color = category_colors.get(category, C.WHITE)
    
    timestamp = f"{C.GRAY}[{datetime.now().strftime('%H:%M')}]{C.RESET}"
    print(f"\n{timestamp} {C.BOLD}{C.BLUE}🤖 ARIA{C.RESET} {C.BLUE}›{C.RESET}")
    
    print_separator("─", 65, C.GRAY)
    
    # Print response with wrapping
    for line in response.split("\n"):
        if line.strip():
            print(f"  {color}{line}{C.RESET}")
        else:
            print()
    
    print_separator("─", 65, C.GRAY)


def print_session_stats(stats: dict):
    """Display session statistics at the end."""
    print(f"\n{C.CYAN}{C.BOLD}{'═' * 65}{C.RESET}")
    print(f"{C.YELLOW}{C.BOLD}  📊 SESSION SUMMARY{C.RESET}")
    print(f"{C.CYAN}{'─' * 65}{C.RESET}")
    print(f"  {C.WHITE}User        :{C.RESET} {C.GREEN}{stats['user_name']}{C.RESET}")
    print(f"  {C.WHITE}Started     :{C.RESET} {stats['session_start']}")
    print(f"  {C.WHITE}Duration    :{C.RESET} {stats['duration']}")
    print(f"  {C.WHITE}Messages    :{C.RESET} {C.CYAN}{stats['messages']}{C.RESET} total exchanges")
    print(f"{C.CYAN}{'═' * 65}{C.RESET}\n")


# ==============================================================================
# MAIN CONVERSATION LOOP
# ==============================================================================

def run_chatbot(save_logs: bool = False):
    """
    Main chatbot loop — the continuous conversation engine.
    
    Implements:
    - Continuous input loop (while True)
    - If-else based response routing via ChatBot.get_response()
    - Farewell detection for clean exit
    - Session logging and statistics
    """
    print_banner()
    
    # Initialize core engine
    bot = ChatBot(name="ARIA")
    logger = ConversationLogger(log_dir="logs") if save_logs else None
    
    print(f"  {C.GREEN}✓ ARIA engine initialized{C.RESET}")
    print(f"  {C.GREEN}✓ Knowledge base loaded{C.RESET}")
    print(f"  {C.GREEN}✓ Conversation loop started{C.RESET}")
    print(f"\n  {C.YELLOW}💡 Type 'help' for a list of topics, 'bye' to exit{C.RESET}")
    print_separator("─", 65, C.GRAY)
    
    # Opening message
    time.sleep(0.5)
    opening = "Hello! I'm ARIA 🤖 — your Artificial Rule-based Intelligent Assistant!\nI'm DecodeLabs Project 1. I demonstrate rule-based AI through control flow and decision trees.\nWhat's your name? Or just start chatting — type 'help' to see what I know!"
    print_bot_response(opening, "greeting")

    # ── CONTINUOUS CONVERSATION LOOP ───────────────────────────────────────────
    while True:
        try:
            user_input = print_user_prompt(bot.user_name)

            # Handle special CLI commands
            if user_input.lower().strip() == "clear":
                print_banner()
                continue

            if user_input.lower().strip() == "stats":
                stats = bot.get_stats()
                print_session_stats(stats)
                continue

            # Get response from rule-based engine
            response, category = bot.get_response(user_input)

            # Display the response
            print_bot_response(response, category)

            # Check for farewell — exit the loop
            if category == "farewell":
                stats = bot.get_stats()
                print_session_stats(stats)
                
                if save_logs and logger:
                    log_path = logger.save_session(
                        bot.conversation_history, stats
                    )
                    print(f"  {C.GREEN}💾 Session saved to: {log_path}{C.RESET}\n")
                
                print(f"  {C.GRAY}Thank you for using ARIA — DecodeLabs AI Project 1{C.RESET}\n")
                break

        except KeyboardInterrupt:
            print(f"\n\n  {C.YELLOW}⚠  Interrupted by user (Ctrl+C){C.RESET}")
            stats = bot.get_stats()
            print_session_stats(stats)
            
            if save_logs and logger:
                log_path = logger.save_session(bot.conversation_history, stats)
                print(f"  {C.GREEN}💾 Session saved to: {log_path}{C.RESET}")
            
            print(f"\n  {C.GRAY}Goodbye! — DecodeLabs ARIA{C.RESET}\n")
            break

        except EOFError:
            # Handle piped input ending
            break


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ARIA — Artificial Rule-based Intelligent Assistant\nDecodeLabs AI Project 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                  # Start ARIA chatbot
  python main.py --save           # Start with session logging
  python main.py --no-color       # Start without ANSI colors
        """
    )
    parser.add_argument(
        "--no-color", action="store_true",
        help="Disable ANSI color output (for unsupported terminals)"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save conversation session to logs/ folder"
    )
    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    run_chatbot(save_logs=args.save)


if __name__ == "__main__":
    main()
