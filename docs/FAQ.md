# Preguntas frecuentes (FAQ)

Q: ¿Por qué falla `python manage.py migrate`?

A: Asegúrate de haber activado el entorno virtual e instalado dependencias. Si hay cambios de modelos no migrados, ejecuta `makemigrations` primero.

Q: ¿Por qué no se ven los estilos (Tailwind)?

A: Verifica que `npm install` y `npm run dev` hayan corrido en `ui/static_src`. Para producción, ejecuta el build de producción y `collectstatic`.

Q: ¿Cómo ejecuto los tests con pytest?

A: Desde la carpeta `src` ejecuta `pytest -q`. También puedes usar `python manage.py test` si prefieres el runner de Django.

Q: ¿Dónde está la base de datos?

A: Por defecto está en `src/db.sqlite3`. En producción, la configuración puede apuntar a otra BD gestionada por `DATABASES` en `settings.py`.

Q: ¿Cómo agrego nuevas apps?

A: Crear app con `python manage.py startapp <name>`, registrar en `INSTALLED_APPS` y añadir `urls.py` si aplica.
