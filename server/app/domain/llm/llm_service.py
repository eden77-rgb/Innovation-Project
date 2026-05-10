from collections.abc import Generator

from domain import PromptBuilder
from domain import PromptType

from infrastructure import OllamaClient


class LLMService:
    def __init__(self, prompt_builder: PromptBuilder, ollama_client: OllamaClient):
        self.prompt_builder = prompt_builder
        self.ollama_client = ollama_client


    def generate(self, prompt_type: PromptType, content: str) -> str:
        prompt = self.prompt_builder.build(
            prompt_type = prompt_type, 
            content = content
        )

        options = self.__build_options(prompt_type)

        return self.ollama_client.generate(
            prompt = prompt, 
            options = options.to_dict())


    def stream(self, prompt_type: PromptType, content: str) -> Generator[str]  :
        pass


    def __build_options(self, prompt_type: PromptType):
        match prompt_type:

            case PromptType.SUMMARY:
                return ...
            
            case PromptType.TRANSLATE:
                return ...
            
            case PromptType.REWRITE:
                return ...
            
            case _:
                raise ValueError(f"Unsupported prompt type: {prompt_type}")
