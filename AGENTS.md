Te encargas de hacer los commit y merge y push de las ramas.

Siempre usas convention commit.

El idioma para los commits es ingles.

Tienes que asegurarte que siempre estas en la rama dev para hacer los commit.


Si hay "algo" en la rama main entonces usas stash y luego pop en la rama dev, luego haces el commit, siempre en dev.

Luego haces merge --ff-only en main. 

Por ultimo subes ambas ramas al repositorio con git push origin --all o como quieras.

Cualquier cosa "rara" tienes que avisarme, no hagas nada sin preguntarme.

Guarda cualquier cambio antes de hacer commit si es necesario.

Por ultimo vuelves a la rama dev.

Jamas hacemos git reset, recuerda que es un mono repo y hacer esos cambios implica romper la aplicacion en otra parte.

antes de hacer commit debes avisar para yo poder ver los cabios ne vscode.

No haces instalaciones sin preguntarme, siempre pregunta, si necesitas algun programa en la mayoria de los casos hare yo la instalacion.

Lo mismo para los servidores vps, nunca haces instalacione tu directamente, si son necesarias me dices, en la mayoria de los casos las hare yo.

Nunca haces cambios manuales en los servers, siempre pasan por git. (primero local, luego al servidor mediante pull).

Usamos gitactions con workflow, tienes el comando < gh > para ver si los desplieges se estan haciendo correctamente, recuerda no hacer cambios manuales en el
servidor a menos que sea estrictamente necesario y siempre comunicandomelo a mi.

## Nginx (VPS Contabo)

Los `server` blocks estan versionados en `nginx/sites-available/`. Ese directorio es la fuente de verdad: no se editan a mano en el VPS.

- Cambio en nginx: se edita `nginx/sites-available/`, commit en dev, merge --ff-only a main, push.
- En el servidor se aplican con `sudo bash /var/www/chatbot/nginx/apply.sh`: hace backup en `/root/nginx-backup-<fecha>`, instala, valida con `nginx -t` y solo entonces recarga. Si la validacion falla, no recarga.
- El workflow de deploy no toca nginx: solo pull, deps, build del frontend y restart de `chatbot.service`.
- Certificados con certbot, webroot `/var/www/html`, renovacion automatica por timer. El cert `chat-bot.soluciones.uk` es propio, separado del de `soluciones.uk` (que vive en el repo portfolio).

Si el `git pull` del deploy falla porque el VPS tiene cambios locales (por ejemplo un `chmod` hecho a mano), se descarta ese cambio con `git checkout -- <archivo>` y se relanza el run. En el servidor nunca se hace stash, merge ni reset.

