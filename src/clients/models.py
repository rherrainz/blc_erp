from django.db import models
from core.models import Entity

class Client(Entity):
    notes = models.TextField(verbose_name="Notas", blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.company_name} - {self.name}"
