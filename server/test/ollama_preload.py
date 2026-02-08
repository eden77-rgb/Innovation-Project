from ollama import chat
import time

TIME_SLEEP = [0, 120, 600]
# ===== PRÉCHARGEMENT EFFICACE =====
print("Chargement du modèle en mémoire...")
start_preload = time.time()

chat(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': 'Hi'}],
    options={'num_ctx': 2048, 'num_predict': 10}  # Génère quelques tokens
)

print(f"Modèle prêt ! ({time.time() - start_preload:.3f}s)\n")

# ===== TES VRAIES REQUÊTES =====
for i in range(3):
    print(f"Attente de : {TIME_SLEEP[i]} secondes")
    time.sleep(TIME_SLEEP[i])

    print(f"Requête {i+1}")
    start = time.time()
    
    response = chat(
        model='llama3.2:1b',
        messages=[{'role': 'user', 'content': f'Why is the sky blue?'}],
        options={'num_ctx': 2048, 'num_predict': 256}
    )
    
    print(response['message']['content'][:50] + "...")
    print(f"Temps : {time.time() - start:.3f}s\n")

"""
Objectif : 
Précharger le modele pour réduire le temps avant une requete
"""