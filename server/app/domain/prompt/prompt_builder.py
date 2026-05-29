from .prompt_types import PromptType
from ..exceptions import EmptyPromptError, InvalidPromptTypeError, PromptTemplateNotFoundError
from pathlib import Path


class PromptBuilder:

    BASE_DIR = Path(__file__).resolve().parent
    TEMPLATE_DIR = BASE_DIR / "templates"

    PROMPTS = {
        PromptType.SUMMARY: "summary.txt",
        PromptType.TRANSLATE: "translate.txt",
        PromptType.REWRITE: "rewrite.txt",
        PromptType.RESPONSE: "response.txt"
    }

    @staticmethod
    def build(type: PromptType, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            print("[ERROR]: EmptyPromptError")
            raise EmptyPromptError("Prompt text cannot be empty")

        if type not in PromptBuilder.PROMPTS:
            raise InvalidPromptTypeError(f"Unsupported prompt type: {type}")
    
        file = PromptBuilder.PROMPTS[type]

        try:
            with open(PromptBuilder.TEMPLATE_DIR / file, "r", encoding="utf-8") as f:
                template = f.read()

        except FileNotFoundError:
            raise PromptTemplateNotFoundError(f"Template not found: {file}")

        return template.format(input=text)
