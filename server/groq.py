from openai import OpenAI
import time

print("Lancement")
start = time.time()

client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Explain the importance of fast language models",
    model="openai/gpt-oss-20b",
)

end = time.time()

print(response.output_text)
print(f"Temps d'exécution : {end - start:.3f} secondes")
