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





""" TEST OLLAMACLIENT
from infrastructure import OllamaClient

ollama = OllamaClient('llama3.2:1b', "localhost", 0.9, 10)


print("generate()")
print(ollama.generate("Why is the sky blue ?"))


print("stream()")
for token in ollama.stream("Why is the sky blue ?"):
    print(token, end="", flush=True)
"""





""" TEST LLMSERVICE
from application import LLMService, LLMPolicy
from domain import PromptBuilder, PromptType
from infrastructure import OllamaClient

service = LLMService(PromptBuilder, OllamaClient('qwen2.5:3b', "localhost", 0.9, 10), LLMPolicy()) # llama3.2:1b | gemma3:latest

prompt = '''
Le développement des villes au cours des deux derniers siècles a profondément transformé les modes de vie humains. Avec la révolution industrielle, les populations rurales ont progressivement migré vers les centres urbains à la recherche de travail dans les usines. Cette urbanisation rapide a entraîné une croissance importante des villes, mais aussi de nombreux défis. Les infrastructures ont dû s’adapter pour répondre à une population toujours plus nombreuse, ce qui a conduit à la construction de logements en grande quantité, parfois sans réelle planification.

Au fil du temps, les villes sont devenues des centres économiques, culturels et politiques majeurs. Elles concentrent aujourd’hui la majorité des activités économiques et attirent des populations très diverses. Cependant, cette concentration a aussi des conséquences négatives, comme la pollution de l’air, les embouteillages, le manque de logements abordables et les inégalités sociales. Certaines zones urbaines connaissent une forte densité de population, tandis que d’autres sont moins développées.

Face à ces défis, les urbanistes et les gouvernements cherchent des solutions pour rendre les villes plus durables. Cela inclut le développement des transports en commun, la création d’espaces verts, l’amélioration de l’efficacité énergétique des bâtiments et la promotion de villes dites “intelligentes” utilisant les nouvelles technologies pour mieux gérer les ressources.

Aujourd’hui, l’urbanisation continue à l’échelle mondiale, notamment dans les pays en développement. On estime qu’une grande partie de la croissance démographique future se concentrera dans les villes. Cela rend essentiel de réfléchir à des modèles urbains capables de concilier croissance économique, qualité de vie et respect de l’environnement.
'''

print("[DEBUG]: generate()")
print(service.generate(PromptType.TRANSLATE, prompt))


print("[DEBUG]: stream()")
for token in service.stream(PromptType.TRANSLATE, prompt):
    print(token, end="", flush=True)
"""





from fastapi import FastAPI
from interfaces import router
from interfaces import register_exception_handler

app = FastAPI()

register_exception_handler(app=app)

app.include_router(router, prefix="/api")
