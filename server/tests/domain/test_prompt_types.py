from app.domain import PromptType


def test_prompt_type_values():
    assert PromptType.SUMMARY.value == "summary"
    assert PromptType.TRANSLATE.value == "translate"
    assert PromptType.REWRITE.value == "rewrite"
