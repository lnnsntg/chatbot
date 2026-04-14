"""
AI Chatbot Backend - FastAPI + Ollama
Portfolio Project for Upwork
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Chatbot API")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2:1b")


# Modelo del mensaje
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


def check_ollama():
    """Verifica si Ollama está disponible"""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except:
        return False


def get_ollama_response(prompt: str) -> str:
    """Obtiene respuesta de Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json().get("message", {}).get("content", "")
    except Exception as e:
        print(f"Ollama error: {e}")
    return None


# Ruta de health
@app.get("/")
def root():
    ollama_available = check_ollama()
    return {
        "status": "ok",
        "message": "AI Chatbot API running",
        "ollama": ollama_available,
    }


@app.get("/health")
def health():
    return {"status": "healthy", "ollama": check_ollama()}


# Endpoint de chat
@app.post("/chat")
def chat(request: ChatRequest):
    # Intentar usar Ollama si está disponible
    if check_ollama():
        ollama_response = get_ollama_response(request.message)
        if ollama_response:
            return {
                "response": ollama_response,
                "user_message": request.message,
                "model": MODEL,
            }

    # Fallback: solo un mensaje si Ollama no está disponible
    return {
        "response": "Ollama is not available. Please start Ollama locally.",
        "user_message": request.message,
        "model": "offline",
    }


# Endpoint de streaming (demo)
@app.get("/api/info")
def info():
    return {
        "name": "AI Chatbot Portfolio",
        "tech_stack": ["FastAPI", "React", "Ollama"],
        "features": ["Chat interactivo", "Historial", "LLM local", "Despliegue"],
        "model": MODEL,
        "ollama_available": check_ollama(),
    }
