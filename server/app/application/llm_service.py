from collections.abc import Generator

from domain import PromptBuilder
from domain import PromptType

from .policies.llm_policy import LLMPolicy 

from infrastructure import OllamaClient


class LLMService:
    def __init__(self, prompt_builder: PromptBuilder, ollama_client: OllamaClient, options_policy: LLMPolicy):
        self.prompt_builder = prompt_builder
        self.ollama_client = ollama_client
        self.options_policy = options_policy


    def generate(self, prompt_type: PromptType, content: str) -> str:
        prompt = self.prompt_builder.build(
            type = prompt_type, 
            text = content
        )

        options = self.options_policy.build_options(prompt_type)

        return self.ollama_client.generate(
            prompt = prompt, 
            options = options.to_dict()
        )


    def stream(self, prompt_type: PromptType, content: str) -> Generator[str]  :
        prompt = self.prompt_builder.build(
            type = prompt_type,
            text = content
        )

        options = self.options_policy.build_options(prompt_type)

        yield from self.ollama_client.stream(
            prompt = prompt, 
            options = options.to_dict()
        )
