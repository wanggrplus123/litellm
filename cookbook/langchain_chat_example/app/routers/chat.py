"""
Chat router module.
Defines the chat endpoint and request handling logic.
"""
import time
from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    Chat endpoint with conversation memory and summary management.
    
    This endpoint:
    1. Loads conversation summary from Redis
    2. Processes user input through LLM with history
    3. Generates updated conversation summary
    4. Saves summary back to Redis
    5. Returns assistant response with timing information
    
    Args:
        req: Chat request containing question, sessionID, and sourceInfo
        
    Returns:
        ChatResponse: Assistant's response with timing information
        
    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    # Record overall request start time
    total_start = time.perf_counter()
    
    # Validate required fields
    if not req.sessionID or not req.question:
        raise HTTPException(
            status_code=400,
            detail="sessionID and question cannot be empty"
        )
    
    session_id = req.sessionID
    user_input = req.question.strip()
    
    # Log request information
    print("=" * 80)
    print("📌 原始请求输入信息")
    print(f"  - sessionID：{req.sessionID}")
    print(f"  - 原始问题（question）：{req.question}")
    print(f"  - 来源信息（sourceInfo）：{req.sourceInfo}")
    print(f"  - 处理后问题（去空格）：{user_input}")
    print("=" * 80)
    
    try:
        # Process chat through service layer
        assistant_text, timing_info = await chat_service.process_chat(
            session_id=session_id,
            user_input=user_input,
            source_info=req.sourceInfo
        )
        
        # Calculate total request time
        total_end = time.perf_counter()
        total_cost = (total_end - total_start) * 1000
        
        print("=" * 80)
        print(f"🎉  本次请求整体耗时：{total_cost:.2f} 毫秒")
        print("=" * 80)
        
        return ChatResponse(
            sessionID=session_id,
            question=req.question,
            answer=assistant_text,
            total_cost_ms=round(total_cost, 2)
        )
        
    except Exception as e:
        # Log error with timing information
        total_end = time.perf_counter()
        total_cost = (total_end - total_start) * 1000
        print(f"\n❌  本次请求执行失败，已耗时：{total_cost:.2f} 毫秒，错误信息：{str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )
