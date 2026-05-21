from ollama import ChatResponse, Client
from domain.exceptions import OllamaNotAvailableError, OllamaTimeoutError, OllamaGenerationError
from collections.abc import Generator


class OllamaClient:
    def __init__(self, model: str, host: str, temperature: float, timeout: int):
        self.model = model
        self.temperature = temperature
        # self.timeout = timeout

        self.client  = Client(host=host)


    def generate(self, prompt: str, options: dict | None = None) -> str:
        try:
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

        except ConnectionError:
            raise OllamaNotAvailableError("Ollama server is not running")
        
        except TimeoutError:
            raise OllamaTimeoutError("Ollama request timed out")
        
        except Exception as e:
            raise OllamaGenerationError(str(e))


    def stream(self, prompt: str, options: dict | None = None) -> Generator[str]:
        try:
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

        except ConnectionError:
            raise OllamaNotAvailableError("Ollama server is not running")
        
        except TimeoutError:
            raise OllamaTimeoutError("Ollama request timed out")
        
        except Exception as e:
            raise OllamaGenerationError(str(e))
