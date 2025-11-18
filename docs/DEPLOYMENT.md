# Despliegue (guía rápida)

Consideraciones generales

- Seguridad: `DEBUG=False`, `SECRET_KEY` en variables de entorno, configurar `ALLOWED_HOSTS`.
- Base de datos: migrar a PostgreSQL para producción.
- Servidor WSGI: `gunicorn` o `uvicorn` (si usas ASGI).

Pasos mínimos (Linux - ejemplo)

1. Crear entorno y clonar repo

2. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configurar variables de entorno

```bash
export DJANGO_SETTINGS_MODULE=blc_erp.settings
export SECRET_KEY='tu_secret'
export ALLOWED_HOSTS='tu.dominio.com'
```

4. Migraciones

```bash
python manage.py migrate
```

5. Recolectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

6. Ejecutar con gunicorn (ejemplo)

```bash
gunicorn blc_erp.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

7. Configurar proxy reverso (nginx)

- Proxy hacia `localhost:8000` y servir `static` y `media` desde `nginx`.

Ejemplo mínimo `nginx`:

```
server {
    listen 80;
    server_name tu.dominio.com;

    location /static/ {
        alias /ruta/a/tu/proyecto/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Monitoreo y backups

- Configura rotación de logs y backups periódicos de la base de datos.
- Considera usar `systemd` para administrar el servicio `gunicorn`.
