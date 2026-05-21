from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from .dependencies import get_llm_service
from .schemas import GenerateRequest, GenerateResponse

router = APIRouter(tags=["LLM API"])


# GET
@router.get(
    "/health",
    summary="Health check",
    description="Simple endpoint to verify that the API is running correctly."
)
def read_health() -> dict:
    return { "status": 200, "ok": True }


@router.get(
    "/info",
    summary="API information",
    description="Returns metadata about the API, including version and AI model availability."
)
def read_info() -> dict:
    return {
        "status": 200,
        "ok": True,
        "api_version": 1,
        "ai_available": True,
        "current_model": "qwen2.5:3b"
    }


# POST
@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Generate full LLM response",
    description="Generate a complete response from the LLM based on prompt type and content."
)
def generate(req: GenerateRequest, service = Depends(get_llm_service)) -> GenerateResponse:
    response = service.generate(
        req.prompt_type,
        req.content
    )

    return {
        "data": response
    }


@router.post(
    "/stream",
    summary="Stream LLM response",
    description="Streams the LLM response token by token in real-time, based on prompt type and content.",
    responses={
        200: {
            "description": "Streaming text response",
            "content": {
                "text/plain": {
                    "schema": { "type": "string" }
                }
            }
        }
    }
)
def stream(req: GenerateRequest, service = Depends(get_llm_service)) -> StreamingResponse:
    generator = service.stream(
        req.prompt_type,
        req.content
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )
