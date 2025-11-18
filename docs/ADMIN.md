# Panel administrativo (Django Admin)

Acceso

- URL por defecto: `/admin/`.
- Crear usuario administrador: `python manage.py createsuperuser`.

Consejos de uso

- Registra modelos en `app/admin.py` para que aparezcan en el admin.
- Usa filtros y `list_display` para mejorar la usabilidad del panel.

Permisos

- Usuarios del admin deben tener `is_staff=True`.
- Para permisos finos, usar `Group` y `Permissions` de Django.

Seguridad

- Limitar acceso por IP o usar autenticación adicional en producción.
- No exponer `/admin/` sin HTTPS y sin autenticación correcta.
