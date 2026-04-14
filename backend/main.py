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

app = FastAPI(title="AI Chatbot API")

# CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Ollama
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"  # Modelo ligero para VPS

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
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "")
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
        "ollama": ollama_available
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
                "model": MODEL
            }
    
    # Fallback: respuestas basadas en palabras clave
    user_message = request.message.lower()
    
    if "hola" in user_message or "hello" in user_message or "hi" in user_message:
        response = "Hi! I am a demo chatbot with Ollama. How can I help you?"
    elif "python" in user_message or "django" in user_message:
        response = "Python is a very versatile language. Django is excellent for full web apps, and FastAPI is perfect for fast APIs."
    elif "javascript" in user_message or "react" in user_message:
        response = "JavaScript and React are ideal for frontend. Next.js adds Server-Side Rendering for better SEO."
    elif "ai" in user_message or "llm" in user_message:
        response = "This chatbot uses Ollama (local LLM). It is private and fast. Perfect for demos and limited VPS."
    elif "proyecto" in user_message or "project" in user_message or "portfolio" in user_message:
        response = "This project demonstrates my skills with FastAPI, React and production deployment."
    elif "quien" in user_message or "name" in user_message:
        response = "I am a demo chatbot for your Upwork portfolio. Contact me for projects!"
    elif "precio" in user_message or "cost" in user_message or "rate" in user_message:
        response = "For custom projects, I can offer you a budget tailored to your needs."
    else:
        response = f"Got it: '{request.message}'. If Ollama were connected, I would respond with real AI. For now I am a smart placeholder 😊"
    
    return {
        "response": response,
        "user_message": request.message,
        "model": "fallback"
    }

# Endpoint de streaming (demo)
@app.get("/api/info")
def info():
    return {
        "name": "AI Chatbot Portfolio",
        "tech_stack": ["FastAPI", "React", "Ollama"],
        "features": ["Chat interactivo", "Historial", "LLM local", "Despliegue"],
        "model": MODEL,
        "ollama_available": check_ollama()
    }

