from fastapi import FastAPI

app = FastAPI()


# GET
@app.get("/health", summary="Confirms the API server is alive and running.")
def read_health():
    return { "status": 200, "ok": True }

@app.get("/status", summary="Confirms the API and the local AI are reachable and operational.")
def read_status():
    return { 
        "status": 200,
        "ok": True,
        "api_version": 0,
        "ai_available": False
    }


# POST
@app.post("/generate", summary="Generates text from a prompt")
def generate(body):
    """
    body: 
    {
        model: "",
        prompt: "",
        context?: ""
    }
    """
    
    return {
        "status": 200,
        "ok": True,
        "response": "",
        "duration_ms": 0,
        "tokens_used": 0,
        "error": None
    }
