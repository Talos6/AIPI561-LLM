from fastapi import APIRouter, HTTPException, Form
from src.cache import Cache
from src.llm import llm
import json
import logging
import hashlib

logger = logging.getLogger(__name__)
router = APIRouter()
cache = Cache()

def create_cache_key(prompt):
    key_data = {
        "prompt": prompt
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_string.encode()).hexdigest()

@router.post("/ask")
async def generate_text(prompt = Form(...)):
    if not llm.is_model_loaded():
        raise HTTPException(
            status_code=503,
            detail="LLM is not available. Model may not be loaded."
        )

    cache_key = create_cache_key(prompt)
    
    cached_response = cache.get(cache_key)
    
    if cached_response:
        logger.info(f"Cache hit for key: {cache_key[:16]}...")
        cached_data = json.loads(cached_response)
        return {
            "response": cached_data,
            "cached": True
        }

    try:
        logger.info(f"Generating text with prompt: {prompt[:50]}...")
        result = llm.generate_text(prompt)
        logger.info(f"Caching response for key: {cache_key[:16]}...")
        cache.set(cache_key, json.dumps(result))
        
        return {
            "response": result,
            "cached": False
        }
        
    except RuntimeError as e:
        logger.error(f"LLM error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"LLM error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.post("/model/load")
async def load_model():
    try:
        if llm.is_model_loaded():
            return {"message": "Model already loaded", "loaded": True}
        
        success = llm.load_model()
        if success:
            return {"message": "Model loaded successfully", "loaded": True}
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to load model"
            )
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error loading model: {str(e)}"
        )

@router.post("/model/unload")
async def unload_model():
    try:
        llm.unload_model()
        return {"message": "Model unloaded successfully", "loaded": False}
    except Exception as e:
        logger.error(f"Error unloading model: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error unloading model: {str(e)}"
        )

@router.delete("/cache")
async def clear_cache():
    try:
        cache.clear()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )