# Chatbot

 Chatbot con frontend React y backend FastAPI. Desplegado en **chat-bot-ports.duckdns.org**.

## Estructura

```
chatbot/
├── backend/          # API con FastAPI
│   └── main.py
└── frontend/         # Interfaz con React + Vite
    └── src/
```

## Requisitos

- Python 3.12+
- Node.js 18+

## Instalación y ejecución

### Backend

```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

El backend estará en `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend estará en `http://localhost:5173`

## Rama principal

- `dev`: rama de desarrollo
- `main`: rama estable (fusionar desde dev)

## Commits

Este proyecto usa [Conventional Commits](https://www.conventionalcommits.org/).