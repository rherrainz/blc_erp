# Arquitectura del sistema - BLC ERP

Resumen rápido

- Proyecto: Django (monorepo con apps independientes)
- Apps principales: `core`, `clients`, `suppliers`, `ui`
- Base de datos: SQLite por defecto (archivo `src/db.sqlite3`) — en producción usar PostgreSQL o MySQL
- Frontend: plantillas Django + Tailwind CSS (gestionado desde `ui/static_src`)

Componentes y responsabilidades

- `blc_erp/` : configuración global de Django (settings, urls, wsgi/asgi).
- `core/`    : vistas y utilidades globales (home, Entity base model).
- `clients/` : modelos, formularios y vistas CRUD para clientes.
- `suppliers/`: modelos, formularios y vistas CRUD para proveedores.
- `ui/`      : integración con Tailwind y plantillas compartidas (components, partials).

Flujo de una petición web

1. El router global (`blc_erp.urls`) despacha la URL al `include()` correspondiente.
2. La vista procesa datos (forms, modelos) y renderiza template o redirige.
3. Las plantillas usan componentes en `ui/templates/components/` para UI consistente.

Buenas prácticas arquitecturales

- Mantener la lógica de negocio en modelos o servicios (no en templates).
- Reutilizar `Entity` como base común para modelos que comparten campos.
- Mantener URLs y nombres consistentes por app (namespace).
