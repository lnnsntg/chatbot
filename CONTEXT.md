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

- Unit `chatbot.service`: `User=root`, `Group=www-data`, `UMask=0007`.
- Socket `/run/chatbot.sock`: `root:www-data` con modo `770`. El umask hay que pasárselo a gunicorn (`--umask 0007`): gunicorn hace su propio `os.umask(conf.umask)` al crear el socket y **sobreescribe** el `UMask` de systemd (default `0` = `777`).
- nginx corre como `www-data`, así que entra en el socket por grupo. Ningún otro usuario local puede llamar a la API saltándose nginx.
- `.env` en el servidor: `600 root:root`, no está en git (`.gitignore`).
- nginx solo sirve `frontend/dist`: el backend, `.env` y el `.git` no son accesibles por HTTP (probado: `/.env`, `/backend/.env`, `/.git/config` devuelven el `index.html` del SPA).

## Deploy

- GitHub Actions `.github/workflows/deploy.yml` en push a `main`:
  - pull en `/var/www/chatbot` — siempre.
  - instala la unit en `/etc/systemd/system/` + `daemon-reload` — solo si cambió `backend/chatbot.service`.
  - `uv sync --frozen` — solo si cambió `pyproject.toml` o `uv.lock`.
  - `npm ci && npm run build` — solo si cambió `frontend/`.
  - `systemctl restart chatbot.service` + health check por socket — solo si cambió `backend/*.py`, las deps o la unit. Un push de docs o solo frontend no reinicia el backend.
- El workflow no toca nginx: los cambios de nginx se aplican con `nginx/apply.sh`.
