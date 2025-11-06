from django.db import models

from core.models import Entity

class Supplier(Entity):
    notes = models.TextField(verbose_name="Notas", blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
