"""
LLM service for managing chat chains and prompts.
Handles the setup and invocation of LangChain components.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.dependencies import get_llm, get_chat_history


def create_chat_chain():
    """
    Create the main chat chain with prompt template and LLM.
    
    Returns:
        RunnableWithMessageHistory: Chat chain with message history support
    """
    # Define the chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个严格依赖工具结果的专属助手。
请返回结构化JSON，字段：analysis_result
{{
  "analysis_result": "根据用户的输入和历史对话得出分析结果"
}}
"""),
        ("system", "历史对话摘要（用于压缩长期记忆）：\n{summary}"),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{user_input}"),
    ])
    
    # Create the chain by piping prompt to LLM
    llm = get_llm()
    chat_chain = chat_prompt | llm
    
    # Wrap with message history support
    chat_chain_with_history = RunnableWithMessageHistory(
        runnable=chat_chain,
        get_session_history=get_chat_history,
        input_messages_key="user_input",
        history_messages_key="messages",
    )
    
    return chat_chain_with_history


def create_summary_chain():
    """
    Create the summary generation chain.
    
    Returns:
        Runnable: Chain for generating conversation summaries
    """
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是对话记忆整理器。目标：保留未来对话需要的关键信息，避免摘要过短或丢失细节。"),
        ("human", """请基于旧摘要和最新一轮对话，生成新的【较完整】摘要。

硬性要求：
- 不能少于 500 字（如果信息不足，也要把已知信息写完整，宁可重复关键点）
- 必须包含以下栏目，缺失则写"无"：
  1) 用户画像/偏好
  2) 当前目标/需求
  3) 已确认的事实/约束（包含关键数字、接口、环境、版本）
  4) 已做过的尝试与结果（错误信息要保留原文）
  5) 待办/下一步

旧摘要：
{summary}

最新一轮对话：
用户：{user_input}
助手：{assistant_output}

输出新的摘要（中文）：""")
    ])
    
    llm = get_llm()
    return summary_prompt | llm
