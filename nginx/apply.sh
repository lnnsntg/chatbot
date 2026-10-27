#!/bin/bash
# Aplica el server block de nginx de este repo a /etc/nginx y recarga nginx.
# Uso: sudo bash nginx/apply.sh
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/sites-available" && pwd)"
DEST_DIR="/etc/nginx/sites-available"
SITES="chat-bot.soluciones.uk"

if [ "$(id -u)" -ne 0 ]; then
    echo "→ Se necesita root: sudo bash $0" >&2
    exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="/root/nginx-backup-$STAMP"
mkdir -p "$BACKUP"
for site in $SITES; do
    [ -f "$DEST_DIR/$site" ] && cp -a "$DEST_DIR/$site" "$BACKUP/"
done
echo "→ Backup en $BACKUP"

for site in $SITES; do
    echo "→ $site"
    install -m 644 -o root -g root "$SRC_DIR/$site" "$DEST_DIR/$site"
    ln -sfn "$DEST_DIR/$site" "/etc/nginx/sites-enabled/$site"
done

echo "→ nginx -t"
if ! nginx -t; then
    echo "✗ Configuración inválida. No se recarga. Restaurar desde $BACKUP" >&2
    exit 1
fi

systemctl reload nginx
echo "✓ nginx recargado $(date)"
