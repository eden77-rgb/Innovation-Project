from pydantic import BaseModel, Field
from domain import PromptType

class GenerateRequest(BaseModel):
    prompt_type: PromptType = Field(
        ...,
        description="Type of prompt (summary, translate, rewrite)",
        examples=["translate"]
    )
    content: str = Field(
        ...,
        description="Input text to process",
        examples=["Why is the sky blue ?"]
    )


class GenerateResponse(BaseModel):
    data: str = Field(
        ...,
        description="Generated output from the LLM based on the provided prompt type and content.",
        examples=["Pourquoi le ciel est bleu ?"]
    )
