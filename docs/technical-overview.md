# Technical Overview

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│   In-Memory     │───▶│   TinyLlama     │
│   (app.py)      │    │   Cache         │    │   Model         │
│                 │    │   (cache.py)    │    │   (llm.py)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Router    │    │   TTL-based     │    │  ctransformers  │
│   (router.py)   │    │   Expiration    │    │   Inference     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components

### 1. FastAPI Application (`app.py`)
- Main application entry point
- CORS middleware configuration
- Server initialization

### 2. API Router (`src/router.py`)
- RESTful endpoint definitions
- Error handling and HTTP status codes
- Cache integration

### 3. LLM Service (`src/llm.py`)
- Thread-safe model loading/unloading
- Text generation using ctransformers
- TinyLlama GGUF model integration

### 4. Cache System (`src/cache.py`)
- In-memory OrderedDict implementation
- TTL-based expiration
- Thread-safe operations

## Data Flow

1. **Request Processing**

2. **Cache Lookup**

3. **Text Generation**

4. **Response Caching**

## Error Handling

### Error Types
- **Model Loading Errors**: Handled with graceful fallback
- **Generation Errors**: Logged and returned as 503 status
- **Cache Errors**: Non-blocking, logged but don't affect operation
- **Validation Errors**: Form data validation with FastAPI

## Test Coverage

| File | Test File | Coverage |
|------|-----------|----------|
| **app.py** | app_test.py |  All endpoints, error cases |
| **router.py** | router_test.py |  All endpoints, error cases |
| **cache.py** | cache_test.py | All methods |
| **llm.py** | Indirect | Via application |

## Performance Considerations

### Memory Usage
- Model size: ~638MB (TinyLlama GGUF)
- Cache memory: Variable based on usage

## Lessons Learned

- **GGUF Format**: Quantized model for reduced memory footprint
- **AWS Deployment**: Deploy with ECR and App Runner
- **LRU Cache**: Cache helps to boost performance and reduce usage

## Future Improvements
- **Model Registry**: Dynamic model loading from external sources
- **GPU Support**: CUDA acceleration for faster inference
- **Scaling**: Multiple instances with load balancer
