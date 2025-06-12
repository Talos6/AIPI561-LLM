from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests
from typing import List, Optional
from cache.redis_cache import RedisCache
from config.settings import Settings
import json

router = APIRouter()
settings = Settings()
cache = RedisCache()

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    model: Optional[str] = None  # Will use default from settings if not specified

class GenerateResponse(BaseModel):
    text: str
    model: str
    cached: bool = False

def check_ollama_health():
    try:
        response = requests.get(
            f"{settings.ollama_api_url}/api/health",
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
        return True
    except Exception:
        return False

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    if not check_ollama_health():
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available"
        )

    # Use model from request or default from settings
    model = request.model or settings.ollama_model
    
    # Try to get from cache first
    cache_key = f"{model}:{request.prompt}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        return GenerateResponse(
            text=cached_response,
            model=model,
            cached=True
        )

    try:
        # Use Ollama
        response = requests.post(
            f"{settings.ollama_api_url}/api/generate",
            json={
                "model": model,
                "prompt": request.prompt,
                "options": {
                    "num_predict": request.max_tokens,
                    "temperature": request.temperature
                }
            },
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
        generated_text = response.json()["response"]
        
        # Cache the response
        cache.set(cache_key, generated_text)
        
        return GenerateResponse(
            text=generated_text,
            model=model,
            cached=False
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating text: {str(e)}"
        )

@router.get("/models", response_model=List[str])
async def list_models():
    try:
        response = requests.get(
            f"{settings.ollama_api_url}/api/tags",
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
        models = response.json().get("models", [])
        
        if not models:
            return [settings.ollama_model]  # Return default model if no others found
            
        return models
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error fetching models: {str(e)}"
        )

@router.get("/health")
async def health_check():
    ollama_healthy = check_ollama_health()
    cache_healthy = cache.ping()
    
    if not ollama_healthy:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not healthy"
        )
        
    if not cache_healthy:
        raise HTTPException(
            status_code=503,
            detail="Cache service is not healthy"
        )
    
    return {
        "status": "healthy",
        "ollama": ollama_healthy,
        "cache": cache_healthy
    }