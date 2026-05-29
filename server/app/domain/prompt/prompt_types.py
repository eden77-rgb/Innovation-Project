from enum import Enum


class PromptType(Enum):
    SUMMARY = "summary"
    TRANSLATE = "translate"
    REWRITE = "rewrite"
    RESPONSE = "response"
    CUSTOM = "custom"
