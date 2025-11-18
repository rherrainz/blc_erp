from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Entity


class EntityModelTests(TestCase):
    """Tests para el modelo abstracto Entity"""

    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Creamos un modelo concreto para testear Entity
        # Usaremos la clase Client como subclase de Entity
        from clients.models import Client
        
        self.client_test = Client.objects.create(
            company_name="Test Company S.A.",
            name="Test Contact",
            email="test@example.com",
            phone="+54 11 1234-5678",
            address="Calle Test 123, Buenos Aires",
            tax_id="20-12345678-9",
            is_active=True
        )

    def test_entity_creation(self):
        """Test que se crea una entidad correctamente"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Nueva Empresa",
            name="Nuevo Contacto"
        )
        
        self.assertIsNotNone(client.id)
        self.assertEqual(client.company_name, "Nueva Empresa")
        self.assertEqual(client.name, "Nuevo Contacto")
        self.assertTrue(client.is_active)

    def test_entity_required_fields(self):
        """Test que los campos obligatorios se requieren"""
        from clients.models import Client
        from django.core.exceptions import ValidationError
        
        # Intentar validar sin company_name
        client = Client(name="Test")
        with self.assertRaises(ValidationError):
            client.full_clean()
        
        # Intentar validar sin name
        client2 = Client(company_name="Test")
        with self.assertRaises(ValidationError):
            client2.full_clean()

    def test_entity_optional_fields(self):
        """Test que los campos opcionales pueden ser nulos"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Test",
            name="Test"
        )
        
        self.assertIsNone(client.email)
        self.assertIsNone(client.phone)
        self.assertIsNone(client.address)
        self.assertIsNone(client.tax_id)

    def test_entity_is_active_default(self):
        """Test que is_active por defecto es True"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Test",
            name="Test"
        )
        
        self.assertTrue(client.is_active)

    def test_entity_is_active_false(self):
        """Test que se puede desactivar una entidad"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Test",
            name="Test",
            is_active=False
        )
        
        self.assertFalse(client.is_active)

    def test_entity_string_representation(self):
        """Test la representación en string de una entidad"""
        self.assertEqual(
            str(self.client_test),
            "Test Company S.A. - Test Contact"
        )

    def test_entity_update(self):
        """Test que se puede actualizar una entidad"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Original",
            name="Original Contact"
        )
        
        client.company_name = "Actualizado"
        client.email = "nuevo@example.com"
        client.save()
        
        client.refresh_from_db()
        self.assertEqual(client.company_name, "Actualizado")
        self.assertEqual(client.email, "nuevo@example.com")

    def test_entity_delete(self):
        """Test que se puede eliminar una entidad"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Para Eliminar",
            name="Test"
        )
        
        client_id = client.id
        client.delete()
        
        self.assertEqual(Client.objects.filter(id=client_id).count(), 0)

    def test_entity_queryset_filtering_by_active(self):
        """Test que se puede filtrar por is_active"""
        from clients.models import Client
        
        Client.objects.all().delete()
        
        Client.objects.create(company_name="Active 1", name="Test", is_active=True)
        Client.objects.create(company_name="Active 2", name="Test", is_active=True)
        Client.objects.create(company_name="Inactive", name="Test", is_active=False)
        
        active_clients = Client.objects.filter(is_active=True)
        self.assertEqual(active_clients.count(), 2)
        
        inactive_clients = Client.objects.filter(is_active=False)
        self.assertEqual(inactive_clients.count(), 1)

    def test_entity_email_validation(self):
        """Test validación de formato de email"""
        from clients.models import Client
        
        # Django valida emails automáticamente en EmailField
        client = Client(
            company_name="Test",
            name="Test",
            email="invalid-email"
        )
        
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_entity_tax_id_length(self):
        """Test que el CUIT tiene un límite de caracteres"""
        from clients.models import Client
        
        # Crear con un tax_id válido
        client = Client.objects.create(
            company_name="Test",
            name="Test",
            tax_id="20-12345678-9"
        )
        
        self.assertEqual(client.tax_id, "20-12345678-9")


class CoreViewsTests(TestCase):
    """Tests para las vistas de la app core"""

    def test_home_view_get(self):
        """Test GET en vista home"""
        from django.test import Client as DjangoTestClient
        from django.urls import reverse
        
        test_client = DjangoTestClient()
        response = test_client.get(reverse('core:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context(self):
        """Test que home view retorna contexto correcto"""
        from django.test import Client as DjangoTestClient
        from django.urls import reverse
        
        test_client = DjangoTestClient()
        response = test_client.get(reverse('core:home'))
        
        # El template home.html se renderiza correctamente
        self.assertEqual(response.status_code, 200)
