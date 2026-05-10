from ollama import ChatResponse, Client
from collections.abc import Generator


class OllamaClient:
    def __init__(self, model: str, host: str, temperature: float, timeout: int):
        self.model = model
        self.temperature = temperature
        # self.timeout = timeout

        self.client  = Client(host=host)


    def generate(self, prompt: str, options: dict | None = None) -> str:
        response : ChatResponse = self.client.chat(
            model = self.model,
            options = { "temperature": self.temperature, **(options or {}) },
            messages = [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        return response['message']['content']


    def stream(self, prompt: str, options: dict | None = None) -> Generator[str]:
        stream : ChatResponse  = self.client.chat(
            model = self.model,
            options = { "temperature": self.temperature, **(options or {}) },
            messages = [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            stream = True
        )

        for chunk in stream:
            yield chunk['message']['content']
