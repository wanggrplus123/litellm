# LangChain Chat Application with Memory

A production-ready FastAPI application that implements a chat interface with persistent conversation memory using LangChain, Redis, and ChatTongyi (Qwen) LLM.

## Features

- **Session-based Conversation History**: Each user session maintains its own conversation history stored in Redis
- **Automatic Memory Summarization**: Long conversations are automatically summarized to maintain context while reducing token usage
- **Modular Architecture**: Clean separation of concerns with services, routers, and configuration
- **Performance Monitoring**: Built-in timing information for each request step
- **Production-Ready**: Structured for deployment with proper error handling and logging

## Architecture

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── models.py            # Pydantic models for request/response
├── dependencies.py      # Dependency injection (LLM, Redis)
├── routers/
│   └── chat.py         # Chat endpoint router
└── services/
    ├── chat_service.py     # Chat orchestration
    ├── memory_service.py   # Memory management (summary)
    └── llm_service.py      # LLM chain setup
```

## Prerequisites

- Python 3.9+
- Redis server (for conversation history storage)
- DashScope API key (for ChatTongyi/Qwen access)

## Installation

1. Clone the repository and navigate to the application directory:
```bash
cd cookbook/langchain_chat_example
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables and gitignore (optional):
```bash
cp .env.example .env
# Edit .env with your configuration

# Optional: Set up .gitignore if you plan to initialize git in this directory
cp gitignore.example .gitignore
```

## Configuration

Edit the `.env` file with your settings:

```env
# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# LLM Configuration
DASHSCOPE_API_KEY=your-api-key-here
LLM_MODEL=qwen-turbo
LLM_TEMPERATURE=0.3
```

## Running the Application

### Development Mode

```bash
# From the cookbook/langchain_chat_example directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:
```bash
python app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or using Gunicorn with Uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Usage

### Interactive Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Chat Endpoint

**POST** `/chat`

Request body:
```json
{
  "question": "What is the weather like today?",
  "sessionID": "user-123-session-456",
  "sourceInfo": "User from mobile app"
}
```

Response:
```json
{
  "sessionID": "user-123-session-456",
  "question": "What is the weather like today?",
  "answer": "I don't have real-time weather data...",
  "total_cost_ms": 1234.56
}
```

### Example using cURL

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hello, how are you?",
    "sessionID": "test-session-001",
    "sourceInfo": "Testing from cURL"
  }'
```

### Example using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "question": "Hello, how are you?",
        "sessionID": "test-session-001",
        "sourceInfo": "Testing from Python"
    }
)
print(response.json())
```

## How It Works

1. **Memory Loading**: The system loads any existing conversation summary from Redis for the given session
2. **Context Enhancement**: If this is the first message (no prior summary), the `sourceInfo` is prepended to provide context
3. **LLM Processing**: The message is processed through the LangChain chat chain with history
4. **Summary Generation**: A new summary is generated that includes key information from the conversation
5. **Memory Saving**: The updated summary is saved back to Redis for future conversations

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t langchain-chat-app .
docker run -p 8000:8000 --env-file .env langchain-chat-app
```

### Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
    depends_on:
      - redis

volumes:
  redis_data:
```

Run with:
```bash
docker-compose up -d
```

## Performance Monitoring

The application logs timing information for each step:

```
⏱  步骤1：加载历史摘要耗时：12.34 毫秒
⏱  步骤2：调用主链（LLM生成）耗时：1234.56 毫秒
⏱  步骤3：生成新摘要（LLM）耗时：890.12 毫秒
⏱  步骤4：保存新摘要（Redis）耗时：5.67 毫秒
🎉  本次请求整体耗时：2143.69 毫秒
```

## Customization

### Changing the LLM

Edit `app/dependencies.py` to use a different LangChain chat model:

```python
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(model="gpt-4", temperature=0.3)
```

### Modifying the Prompt

Edit the prompts in `app/services/llm_service.py`:

```python
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt here"),
    # ... rest of the prompt
])
```

### Adding New Endpoints

Create a new router in `app/routers/` and include it in `app/main.py`:

```python
from app.routers import chat, new_router

app.include_router(chat.router)
app.include_router(new_router.router)
```

## Troubleshooting

### Redis Connection Issues

- Ensure Redis is running: `redis-cli ping`
- Check the `REDIS_URL` in your `.env` file
- Verify network connectivity if using a remote Redis instance

### LLM API Issues

- Verify your `DASHSCOPE_API_KEY` is valid
- Check your API quota and rate limits
- Review the logs for specific error messages

### Import Errors

- Ensure you're running from the correct directory
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.9+)

## License

This example is part of the LiteLLM project and follows the same MIT license.

## Contributing

Contributions are welcome! Please follow the standard GitHub flow:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Check the LiteLLM documentation: https://docs.litellm.ai/
- Review LangChain documentation: https://python.langchain.com/
