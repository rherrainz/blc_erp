from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType



class Entity(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Razón Social")  # Obligatorio
    name = models.CharField(max_length=255, verbose_name="Nombre")  # Obligatorio
    email = models.EmailField(verbose_name="Email", blank=True, null=True)  # Opcional
    phone = models.CharField(max_length=50, verbose_name="Teléfono", blank=True, null=True)  # Opcional
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)  # Opcional
    tax_id = models.CharField(max_length=50, verbose_name="CUIT/CUIL", blank=True, null=True)  # Opcional
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # Siempre definido (True o False)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """Registro de auditoría append-only para eventos importantes.

    Campos básicos:
    - timestamp: cuándo ocurrió
    - actor: usuario que realizó la acción (si está disponible)
    - action: tipo ('create','update','delete','login','logout','login_failed',...)
    - content_type/object_pk/object_repr: referencia al objeto afectado
    - changes: JSON con cambios (opcional)
    - ip_address/path/user_agent: metadatos de la request
    """

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=32)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_pk = models.CharField(max_length=255, null=True, blank=True)
    object_repr = models.CharField(max_length=255, null=True, blank=True)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=512, null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    entry_hash = models.CharField(max_length=128, null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"[{self.timestamp.isoformat()}] {self.action} {self.content_type} {self.object_pk}"