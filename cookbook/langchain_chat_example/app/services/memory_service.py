"""
Memory service for managing conversation summaries.
Handles loading and saving of conversation context using Redis.
"""
from fastapi import HTTPException
from app.dependencies import get_summary_history


async def load_summary(session_id: str) -> str:
    """
    Load the conversation summary for a given session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        str: The conversation summary, or empty string if none exists
        
    Raises:
        HTTPException: If Redis operation fails
    """
    try:
        history = get_summary_history(session_id)
        messages = history.messages
        
        if not messages:
            return ""
        
        # Return the last AI message as the summary
        return messages[-1].content.strip() if messages[-1].content else ""
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load summary: {str(e)}"
        )


async def save_summary(session_id: str, summary: str) -> None:
    """
    Save a conversation summary for a given session.
    Avoids redundant writes if the summary hasn't changed.
    
    Args:
        session_id: Unique session identifier
        summary: The summary text to save
        
    Raises:
        HTTPException: If Redis operation fails
    """
    if not summary or summary.strip() == "":
        return  # Don't save empty summaries
    
    try:
        history = get_summary_history(session_id)
        
        # Optimize: Check if summary has changed before writing
        current_summary = await load_summary(session_id)
        if current_summary == summary.strip():
            return
        
        # Clear old summary and save new one
        history.clear()
        history.add_ai_message(summary.strip())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save summary: {str(e)}"
        )
