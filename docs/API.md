# API y rutas principales

Este proyecto es una aplicación Django tradicional basada en vistas y templates. Aun así, aquí se listan las rutas y recursos principales expuestos por la aplicación.

Rutas relevantes (ejemplos)

- `/` : Home (app `core`)
- `/clients/` : Listado de clientes (app `clients`)
- `/clients/add/` : Crear cliente
- `/clients/<pk>/` : Detalle cliente
- `/clients/<pk>/edit/` : Editar cliente
- `/suppliers/` : Listado de proveedores (app `suppliers`)
- `/suppliers/add/` : Crear proveedor
- `/suppliers/<pk>/` : Detalle proveedor
- `/admin/` : Panel administrativo de Django

Notas

- Si se añaden endpoints REST (DRF u otros), documentar aquí los recursos, métodos HTTP y ejemplos de request/response.
- Para APIs públicas, añadir autenticación (token, OAuth2) y versionado (`/api/v1/`).
