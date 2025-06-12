# Local LLM API with Ollama

A FastAPI-based service that provides text generation using Ollama's local LLM models, with in-memory caching and AWS App Runner deployment.

## Features

- 🤖 Local LLM text generation using Ollama (tinyllama model)
- 🗄️ Simple in-memory caching to avoid duplicate questions
- 🚀 FastAPI with automatic API documentation
- 🐳 Docker containerization for easy deployment
- ☁️ AWS App Runner ready deployment
- 🔍 Comprehensive health checks and monitoring
- 📊 Cache statistics and debugging tools

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama**
   ```bash
   # On macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull the model
   ollama pull tinyllama
   ```

3. **Run the Application**
   ```bash
   python src/main.py
   ```

4. **Test the API**
   ```bash
   # Health check
   curl http://localhost:8000/v1/health
   
   # Generate text
   curl -X POST "http://localhost:8000/v1/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?", "max_tokens": 100}'
   ```

### Docker Deployment

1. **Build the Image**
   ```bash
   docker build -t local-llm-api .
   ```

2. **Run the Container**
   ```bash
   docker run -p 8000:8000 local-llm-api
   ```

### AWS App Runner Deployment

1. **Connect your GitHub repository to AWS App Runner**
2. **Use the provided `apprunner.yaml` configuration**
3. **Set required environment variables**
4. **Deploy with 4+ vCPU and 8+ GB RAM**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions and troubleshooting.

## API Endpoints

### Text Generation
- **POST** `/v1/generate` - Generate text using the LLM
  ```json
  {
    "prompt": "Your prompt here",
    "max_tokens": 100,
    "temperature": 0.7,
    "model": "tinyllama"
  }
  ```

### Model Management
- **GET** `/v1/models` - List available models

### Health & Monitoring
- **GET** `/health` - Basic health check
- **GET** `/v1/health` - Detailed health check with service status
- **GET** `/v1/cache/stats` - Cache usage statistics

### API Documentation
- **GET** `/docs` - Interactive Swagger UI
- **GET** `/redoc` - ReDoc documentation

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | API server port |
| `DEBUG_MODE` | false | Enable debug mode |
| `OLLAMA_MODEL` | tinyllama | Default LLM model |
| `OLLAMA_TIMEOUT` | 60 | Ollama API timeout (seconds) |
| `CACHE_TTL` | 3600 | Cache TTL (seconds) |

## Caching Strategy

The application uses a simple in-memory caching system:

1. **In-memory cache**: Fast local caching for duplicate question detection
2. **TTL support**: Configurable cache expiration (default 1 hour)
3. **Automatic cleanup**: Expired entries are automatically removed
4. **Simple and reliable**: No external dependencies required

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│ In-Memory Cache │───▶│   Ollama LLM    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Health Checks │    │ Cache Statistics│    │  Model Download │
│   Monitoring    │    │   & Management  │    │   & Management  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Development

### Project Structure
```
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   └── router.py        # API routes and handlers
│   ├── cache/
│   │   └── redis_cache.py   # In-memory cache implementation
│   ├── config/
│   │   └── settings.py      # Configuration management
│   └── test_app.py          # Diagnostic testing script
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── Dockerfile               # Container definition
├── apprunner.yaml          # AWS App Runner configuration
├── requirements.txt        # Python dependencies
└── DEPLOYMENT.md           # Deployment guide
```

### Running Tests
```bash
# Run diagnostic tests
python src/test_app.py

# Run unit tests
pytest tests/
```

### Adding New Models

1. **Download the model**
   ```bash
   ollama pull llama2:7b
   ```

2. **Update the default model**
   ```bash
   export OLLAMA_MODEL=llama2:7b
   ```

3. **Restart the application**

## Troubleshooting

### Common Issues

1. **Ollama not starting**: Check if the service is running and accessible
2. **Model download fails**: Ensure internet connectivity and sufficient disk space
3. **Memory issues**: Use smaller models (tinyllama) or increase container memory
4. **Cache statistics**: Check `/v1/cache/stats` for cache performance

### Debug Tools

- Use `src/test_app.py` for comprehensive diagnostics
- Check `/v1/health` endpoint for service status
- Monitor logs for detailed error information
- Use `/v1/cache/stats` for cache performance

## Performance

### Recommended Resources
- **Minimum**: 4 vCPU, 8GB RAM
- **Production**: 8 vCPU, 16GB RAM

### Model Comparison
| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| tinyllama | 1.1GB | Fast | Basic |
| llama2:7b | 3.8GB | Medium | Good |
| codellama:7b | 3.8GB | Medium | Code-focused |

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
- Use the diagnostic script: `python src/test_app.py`
- Review application logs for detailed error information
