from ollama import chat, ChatResponse
import time

print("Lancement")
start = time.time()

response: ChatResponse = chat(
    model='llama3.2:1b', 
    messages=[
        {'role': 'user', 'content': 'Why is the sky blue?'},
    ],
    stream=True
)

for chunk in response:
    print(chunk['message']['content'], end="", flush=True)

print(f"\n\nTemps : {time.time() - start:.3f}s\n")
