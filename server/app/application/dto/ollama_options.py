from dataclasses import dataclass


@dataclass
class OllamaOptions:
    """
    temperature : Contrôle la créativité du modèle
    top_p : Contrôle la diversité globale des mots possibles
    num_predict : Nombre maximal de tokens générés
    repeat_penalty : Pénalise les répétitions

    top_k : Limite le nombre
    presence_penalty : Pas la nouveauté
    frequency_penalty : Pas de pénalisation artificielle
    """

    temperature: float | None = None
    top_p: float | None = None
    num_predict: int | None = None
    repeat_penalty: float | None = None

    top_k: int = None
    presence_penalty: float = None
    frequency_penalty: float = None


    def to_dict(self):
        return { key: value for key, value in self.__dict__.items() if value }
