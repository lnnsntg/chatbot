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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2:1b")

# Cloud LLM config (OpenCode Zen Go, OpenAI-compatible)
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY", "")
CLOUD_MODEL = os.getenv("CLOUD_MODEL", "deepseek-v4.1-flash")
CLOUD_API_URL = os.getenv("CLOUD_API_URL", "https://opencode.ai/zen/go/v1/chat/completions")


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


def get_cloud_response(prompt: str) -> str:
    """Obtiene respuesta de API cloud (GROQ/OpenAI)"""
    if not CLOUD_API_KEY:
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
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Cloud API error: {e}")
    return None


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
    # 1. Cloud API first (faster, better quality)
    cloud_response = get_cloud_response(request.message)
    if cloud_response:
        return {
            "response": cloud_response,
            "user_message": request.message,
            "model": CLOUD_MODEL,
        }

    # 2. Fallback to local Ollama
    if check_ollama():
        ollama_response = get_ollama_response(request.message)
        if ollama_response:
            return {
                "response": ollama_response,
                "user_message": request.message,
                "model": MODEL,
            }

    # 3. Offline
    return {
        "response": "AI service is not available. Please try again later.",
        "user_message": request.message,
        "model": "offline",
    }


# Endpoint de streaming (demo)
@app.get("/api/info")
def info():
    return {
        "name": "AI Chatbot Portfolio",
        "tech_stack": ["FastAPI", "React", "Ollama + Cloud LLM"],
        "features": ["Chat interactivo", "Historial", "LLM cloud + local", "Despliegue"],
        "model": CLOUD_MODEL if CLOUD_API_KEY else MODEL,
        "ollama_available": check_ollama(),
    }
