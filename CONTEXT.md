# Contexto del proyecto Chatbot

## Servidor
- Host: 84.247.179.120
- Puerto SSH: 5773
- Usuario: root

## Proyecto
- Ubicación local: /home/lenin/chatbot
- Ubicación en el servidor: /var/www/chatbot
- Backend: FastAPI, gunicorn + UvicornWorker en `unix:/run/chatbot.sock`
- Frontend: React/Vite, build en `/var/www/chatbot/frontend/dist`
- Dominio: chat-bot.soluciones.uk

## Archivos de configuración
- Nginx: `nginx/sites-available/chat-bot.soluciones.uk` (versionado en este repo, se aplica con `sudo bash nginx/apply.sh`)
- Service: `backend/chatbot.service` → `/etc/systemd/system/chatbot.service` (unit `chatbot.service`)
- Frontend dist: `/var/www/chatbot/frontend/dist`

## Ramas
- Se trabaja en `dev`: commit en dev, `merge --ff-only` a main, push de ambas.

## Deploy
- GitHub Actions `.github/workflows/deploy.yml` en push a `main`: pull en `/var/www/chatbot`, `uv sync --frozen` si cambia backend, `npm ci && npm run build` si cambia frontend, y `systemctl restart chatbot.service`.
- El workflow no toca nginx: los cambios de nginx se aplican con `nginx/apply.sh`.
