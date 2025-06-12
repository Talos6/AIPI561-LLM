# Local LLM Deployment with Ollama and AWS Bedrock

This project implements a flexible LLM deployment using either Ollama (for local deployment) or AWS Bedrock, with an API wrapper and caching capabilities deployed on AWS App Runner.

## Features

- Dual LLM support:
  - Local deployment using Ollama with TinyLlama (optimized for limited GPU consumption)
  - Cloud deployment using AWS Bedrock
- RESTful API wrapper
- Response caching for improved performance
- AWS App Runner deployment support
- Comprehensive documentation

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For local development with Ollama:
```bash
# Install Ollama (MacOS/Linux)
curl https://ollama.ai/install.sh | sh

# Pull the TinyLlama model (optimized for limited GPU usage)
ollama pull tinyllama
```

3. Configure environment variables:
```bash
# API Settings
DEBUG_MODE=false
PORT=8000

# Model Settings
USE_BEDROCK=true  # Set to false for local-only deployment
BEDROCK_MODEL_ID=anthropic.claude-v2
OLLAMA_MODEL=tinyllama

# Redis Settings
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# AWS Settings
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

4. Start the API server:
```bash
python src/main.py
```

## Project Structure

```
.
├── src/
│   ├── main.py              # Main application entry point
│   ├── api/                 # API implementation
│   ├── cache/              # Caching implementation
│   └── config/             # Configuration files
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── Dockerfile             # Docker configuration
├── apprunner.yaml         # AWS App Runner configuration
└── requirements.txt       # Python dependencies
```

## API Documentation

The API provides the following endpoints:

- `POST /v1/generate`: Generate text using the configured LLM (Bedrock or Ollama)
- `GET /v1/models`: List available models
- `GET /v1/health`: Health check endpoint

For detailed API documentation, see [API.md](docs/API.md)

## Performance Metrics

See [PERFORMANCE.md](docs/PERFORMANCE.md) for detailed performance metrics and benchmarks.

## Deployment Guide

This project is configured for deployment on AWS App Runner. For detailed deployment instructions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Key Deployment Features

1. AWS App Runner deployment for simplified container management
2. Integration with AWS Bedrock for scalable cloud-based inference
3. Optional local deployment using Ollama with TinyLlama for reduced GPU consumption
4. Redis caching for improved response times

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
