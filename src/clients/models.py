from django.db import models
from core.models import Entity

class Client(Entity):
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
