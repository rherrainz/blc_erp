# Auditoría - FAQ

P: ¿Puedo borrar entradas de auditoría desde el admin?
R: No — el admin está configurado como solo lectura para `AuditLog`. Si por políticas internas necesitas borrar, hazlo mediante procesos controlados y registra esa acción en un sistema separado.

P: ¿Almacena la auditoría datos personales?
R: Sí, puede incluir `object_repr` que contenga datos. Revisa la política de retención y considera anonimizar datos sensibles si es necesario.

P: ¿Cómo evito que el logging añada latencia?
R: Mover la escritura de logs a una cola asíncrona (Celery/RabbitMQ) o usar un sistema de logging externo.

P: ¿Puedo añadir más modelos a auditar?
R: Sí — modifica `core.signals` para incluir otros `app_label` o crea reglas más finas por `sender`.
