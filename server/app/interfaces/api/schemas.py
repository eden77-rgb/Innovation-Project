from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from domain import PromptType

class GenerateRequest(BaseModel):
    prompt_type: PromptType
    content: str


class GenerateResponse(BaseModel):
    resultat: str
