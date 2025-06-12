# Use Ubuntu as base for Ollama support
FROM ubuntu:22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.9 \
    python3-pip \
    python3.9-venv \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create and activate virtual environment
RUN python3.9 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better cache utilization
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Install Ollama and download model
RUN curl https://ollama.ai/install.sh | sh
RUN ollama serve & sleep 5 && ollama pull tinyllama

# Expose port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
python3 src/main.py' > start.sh && \
chmod +x start.sh

# Run the application
CMD ["./start.sh"]