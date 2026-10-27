# nginx — sitio `chat-bot.soluciones.uk`

Copia versionada del `server` block que vive en `/etc/nginx/sites-available/` del
VPS (Contabo, `84.247.179.120`). **Esta carpeta es la fuente de verdad**: no se
edita a mano en el servidor.

El workflow de deploy (`.github/workflows/deploy.yml`) **no toca nginx**: solo hace
pull, `uv sync`, build del frontend y reinicia `chatbot.service`.

## Qué sirve

| Fichero | Dominio | Contenido |
|---|---|---|
| `sites-available/chat-bot.soluciones.uk` | `chat-bot.soluciones.uk` | SPA del frontend (`/var/www/chatbot/frontend/dist`) + `/api/` por `unix:/run/chatbot.sock` |

Puerto 80: `/.well-known/acme-challenge/` desde `/var/www/html` y el resto `301` a
HTTPS. Puerto 443: TLS + estáticos + proxy al backend.

## Aplicar

```bash
ssh contabo
cd /var/www/chatbot
sudo bash nginx/apply.sh
```

El script copia el fichero a `/etc/nginx/sites-available/`, lo enlaza en
`sites-enabled/`, valida con `nginx -t` y solo entonces recarga. Si la validación
falla, no recarga nada. Antes deja backup en `/root/nginx-backup-<fecha>`.

## Certificado

Certbot, webroot `/var/www/html`:

- `chat-bot.soluciones.uk` (cert propio, separado del de `soluciones.uk`)

Renovación automática por el timer de certbot. Comprobar con
`sudo certbot renew --dry-run`.
