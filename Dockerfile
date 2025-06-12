# Use Ubuntu as base for Ollama support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3.10-venv \
    build-essential \
    curl \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create and activate virtual environment
RUN python3.10 -m venv /opt/venv

# Copy requirements first for better cache utilization
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Install Ollama (but don't start it yet)
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Expose port
EXPOSE 8000

# Create startup script that handles Ollama and model download
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama service..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "Waiting for Ollama to start..."\n\
for i in {1..30}; do\n\
    if curl -s http://localhost:11434/api/health > /dev/null 2>&1; then\n\
        break\n\
    fi\n\
    echo "Waiting for Ollama... ($i/30)"\n\
    sleep 2\n\
done\n\
\n\
# Download model if not already present\n\
echo "Checking for model..."\n\
if ! ollama list | grep -q tinyllama; then\n\
    echo "Downloading tinyllama model..."\n\
    ollama pull tinyllama\n\
fi\n\
\n\
echo "Starting FastAPI application..."\n\
exec python3 src/main.py' > start.sh && \
chmod +x start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["./start.sh"]