# Quick Reference Guide

## Commands

### Development
```bash
# Start development server with auto-reload
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload

# With custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Production
```bash
# Single worker
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Multiple workers (recommended)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```bash
# Build image
docker build -t langchain-chat-app .

# Run container
docker run -p 8000:8000 --env-file .env langchain-chat-app

# Docker Compose
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f app    # View logs
docker-compose ps             # Check status
```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```bash
GET /health
```

#### Root Info
```bash
GET /
```

#### Chat
```bash
POST /chat
Content-Type: application/json

{
  "question": "Your question here",
  "sessionID": "unique-session-id",
  "sourceInfo": "Optional context"
}
```

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Required:
- `DASHSCOPE_API_KEY` - Your DashScope API key for ChatTongyi

Optional:
- `REDIS_URL` - Redis connection URL (default: localhost)
- `LLM_MODEL` - Model name (default: qwen-turbo)
- `LLM_TEMPERATURE` - Temperature setting (default: 0.3)

## Testing

### Manual Testing with cURL
```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hello",
    "sessionID": "test-001",
    "sourceInfo": "Test"
  }'
```

### Using Python Script
```bash
python example_usage.py
```

## Troubleshooting

### Redis Connection Error
```bash
# Check Redis status
redis-cli ping

# Start Redis (Docker)
docker run -d -p 6379:6379 redis:7-alpine

# Start Redis (local)
redis-server
```

### Module Import Errors
```bash
# Ensure you're in the correct directory
cd cookbook/langchain_chat_example

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)

# Or use a different port
uvicorn app.main:app --port 8080
```

## Project Structure

```
app/
├── main.py              # Entry point
├── config.py            # Configuration
├── models.py            # Pydantic models
├── dependencies.py      # DI container
├── routers/
│   └── chat.py         # Chat endpoint
└── services/
    ├── chat_service.py     # Orchestration
    ├── memory_service.py   # Memory management
    └── llm_service.py      # LLM setup
```

## Customization

### Change LLM Provider
Edit `app/dependencies.py`:
```python
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(model="gpt-4")
```

### Modify Prompts
Edit `app/services/llm_service.py`:
```python
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom prompt"),
    # ...
])
```

### Add New Endpoint
1. Create new file in `app/routers/`
2. Define router with endpoints
3. Include in `app/main.py`

## Monitoring

### Logs
Application logs are printed to stdout with timing information:
```
⏱  步骤1：加载历史摘要耗时：12.34 毫秒
⏱  步骤2：调用主链（LLM生成）耗时：1234.56 毫秒
⏱  步骤3：生成新摘要（LLM）耗时：890.12 毫秒
⏱  步骤4：保存新摘要（Redis）耗时：5.67 毫秒
🎉  本次请求整体耗时：2143.69 毫秒
```

### Response includes timing
```json
{
  "total_cost_ms": 2143.69
}
```

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/docs/)
