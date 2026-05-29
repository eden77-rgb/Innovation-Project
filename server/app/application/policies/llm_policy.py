from ..dto.ollama_options import OllamaOptions
from domain import PromptType
from domain.exceptions import InvalidPromptTypeError

class LLMPolicy:
    def build_options(self, prompt_type: PromptType) -> OllamaOptions:
        match prompt_type:

            case PromptType.SUMMARY:
                return OllamaOptions(
                    temperature = 0.3,
                    top_p = 0.8,
                    num_predict = 400,
                    repeat_penalty = 1.12
                )

            case PromptType.TRANSLATE:
                return OllamaOptions(
                    temperature = 0.1,
                    top_p = 0.95,
                    num_predict = 1200,
                    repeat_penalty = 1.05
                )

            case PromptType.REWRITE:
                return OllamaOptions(
                    temperature = 0.7,
                    top_p = 0.9,
                    num_predict = 800,
                    repeat_penalty = 1.18
                )
            
            case PromptType.RESPONSE:
                return OllamaOptions(
                    temperature = 0.5,
                    top_p = 0.9,
                    num_predict = 800,
                    repeat_penalty = 1.1
                )

            case _:
                raise InvalidPromptTypeError(f"Unsupported prompt type: {prompt_type}")
