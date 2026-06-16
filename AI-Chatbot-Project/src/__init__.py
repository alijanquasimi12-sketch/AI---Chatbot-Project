"""
__init__.py - Source package initializer
"""
from .brain import ChatBot, KnowledgeBase
from .logger import ConversationLogger

__all__ = ["ChatBot", "KnowledgeBase", "ConversationLogger"]
__version__ = "1.0.0"
__author__ = "DecodeLabs AI Engineering Team"
