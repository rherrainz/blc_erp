# Implementación técnica de Auditoría

Resumen

La implementación inicial incluye:

- `core.middleware.RequestMiddleware`: expone la `request` y `user` en thread-local para que handlers fuera del contexto HTTP (signals) puedan acceder a metadatos.
- `core.models.AuditLog`: modelo append-only que almacena entradas de auditoría.
- `core.signals`: handlers que escuchan `post_save`, `pre_delete` para `clients` y `suppliers`, y señales de autenticación (`user_logged_in`, `user_logged_out`, `user_login_failed`).

Detalles importantes

- `AuditLog` utiliza `JSONField` para `changes` y almacena `ip_address`, `path` y `user_agent` para trazabilidad.
- Los signals evitan registrar cambios sobre `AuditLog` para prevenir loops.
- Para cargas de trabajo elevadas, considerar enviar logs a una cola (RabbitMQ/Kafka) y procesarlos asíncronamente para no ralentizar las requests.

Migraciones

- Se creó la migración para `core` que añade `AuditLog`. Revisa `src/core/migrations/0001_initial.py` si deseas incluirla/excluirla del VCS.

Mejoras futuras

- Integración con `django-auditlog` o `django-reversion` si se requiere historial por campo y revert.
- Envío a sistemas externos (ELK, CloudWatch) con logging estructurado (JSON).
