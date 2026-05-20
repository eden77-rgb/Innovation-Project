from dataclasses import dataclass


@dataclass
class OllamaOptions:
    """
    temperature : Contrôle la créativité du modèle

    top_p : Contrôle la diversité globale des mots possibles

    num_predict : Nombre maximal de tokens générés

    repeat_penalty : Pénalise les répétitions
    """

    temperature: float | None = None
    top_p: float | None = None
    num_predict: int | None = None
    repeat_penalty: float | None = None


    def to_dict(self):
        return { key: value for key, value in self.__dict__.items() if value }
