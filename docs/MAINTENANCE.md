# Mantenimiento y operaciones

Copias de seguridad

- Para SQLite: copiar `src/db.sqlite3` periódicamente (no recomendado en producción).
- Para PostgreSQL/MySQL: usar `pg_dump` / `mysqldump` y almacenar en un lugar seguro.

Actualizaciones y migraciones

- Antes de actualizar el código: crear backup de la base de datos.
- Ejecutar `python manage.py makemigrations` y `python manage.py migrate` tras actualizar modelos.

Logs

- Django escribe logs si está configurado en `settings.LOGGING`.
- Revisa `/var/log/` o la ruta de logs definida por el servicio en producción.

Rotación de logs

- Usar `logrotate` en Linux o configuración de `systemd`/journald para evitar crecimiento indefinido.

Salud del sistema

- Revisar uso de disco y backups automáticos.
- Verificar tareas programadas (si hay cronjobs o celery tasks en futuras integraciones).

Recuperación ante desastre

1. Restaurar backup de BD
2. Restaurar archivos estáticos/media
3. Ejecutar `migrate` y revisar integridad
