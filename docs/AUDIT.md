# Auditoría del sistema

Este documento describe la implementación inicial de auditoría en BLC ERP.

Objetivo

- Registrar eventos críticos: creación/actualización/eliminación de entidades, autenticaciones (login/logout/failed) y cambios de permisos.

Implementación mínima

- `core.middleware.RequestMiddleware`: expone la request y el usuario en thread-local.
- `core.models.AuditLog`: modelo append-only para almacenar entradas de auditoría.
- Próximos pasos: señales para `clients` y `suppliers`, tests y UI de consulta.

Cómo consultar

- Desde Django Admin (si se registra), o mediante queries a `core.models.AuditLog`.

Política recomendada

- Retención: 1 año en BD caliente, luego archivar en S3/Glacier.
- Seguridad: exportar copias periódicas a almacenamiento externo con acceso restringido.
- Integridad: opcionalmente calcular hashing encadenado para detectar manipulaciones.

***

Si quieres, implemento ahora los signal handlers y los tests básicos.
