from django.db import models
from core.models import Entity

class Supplier(Entity):
    company_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
