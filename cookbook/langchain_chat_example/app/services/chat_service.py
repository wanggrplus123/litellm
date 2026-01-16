"""
Chat service for orchestrating the chat workflow.
Coordinates between LLM service and memory service.
"""
import time
from typing import Tuple
from app.services.llm_service import create_chat_chain, create_summary_chain
from app.services.memory_service import load_summary, save_summary


class ChatService:
    """Service for handling chat operations."""
    
    def __init__(self):
        self.chat_chain = create_chat_chain()
        self.summary_chain = create_summary_chain()
    
    async def process_chat(
        self,
        session_id: str,
        user_input: str,
        source_info: str
    ) -> Tuple[str, dict]:
        """
        Process a chat request with memory management.
        
        Args:
            session_id: Unique session identifier
            user_input: User's message/question
            source_info: Additional context information
            
        Returns:
            Tuple of (assistant_response, timing_info)
        """
        timing_info = {}
        
        # Step 1: Load summary
        step1_start = time.perf_counter()
        summary_text = await load_summary(session_id)
        timing_info['load_summary_ms'] = (time.perf_counter() - step1_start) * 1000
        
        print(f"\n⏱  步骤1：加载历史摘要耗时：{timing_info['load_summary_ms']:.2f} 毫秒")
        print(f"\n📜 加载的历史对话摘要：{'无摘要（首次会话）' if not summary_text else summary_text[:200]}...")
        
        # Enhance user input with source info if no prior summary exists
        if not summary_text and source_info:
            user_input = f"{source_info} 问题是：{user_input}"
            print(f"\n✨ 拼接sourceInfo后最终用户输入：{user_input}")
        
        # Step 2: Invoke main chat chain (core LLM call)
        step2_start = time.perf_counter()
        result_msg = await self.chat_chain.ainvoke(
            {"user_input": user_input, "summary": summary_text},
            config={"configurable": {"session_id": session_id}},
        )
        timing_info['llm_generation_ms'] = (time.perf_counter() - step2_start) * 1000
        assistant_text = result_msg.content.strip()
        
        print(f"\n⏱  步骤2：调用主链（LLM生成）耗时：{timing_info['llm_generation_ms']:.2f} 毫秒")
        print(f"\n📝 LLM 回复结果：{assistant_text[:100]}...")
        
        # Step 3: Generate new summary
        step3_start = time.perf_counter()
        new_summary_msg = await self.summary_chain.ainvoke({
            "summary": summary_text,
            "user_input": user_input,
            "assistant_output": assistant_text
        })
        timing_info['summary_generation_ms'] = (time.perf_counter() - step3_start) * 1000
        new_summary = new_summary_msg.content.strip()
        
        print(f"\n⏱  步骤3：生成新摘要（LLM）耗时：{timing_info['summary_generation_ms']:.2f} 毫秒")
        
        # Step 4: Save summary
        step4_start = time.perf_counter()
        await save_summary(session_id, new_summary)
        timing_info['save_summary_ms'] = (time.perf_counter() - step4_start) * 1000
        
        print(f"\n⏱  步骤4：保存新摘要（Redis）耗时：{timing_info['save_summary_ms']:.2f} 毫秒")
        
        return assistant_text, timing_info


# Global service instance
chat_service = ChatService()
