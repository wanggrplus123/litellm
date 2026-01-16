"""
Main FastAPI application entry point.
"""
import inspect
import langchain
from fastapi import FastAPI
from app.config import settings
from app.routers import chat

# Print LangChain version info at startup
print("langchain file:", inspect.getfile(langchain))
print("langchain version:", getattr(langchain, "__version__", "no __version__"))


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="""
        LangChain-based chat API with persistent conversation memory.
        
        Features:
        - Session-based conversation history stored in Redis
        - Automatic conversation summarization for long-term memory
        - Integration with ChatTongyi (Qwen) LLM
        - Performance timing for each request
        """
    )
    
    # Include routers
    app.include_router(chat.router)
    
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "LangChain Chat API",
            "version": settings.API_VERSION,
            "endpoints": {
                "chat": "/chat",
                "docs": "/docs",
                "redoc": "/redoc"
            }
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
