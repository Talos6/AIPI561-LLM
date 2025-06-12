from ctransformers import AutoModelForCausalLM
import logging
import threading

logger = logging.getLogger(__name__)

class LLM:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LLM, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self.model = None
        self._model_lock = threading.RLock()
        self._initialized = True
        logger.info("LLM Service initialized with ctransformers")
    
    def load_model(self):
        try:
            if self.model is not None:
                logger.info("Model already loaded")
                return True
            
            with self._model_lock:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path_or_repo_id = './src',
                    model_file = 'tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
                    model_type="llama",
                    local_files_only=True
                )
            
            logger.info("Model loaded successfully with ctransformers")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def is_model_loaded(self):
        return self.model is not None
    
    def generate_text(self, prompt):
        if not self.is_model_loaded():
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            with self._model_lock:
                logger.info(f"Generating text for prompt: {prompt[:50]}...")
                
                generated_text = self.model(
                    prompt,
                    max_new_tokens=512,
                    temperature=0.7
                )
                
                return generated_text
                
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise RuntimeError(f"Text generation failed: {str(e)}")
    
    def unload_model(self):
        with self._model_lock:
            if self.model is not None:
                del self.model
                self.model = None
                logger.info("Model unloaded")

# Global instance
llm = LLM() 