# Deployment Guide

This guide walks through deploying the LLM API to AWS using AWS App Runner and integrating with AWS Bedrock.

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Docker installed locally (optional)
4. Git repository access

## Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file with your configuration:
```bash
# API Settings
DEBUG_MODE=false
PORT=8000

# Model Settings
USE_BEDROCK=true
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

## AWS Infrastructure Setup

1. Create an AWS App Runner service:
   - Go to AWS Console > App Runner
   - Click "Create service"
   - Choose source code repository or container image
   - Configure the service using the provided `apprunner.yaml`

2. Create a Redis instance using AWS ElastiCache:
```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id llm-api-cache \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

3. Configure AWS Bedrock access:
   - Enable AWS Bedrock in your AWS account
   - Grant necessary permissions to App Runner service role
   - Configure model access for Claude v2

## Deployment Steps

1. Push your code to the repository:
```bash
git add .
git commit -m "Prepare for App Runner deployment"
git push
```

2. Deploy using AWS App Runner:
   - App Runner will automatically detect the `apprunner.yaml` configuration
   - Configure environment variables in App Runner console
   - Deploy the service

3. Configure custom domain (optional):
   - Add domain in App Runner console
   - Configure DNS records
   - Enable HTTPS

## Monitoring and Maintenance

1. Monitor using AWS CloudWatch:
   - Application logs
   - API metrics
   - Error rates
   - Resource utilization

2. Set up CloudWatch alarms for:
   - Application errors
   - High latency
   - Resource constraints

3. Regular maintenance:
   - Update dependencies
   - Monitor costs
   - Review security settings

## Security Best Practices

1. Application Security:
   - Implement API authentication
   - Use HTTPS endpoints
   - Rate limiting

2. AWS Security:
   - Use IAM roles with least privilege
   - Enable AWS WAF
   - Regular security audits

3. Data Security:
   - Encrypt data in transit
   - Secure environment variables
   - Regular backup strategy

## Local Development with Ollama

For local development or when Bedrock is not needed:

1. Install Ollama:
```bash
curl https://ollama.ai/install.sh | sh
```

2. Pull TinyLlama model:
```bash
ollama pull tinyllama
```

3. Set environment variables:
```bash
USE_BEDROCK=false
OLLAMA_MODEL=tinyllama
```

4. Run the application:
```bash
python src/main.py
```

## Support and Resources

- AWS App Runner Documentation
- AWS Bedrock Documentation
- Ollama Documentation
- Project Issues Tracker