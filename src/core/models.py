from django.db import models

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