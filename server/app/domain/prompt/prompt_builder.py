from .prompt_types import PromptType
from pathlib import Path


class PromptBuilder:

    BASE_DIR = Path(__file__).resolve().parent
    TEMPLATE_DIR = BASE_DIR / "templates"

    PROMPTS = {
        PromptType.SUMMARY: "summary.txt",
        PromptType.TRANSLATE: "translate.txt",
        PromptType.REWRITE: "rewrite.txt"
    }

    @staticmethod
    def build(type: PromptType, text: str):
        file = PromptBuilder.PROMPTS[type]

        with open(PromptBuilder.TEMPLATE_DIR / file, "r", encoding="utf-8") as f:
            template = f.read()

        return template.format(input=text)
