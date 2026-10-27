"""
AI Chatbot Backend - FastAPI + OpenCode Zen Go
Portfolio Project for Upwork
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloud LLM config (OpenCode Zen Go, OpenAI-compatible)
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY", "")
CLOUD_MODEL = os.getenv("CLOUD_MODEL", "deepseek-v4.1-flash")
CLOUD_API_URL = os.getenv("CLOUD_API_URL", "https://opencode.ai/zen/go/v1/chat/completions")
# OpenCode Zen Go exige esta cabecera: sin ella responde 400 MissingSessionID
CLOUD_SESSION = os.getenv("CLOUD_SESSION", "chatbot")


# Modelo del mensaje
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


def get_cloud_response(prompt: str) -> Optional[str]:
    """Obtiene respuesta de la API cloud (OpenCode Zen Go)"""
    if not CLOUD_API_KEY:
        print("Cloud API error: CLOUD_API_KEY vacia")
        return None
    try:
        response = requests.post(
            CLOUD_API_URL,
            json={
                "model": CLOUD_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
            },
            headers={
                "Authorization": f"Bearer {CLOUD_API_KEY}",
                "Content-Type": "application/json",
                "x-opencode-session": CLOUD_SESSION,
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        print(f"Cloud API error: {response.status_code} {response.text[:300]}")
    except Exception as e:
        print(f"Cloud API error: {e}")
    return None


# Ruta de health
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AI Chatbot API running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# Endpoint de chat
@app.post("/chat")
def chat(request: ChatRequest):
    cloud_response = get_cloud_response(request.message)
    if cloud_response:
        return {
            "response": cloud_response,
            "user_message": request.message,
            "model": CLOUD_MODEL,
        }

    raise HTTPException(status_code=503, detail="AI service is not available")


@app.get("/api/info")
def info():
    return {
        "name": "AI Chatbot Portfolio",
        "tech_stack": ["FastAPI", "React", "OpenCode Zen Go"],
        "features": ["Chat interactivo", "Historial", "LLM cloud", "Despliegue"],
        "model": CLOUD_MODEL,
    }
