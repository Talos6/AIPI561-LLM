from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug_mode: bool = False

    # Model Settings
    use_bedrock: bool = False  # Disabled by default
    ollama_model: str = "tinyllama"  # Using a smaller model by default
    ollama_api_url: str = "http://localhost:11434"
    ollama_timeout: int = 30  # Timeout in seconds for Ollama API calls

    # Redis Settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    cache_ttl: int = 3600  # 1 hour

    # AWS Settings (kept for compatibility but not used by default)
    aws_region: str = "us-east-1"

    class Config:
        env_file = ".env"