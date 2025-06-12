# Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.10+
- Git

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AIPI561-LLM
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Test the API**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Load model
   curl -X POST http://localhost:8000/model/load
   
   # Generate text
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "prompt=Hello, how are you?"
   ```

## Docker Deployment

### Build Docker Image

1. **Build the Image**
   ```bash
   docker build -t tinyllama-api .
   ```

2. **Run Locally**
   ```bash
   docker run -p 8000:8000 tinyllama-api
   ```

3. **Test Container**
   ```bash
   curl http://localhost:8000/health
   ```

### Image Details
- Base: `python:3.10-slim`
- Size: ~2GB (includes model file)
- Port: 8000
- Health check: Built-in endpoint monitoring

## AWS ECR Deployment

### Prerequisites
- AWS CLI configured
- Docker installed
- Appropriate IAM permissions

### Push to ECR

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository \
     --repository-name tinyllama-api \
     --region us-east-1
   ```

2. **Get Login Token**
   ```bash
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     <account-id>.dkr.ecr.us-east-1.amazonaws.com
   ```

3. **Tag Image**
   ```bash
   docker tag tinyllama-api:latest \
     <account-id>.dkr.ecr.us-east-1.amazonaws.com/tinyllama-api:latest
   ```

4. **Push Image**
   ```bash
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/tinyllama-api:latest
   ```

## AWS App Runner Deployment

### Create App Runner Service

1. **Using AWS Console**
   - Go to AWS App Runner console
   - Click "Create service"
   - Choose "Container registry" as source
   - Select your ECR repository
   - Choose "Manual" deployment trigger

2. **Configure Service Settings**
   ```yaml
   Service name: tinyllama-api
   Port: 8000
   CPU: 2 vCPU (minimum)
   Memory: 4 GB (minimum)
   ```
