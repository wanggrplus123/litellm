"""
Example usage of the LangChain Chat API.

This script demonstrates how to interact with the chat API
using different methods.
"""
import requests
import json


def test_chat_api(base_url: str = "http://localhost:8000"):
    """
    Test the chat API with example requests.
    
    Args:
        base_url: Base URL of the API server
    """
    print("=" * 80)
    print("LangChain Chat API - Example Usage")
    print("=" * 80)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: First message in a new session
    print("\n2. Sending first message in a new session...")
    session_id = "example-session-001"
    
    first_message = {
        "question": "你好，我是一个软件开发者，正在学习 Python。",
        "sessionID": session_id,
        "sourceInfo": "用户是一位初级开发者，正在学习后端开发"
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=first_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Session ID: {result['sessionID']}")
        print(f"   Question: {result['question']}")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Processing time: {result['total_cost_ms']} ms")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 3: Follow-up message in the same session
    print("\n3. Sending follow-up message in the same session...")
    
    followup_message = {
        "question": "我应该从哪些Python框架开始学习？",
        "sessionID": session_id,
        "sourceInfo": ""  # Not needed for follow-up messages
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=followup_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Question: {result['question']}")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Processing time: {result['total_cost_ms']} ms")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: New session to demonstrate context isolation
    print("\n4. Starting a new session (different context)...")
    
    new_session_message = {
        "question": "我对机器学习很感兴趣。",
        "sessionID": "example-session-002",
        "sourceInfo": "用户对AI和机器学习感兴趣"
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=new_session_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Session ID: {result['sessionID']}")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Processing time: {result['total_cost_ms']} ms")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 80)
    print("Example usage completed!")
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    # Allow custom base URL from command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"\nConnecting to: {base_url}")
    print("Make sure the server is running before executing this script.")
    print("Run the server with: python app/main.py")
    print()
    
    input("Press Enter to start the tests...")
    
    test_chat_api(base_url)
