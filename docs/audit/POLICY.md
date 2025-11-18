# Política de Auditoría

Objetivo

- Definir qué eventos deben registrarse, por cuánto tiempo, quiénes pueden acceder a los registros y cómo se protege la integridad de los mismos.

Alcance

- Eventos auditados inicialmente:
  - CRUD sobre entidades críticas: `clients`, `suppliers`.
  - Autenticación: `login`, `logout`, `login_failed`.
  - Cambios de permisos y usuarios (por implementar más adelante).

Datos registrados

- Timestamp (fecha y hora UTC)
- Actor: usuario (si está autenticado)
- Acción: `create`, `update`, `delete`, `login`, `logout`, `login_failed`, etc.
- Referencia al objeto: `content_type`, `object_pk`, `object_repr`
- Cambios: campo->valor antes/después (cuando aplique)
- Metadatos de la request: `ip_address`, `path`, `user_agent`

Retención

- Recomendación inicial: mantener 12 meses en la base de datos primaria; luego archivar en almacenamiento externo (S3, Glacier) para cumplimiento y auditoría forense.

Acceso y permisos

- Solo superusuarios y personal autorizado pueden consultar o exportar logs.
- Las entradas de auditoría son append-only en la lógica de la aplicación (no visibles opciones de borrado desde la UI).

Protección de integridad

- Opcional: implementar hashing encadenado de las entradas (`entry_hash`) y almacenamiento periódico fuera de la BD.

Cumplimiento legal

- Si se almacenan datos personales, establecer procedimientos para cumplir GDPR/leyes locales (retención mínima, derecho al olvido — excluir datos personales de auditoría o anonimizar cuando aplique).
