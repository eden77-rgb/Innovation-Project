from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from .dependencies import get_llm_service
from .schemas import GenerateRequest, GenerateResponse

router = APIRouter()


# GET
@router.get("/health")
def read_health():
    return { "status": 200, "ok": True }

@router.get("/info")
def read_info():
    return {
        "status": 200,
        "ok": True,
        "api_version": 1,
        "ai_available": True,
        "current_model": "qwen2.5:3b"
    }


# POST
@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest, service = Depends(get_llm_service)):
    return {
        "resultat": service.generate(
            req.prompt_type, 
            req.content
        )
    }

@router.post("/stream")
def stream(req: GenerateRequest, service = Depends(get_llm_service)):
    generator = service.stream(
        req.prompt_type, 
        req.content
    )
    
    return StreamingResponse(
        generator,
        media_type="text/plain"
    )
