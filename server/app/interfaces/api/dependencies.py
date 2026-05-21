from application import LLMService
from application import LLMPolicy
from domain import PromptBuilder
from infrastructure import OllamaClient

def get_llm_service() -> LLMService:
    prompt_builder = PromptBuilder

    ollama_client = OllamaClient(
        'qwen2.5:3b',
        "localhost",
        0.9,
        10)

    policy = LLMPolicy()

    return LLMService(prompt_builder, ollama_client, policy)
