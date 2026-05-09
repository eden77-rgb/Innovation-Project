""" TEST PROMPTBUILDER
from domain import PromptBuilder, PromptType

print(
    "###########################\n" \
    "#    PROMPT 1 : Résumé    #\n" \
    "###########################\n"
)

prompt = PromptBuilder.build(
    PromptType.SUMMARY,
    "L'intelligence artificielle transforme de nombreux secteurs comme la santé, l'éducation et l'industrie. Elle permet d'automatiser des tâches complexes et d'améliorer la prise de décision grâce à l'analyse de grandes quantités de données."
)
print(prompt, "\n\n")


print(
    "###########################\n" \
    "#  PROMPT 2 : Traduction  #\n" \
    "###########################\n"
)

prompt = PromptBuilder.build(
    PromptType.TRANSLATE,
    "Le changement climatique est un défi majeur pour l'humanité."
)
print(prompt, "\n\n")


print(
    "###########################\n" \
    "#   PROMPT 3 : Réécrire   #\n" \
    "###########################\n"
)

prompt = PromptBuilder.build(
    PromptType.REWRITE,
    "Je pense que ce produit est bien mais il est un peu cher et pas très pratique."
)
print(prompt, "\n\n")
"""





from infrastructure import OllamaClient

print("Call 1")

ollama = OllamaClient('llama3.2:1b', "localhost", 0.9, 10)
print(ollama.generate("Why is the sky blue ?"))
