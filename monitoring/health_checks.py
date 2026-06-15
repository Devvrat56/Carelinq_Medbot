from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["monitoring"])

@router.get("/")
async def health_check():
    # Placeholder for actual health checks against DBs, Redis, LLM API
    status = {
        "status": "healthy",
        "redis": "connected",
        "chromadb": "connected",
        "neo4j": "connected"
    }
    return status
