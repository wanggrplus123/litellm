"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    question: str = Field(..., description="User's question or message")
    sessionID: str = Field(..., description="Unique session identifier for conversation history")
    sourceInfo: str = Field(default="", description="Additional context or source information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the weather like today?",
                "sessionID": "user-123-session-456",
                "sourceInfo": "User from mobile app"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    sessionID: str = Field(..., description="Session identifier echoed from request")
    question: str = Field(..., description="Original question echoed from request")
    answer: str = Field(..., description="AI assistant's response")
    total_cost_ms: float = Field(..., description="Total request processing time in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sessionID": "user-123-session-456",
                "question": "What is the weather like today?",
                "answer": "I don't have real-time weather data...",
                "total_cost_ms": 1234.56
            }
        }
