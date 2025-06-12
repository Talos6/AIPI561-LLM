# Deployment Guide for Local LLM API

## Overview

This project provides an API service that uses:
- Ollama for local LLM text generation (tinyllama model)
- Simple in-memory cache to avoid duplicate questions
- FastAPI for the REST API
- AWS App Runner for deployment

## AWS App Runner Deployment

### Prerequisites

1. AWS CLI configured with appropriate permissions
2. GitHub repository connected to AWS App Runner
3. Docker support enabled

### Configuration

The `apprunner.yaml` file configures the deployment:

```yaml
version: 1.0
runtime: docker
build:
  commands:
    pre-build:
      - echo "Pre-build phase - App Runner will handle Docker build"
    build:
      - echo "Build phase - Using Dockerfile"
run:
  runtime-version: latest
  command: ./start.sh
  network:
    port: 8000
  env:
    - name: DEBUG_MODE
      value: "false"
    - name: PORT
      value: "8000"
    - name: OLLAMA_MODEL
      value: "tinyllama"
    - name: CACHE_TTL
      value: "3600"
instance:
  cpu: 4
  memory: 8192
```

### Environment Variables

- `DEBUG_MODE`: Set to "true" for development
- `PORT`: Application port (default: 8000)
- `OLLAMA_MODEL`: LLM model to use (default: tinyllama)
- `OLLAMA_TIMEOUT`: Timeout for Ollama API calls (default: 60s)
- `CACHE_TTL`: Cache TTL in seconds (default: 3600)

## Troubleshooting

### Common Issues

1. **App Runner Creation Failed with No Event Logs**
   - Check if the repository has the correct `apprunner.yaml` file
   - Ensure Docker runtime is properly configured
   - Verify instance resources (CPU/Memory) are sufficient
   - Check AWS App Runner service limits

2. **Ollama Service Not Starting**
   - Increase startup timeout in health checks
   - Check if tinyllama model downloads successfully
   - Monitor container logs for Ollama service errors
   - Ensure sufficient memory allocation (8GB recommended)

3. **Model Download Failures**
   - Check internet connectivity in the container
   - Verify Ollama installation completed successfully
   - Consider pre-downloading models in the Docker image

### Debugging Steps

1. **Local Testing**
   ```bash
   # Build and run locally
   docker build -t local-llm-api .
   docker run -p 8000:8000 local-llm-api
   
   # Test the API
   curl http://localhost:8000/health
   curl http://localhost:8000/v1/health
   ```

2. **Use the Test Script**
   ```bash
   python src/test_app.py
   ```

3. **Check Application Logs**
   - Enable verbose logging in App Runner
   - Monitor container startup process
   - Check Ollama service logs

4. **Health Check Endpoints**
   - `GET /health` - Basic health check
   - `GET /v1/health` - Detailed health check with Ollama and cache status
   - `GET /v1/cache/stats` - Cache statistics

### Performance Considerations

1. **Resource Requirements**
   - Minimum: 4 vCPU, 8GB RAM
   - Recommended: 8 vCPU, 16GB RAM for better performance

2. **Model Selection**
   - `tinyllama`: Fastest, smallest (1.1GB)
   - `llama2:7b`: Better quality, larger (3.8GB)
   - `codellama:7b`: Code-focused (3.8GB)

3. **Caching Strategy**
   - In-memory cache stores responses temporarily
   - Cache automatically expires after TTL (default: 1 hour)
   - Cache is process-local (lost on restart)
   - No external dependencies required

## API Usage

### Generate Text
```bash
curl -X POST "http://your-app-url/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, how are you?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

### List Models
```bash
curl "http://your-app-url/v1/models"
```

### Check Health
```bash
curl "http://your-app-url/v1/health"
```

### Cache Statistics
```bash
curl "http://your-app-url/v1/cache/stats"
```

## Security Considerations

1. **CORS Configuration**
   - Currently allows all origins for development
   - Restrict origins in production

2. **API Rate Limiting**
   - Consider implementing rate limiting
   - Monitor API usage and costs

3. **Model Access**
   - Models run locally in the container
   - No external API calls for inference
   - Data doesn't leave your AWS environment

4. **Cache Security**
   - In-memory cache is process-local
   - No persistent storage of cached data
   - Cache is cleared on application restart

## Monitoring

1. **Health Checks**
   - Application provides comprehensive health endpoints
   - Monitor both Ollama and cache services

2. **Metrics**
   - Cache statistics available via `/v1/cache/stats`
   - Application logs provide request/response details

3. **Alerts**
   - Set up CloudWatch alarms for service health
   - Monitor memory usage (Ollama can be memory-intensive)

## Simplified Architecture Benefits

1. **No External Dependencies**
   - No Redis server required
   - Simpler deployment and maintenance
   - Reduced infrastructure costs

2. **Faster Startup**
   - No network connections to establish
   - Immediate cache availability
   - Simplified error handling

3. **Easier Development**
   - No additional services to run locally
   - Simpler configuration
   - Fewer potential failure points 