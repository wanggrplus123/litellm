"""
Dependency injection module for shared resources.
Provides singleton instances of LLM and Redis connections.
"""
from functools import lru_cache
from langchain_community.chat_models import ChatTongyi
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory
from app.config import settings


@lru_cache()
def get_llm() -> ChatTongyi:
    """
    Get or create a singleton ChatTongyi LLM instance.
    
    Returns:
        ChatTongyi: Configured LLM instance
    """
    return ChatTongyi(
        model=settings.LLM_MODEL,
        api_key=settings.DASHSCOPE_API_KEY,
        temperature=settings.LLM_TEMPERATURE,
    )


def get_chat_history(session_id: str) -> RedisChatMessageHistory:
    """
    Get Redis chat message history for a given session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        RedisChatMessageHistory: Redis-backed message history
    """
    return RedisChatMessageHistory(
        session_id=session_id,
        url=settings.REDIS_URL
    )


def get_summary_history(session_id: str) -> RedisChatMessageHistory:
    """
    Get Redis history for storing conversation summaries.
    Uses a prefixed session ID to separate summaries from regular messages.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        RedisChatMessageHistory: Redis-backed summary storage
    """
    return RedisChatMessageHistory(
        session_id=f"{settings.SUMMARY_KEY_PREFIX}{session_id}",
        url=settings.REDIS_URL
    )
