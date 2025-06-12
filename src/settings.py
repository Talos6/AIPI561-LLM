from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # API Settings
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))
    debug_mode: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # Model Settings
    ollama_model: str = os.getenv("OLLAMA_MODEL", "tinyllama")
    ollama_api_url: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "60"))  # Increased timeout

    # Cache Settings
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = False