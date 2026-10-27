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

## Servicio y permisos

- `RuntimeDirectory=chatbot` con `RuntimeDirectoryMode=0750`: systemd crea `/run/chatbot` como `root:www-data` `0750` en cada arranque y lo borra al parar el servicio.
- Gunicorn hace su `--bind unix:/run/chatbot/chatbot.sock` normal (sin `umask` ni `fd://`): el control de acceso lo hace el directorio, no el fichero.
- nginx corre como `www-data` y entra por grupo. Ningún otro usuario local puede ni atravesar `/run/chatbot`.
- `chatbot.service`: `User=root`, `Group=www-data`, `--workers 2`.
- `.env` en el servidor: `600 root:root`, no está en git (`.gitignore`).
- nginx solo sirve `frontend/dist`: el backend, `.env` y el `.git` no son accesibles por HTTP (probado: `/.env`, `/backend/.env`, `/.git/config` devuelven el `index.html` del SPA).

## Deploy

- GitHub Actions `.github/workflows/deploy.yml` en push a `main` (o `workflow_dispatch`), en un solo paso SSH:
  - pull en `/var/www/chatbot` — siempre.
  - la comparación de cambios es contra el último SHA desplegado (`.deployed-sha` en el servidor), no contra `HEAD~1`: así un push con varios commits no se salta nada. Si no hay marcador, aplica todo.
  - instala la unit + `daemon-reload` — solo si cambió `backend/chatbot.service`.
  - `uv sync --frozen` — solo si cambió `pyproject.toml` o `uv.lock`.
  - `npm ci && npm run build` — solo si cambió `frontend/`.
  - `systemctl restart chatbot.service` + health check por socket — solo si cambió `backend/*.py`, las deps o la unit.
  - `nginx/apply.sh` — solo si cambió `nginx/`, y **después** del restart (el socket nuevo tiene que existir antes de que nginx apunte a él).
