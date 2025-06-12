# API Documentation

## Overview

The Local LLM API provides endpoints for text generation using locally deployed language models through Ollama. The API includes built-in caching for improved performance.

## Base URL

```
http://your-api-domain:8000/v1
```

## Endpoints

### Generate Text

Generate text using the local LLM.

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
    "prompt": "string",
    "max_tokens": integer (optional, default: 100),
    "temperature": float (optional, default: 0.7),
    "model": string (optional, default: "llama2")
}
```

**Response:**
```json
{
    "text": "string",
    "model": "string",
    "cached": boolean
}
```

**Example:**
```bash
curl -X POST "http://your-api-domain:8000/v1/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Write a poem about AI",
           "max_tokens": 150,
           "temperature": 0.8
         }'
```

### List Models

Get a list of available models.

**Endpoint:** `GET /models`

**Response:**
```json
[
    "string"
]
```

**Example:**
```bash
curl "http://your-api-domain:8000/v1/models"
```

### Health Check

Check the API health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
    "status": "healthy"
}
```

**Example:**
```bash
curl "http://your-api-domain:8000/health"
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Successful request
- 400: Bad request (invalid parameters)
- 404: Resource not found
- 500: Internal server error

Error responses include a detail message:
```json
{
    "detail": "Error message description"
}
```

## Rate Limiting

- Default rate limit: 60 requests per minute
- Cached responses don't count towards rate limit
- Rate limit headers included in response:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## Caching

- Responses are cached for 1 hour by default
- Cache status indicated in response `cached` field
- Cache key: `{model}:{prompt}`
- Cache can be bypassed with `Cache-Control: no-cache` header

## Security

- CORS enabled for all origins
- API key authentication available (optional)
- HTTPS recommended for production use

## Best Practices

1. Use appropriate `max_tokens` to limit response length
2. Adjust `temperature` for creativity vs. consistency
3. Implement retry logic for failed requests
4. Handle rate limits gracefully
5. Cache frequently used prompts locally