# API Documentation

## Base URL
- Local: `http://localhost:8000`
- Production: `https://the-app-runner-url`

## Endpoints

### Health Check Endpoints

#### GET `/`
Returns basic API status and model availability.

**Response:**
```json
{
  "message": "TINYLLAMA API is running",
  "model_loaded": true
}
```

#### GET `/health`
Health check endpoint for monitoring and load balancers.

**Response:**
```json
{
  "status": "healthy", 
  "model_loaded": true
}
```

### Text Generation

#### POST `/ask`
Generate text using the TinyLlama model.

**Parameters:**
- `prompt` (form data, required): The input text prompt

**Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "prompt=Hello, how are you?"
```

**Response:**
```json
{
  "response": "Generated text response from the model",
  "cached": false
}
```

**Error Responses:**
- `503`: LLM not available or model not loaded
- `500`: Unexpected error during generation

### Model Management

#### POST `/model/load`
Load the LLM model into memory.

**Response:**
```json
{
  "message": "Model loaded successfully",
  "loaded": true
}
```

**Error Response:**
- `500`: Failed to load model

#### POST `/model/unload`
Unload the LLM model from memory.

**Response:**
```json
{
  "message": "Model unloaded successfully", 
  "loaded": false
}
```

**Error Response:**
- `500`: Error unloading model

### Cache Management

#### DELETE `/cache`
Clear all cached responses.

**Response:**
```json
{
  "message": "Cache cleared successfully"
}
```

**Error Response:**
- `500`: Error clearing cache