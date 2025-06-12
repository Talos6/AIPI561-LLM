from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests
from typing import List, Optional
from cache import Cache
from settings import Settings
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
settings = Settings()
cache = Cache()

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
            f"{settings.ollama_api_url}/api/version",
            timeout=10
        )
        response.raise_for_status()
        logger.info("Ollama health check passed")
        return True
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
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
        logger.info(f"Cache hit for key: {cache_key[:50]}...")
        return GenerateResponse(
            text=cached_response,
            model=model,
            cached=True
        )

    try:
        logger.info(f"Generating text with model: {model}")
        
        # Use Ollama
        response = requests.post(
            f"{settings.ollama_api_url}/api/generate",
            json={
                "model": model,
                "prompt": request.prompt,
                "options": {
                    "num_predict": request.max_tokens,
                    "temperature": request.temperature
                },
                "stream": False
            },
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
        
        response_data = response.json()
        logger.info(f"Ollama response: {response_data}")
        
        generated_text = response_data.get("response", "")
        if not generated_text:
            raise HTTPException(
                status_code=500,
                detail="No response generated from Ollama"
            )
        
        # Cache the response
        if cache.set(cache_key, generated_text):
            logger.info(f"Cached response for key: {cache_key[:50]}...")
        else:
            logger.warning("Failed to cache response")
        
        return GenerateResponse(
            text=generated_text,
            model=model,
            cached=False
        )
    except requests.exceptions.Timeout:
        logger.error("Request to Ollama timed out")
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating text: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/models", response_model=List[str])
async def list_models():
    try:
        response = requests.get(
            f"{settings.ollama_api_url}/api/tags",
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
        data = response.json()
        models = [model.get("name", "") for model in data.get("models", [])]
        
        if not models:
            return [settings.ollama_model]  # Return default model if no others found
            
        return models
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
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
        "cache": cache_healthy,
        "cache_type": "memory"
    }

@router.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    return cache.get_stats()