from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from src.router import router
from src.llm import llm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="TINYLLAMA API",
    description="API for text generation using tinyllama"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "TINYLLAMA API is running",
        "model_loaded": llm.is_model_loaded()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": llm.is_model_loaded()
    }

if __name__ == "__main__":
    logger.info(f"Starting application on 0.0.0.0:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000)