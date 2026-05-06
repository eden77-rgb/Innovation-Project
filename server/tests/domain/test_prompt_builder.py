import pytest
from unittest.mock import mock_open, patch
from app.domain import PromptBuilder, PromptType


def test_build_template():
    """Le texte est injecté quel que soit le type"""
    for type in PromptType:
        result = PromptBuilder.build(type, "ceci est mon texte injecté")

        assert "ceci est mon texte injecté" in result


def test_build_mock():
    """Le {input} est bien remplacé par le texte"""
    with patch("builtins.open", mock_open(read_data="Traite ceci : {input}")):
        result = PromptBuilder.build(PromptType.SUMMARY, "bonjour")

    assert result == "Traite ceci : bonjour"


def test_build_text_vide():
    with pytest.raises(ValueError):
        PromptBuilder.build(PromptType.SUMMARY, "")


def test_build_text_espace():
    with pytest.raises(ValueError):
        PromptBuilder.build(PromptType.SUMMARY, "   ")
