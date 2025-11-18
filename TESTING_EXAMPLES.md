"""
Ejemplos de cómo escribir más tests para BLC ERP

Este archivo muestra patrones y ejemplos para extender el testing.
"""

# ============================================================================
# EJEMPLO 1: Test de templatetags
# ============================================================================

"""
# En: src/core/tests.py

from django.test import TestCase
from django.template import Context, Template
from django.template.defaultfilters import mark_safe

class FormFiltersTemplateTagTests(TestCase):
    '''Tests para los filtros de formularios en templatetags'''
    
    def test_form_class_filter_applied(self):
        '''Test que el filtro de clases CSS se aplica correctamente'''
        template = Template("{% load form_filters %}{{ field|add_form_class }}")
        # Renderizar y validar que las clases se agregaron
        
    def test_form_error_display(self):
        '''Test que los errores se muestran con clases correctas'''
        pass
"""

# ============================================================================
# EJEMPLO 2: Tests de seguridad (CSRF)
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase, Client as DjangoTestClient
from django.urls import reverse
from django.middleware.csrf import get_token

class ClientSecurityTests(TestCase):
    '''Tests de seguridad para vistas de Client'''
    
    def setUp(self):
        self.test_client = DjangoTestClient(enforce_csrf_checks=True)
    
    def test_csrf_token_required_on_post(self):
        '''Test que el token CSRF es requerido en POST'''
        # GET para obtener el token CSRF
        response = self.test_client.get(reverse('clients:add'))
        csrf_token = response.context['csrf_token']
        
        # POST con token válido
        response = self.test_client.post(
            reverse('clients:add'),
            {'company_name': 'Test', 'name': 'Test'},
            HTTP_X_CSRFTOKEN=csrf_token,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_xss_protection(self):
        '''Test que el HTML se escapa correctamente'''
        from clients.models import Client
        
        malicious_data = '<script>alert("XSS")</script>'
        client = Client.objects.create(
            company_name=malicious_data,
            name='Test'
        )
        
        response = self.test_client.get(reverse('clients:list'))
        # El script no debe ejecutarse
        self.assertNotIn('<script>', response.content.decode())
"""

# ============================================================================
# EJEMPLO 3: Tests de performance/querycount
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase
from django.test.utils import override_settings
from django.db import connection
from django.db.models import prefetch_related_objects
from django.test import Client as DjangoTestClient
from django.urls import reverse
from clients.models import Client

class ClientPerformanceTests(TestCase):
    '''Tests de performance para vistas de Client'''
    
    def setUp(self):
        self.test_client = DjangoTestClient()
        # Crear 100 clientes
        for i in range(100):
            Client.objects.create(
                company_name=f'Company {i}',
                name=f'Contact {i}'
            )
    
    def test_client_list_query_count(self):
        '''Test que la lista no hace N+1 queries'''
        from django.test import override_settings
        
        with self.assertNumQueries(2):  # Solo 2 queries
            response = self.test_client.get(reverse('clients:list'))
            list(response.context['object_list'])
    
    @override_settings(DEBUG=True)
    def test_list_view_optimized(self):
        '''Test que la lista está optimizada'''
        from django.db import connection, reset_queries
        
        reset_queries()
        response = self.test_client.get(reverse('clients:list'))
        
        num_queries = len(connection.queries)
        self.assertLess(num_queries, 5, 
                       f"View hace {num_queries} queries, máximo 5")
"""

# ============================================================================
# EJEMPLO 4: Tests de validación compleja
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from clients.models import Client
from clients.forms import ClientForm

class ClientValidationTests(TestCase):
    '''Tests de validación avanzada para Client'''
    
    def test_cuit_format_validation(self):
        '''Test validación del formato CUIT/CUIL'''
        # CUIT válido: XX-XXXXXXXX-X
        valid_cuit = '20-12345678-9'
        client = Client(
            company_name='Test',
            name='Test',
            tax_id=valid_cuit
        )
        client.full_clean()  # No debe lanzar excepción
    
    def test_email_domain_validation(self):
        '''Test que solo emails válidos se aceptan'''
        invalid_emails = [
            'test@',           # Sin dominio
            '@example.com',    # Sin user
            'test@.com',       # Sin dominio
            'test @example.com',  # Espacio en blanco
        ]
        
        for email in invalid_emails:
            client = Client(
                company_name='Test',
                name='Test',
                email=email
            )
            with self.assertRaises(ValidationError):
                client.full_clean()
    
    def test_phone_length_validation(self):
        '''Test que el teléfono tiene límite de caracteres'''
        # Max 50 caracteres
        client = Client(
            company_name='Test',
            name='Test',
            phone='1' * 51  # 51 caracteres
        )
        with self.assertRaises(ValidationError):
            client.full_clean()
"""

# ============================================================================
# EJEMPLO 5: Tests con fixtures y Factory
# ============================================================================

"""
# En: src/conftest.py

import factory
from clients.models import Client
from suppliers.models import Supplier

class ClientFactory(factory.django.DjangoModelFactory):
    '''Factory para crear clientes en tests'''
    class Meta:
        model = Client
    
    company_name = factory.Faker('company')
    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    tax_id = factory.Sequence(lambda n: f'20-{n:08d}-9')
    is_active = True

class SupplierFactory(factory.django.DjangoModelFactory):
    '''Factory para crear proveedores en tests'''
    class Meta:
        model = Supplier
    
    company_name = factory.Faker('company')
    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    tax_id = factory.Sequence(lambda n: f'30-{n:08d}-2')

# Uso:
# client = ClientFactory()
# suppliers = ClientFactory.create_batch(10)
# client_batch = ClientFactory.create_batch(5, is_active=False)
"""

# ============================================================================
# EJEMPLO 6: Tests de integración end-to-end
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase, Client as DjangoTestClient
from django.urls import reverse
from clients.models import Client

class ClientIntegrationTests(TestCase):
    '''Tests de integración completos'''
    
    def setUp(self):
        self.test_client = DjangoTestClient()
    
    def test_complete_client_workflow(self):
        '''Test flujo completo: crear -> editar -> ver -> eliminar'''
        
        # 1. Agregar cliente
        client_data = {
            'company_name': 'Nueva Empresa',
            'name': 'Juan Pérez',
            'email': 'juan@empresa.com',
            'phone': '+54 11 1234-5678',
            'address': 'Calle Principal 123'
        }
        response = self.test_client.post(reverse('clients:add'), client_data)
        self.assertEqual(response.status_code, 302)
        
        # 2. Verificar que se creó
        client = Client.objects.get(company_name='Nueva Empresa')
        self.assertIsNotNone(client)
        
        # 3. Editar cliente
        updated_data = client_data.copy()
        updated_data['phone'] = '+54 11 9999-9999'
        response = self.test_client.post(
            reverse('clients:edit', args=[client.id]),
            updated_data
        )
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar edición
        client.refresh_from_db()
        self.assertEqual(client.phone, '+54 11 9999-9999')
        
        # 5. Ver detalle
        response = self.test_client.get(
            reverse('clients:detail', args=[client.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nueva Empresa')
        
        # 6. Eliminar
        response = self.test_client.post(
            reverse('clients:delete', args=[client.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.filter(id=client.id).count(), 0)
"""

# ============================================================================
# EJEMPLO 7: Tests parametrizados
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from clients.models import Client
from parameterized import parameterized

class ClientParameterizedTests(TestCase):
    '''Tests parametrizados para múltiples casos'''
    
    @parameterized.expand([
        ('test@example.com', True),
        ('invalid.email', False),
        ('user@domain.co.uk', True),
        ('@example.com', False),
        ('user@', False),
    ])
    def test_email_validation(self, email, should_be_valid):
        '''Test validación de email con múltiples casos'''
        client = Client(company_name='Test', name='Test', email=email)
        
        if should_be_valid:
            client.full_clean()  # No debe lanzar excepción
        else:
            with self.assertRaises(ValidationError):
                client.full_clean()
    
    @parameterized.expand([
        ('20-12345678-9', True),    # CUIT válido
        ('30-87654321-2', True),    # CUIL válido
        ('invalid-cuit', True),     # Aceptamos cualquier formato
    ])
    def test_tax_id_format(self, tax_id, should_be_valid):
        '''Test formato de CUIT/CUIL'''
        client = Client(
            company_name='Test',
            name='Test',
            tax_id=tax_id
        )
        if should_be_valid:
            client.full_clean()
"""

# ============================================================================
# EJEMPLO 8: Tests asincronos (si usas Django async)
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TransactionTestCase
from asgiref.sync import async_to_sync
from clients.models import Client

class ClientAsyncTests(TransactionTestCase):
    '''Tests para vistas async'''
    
    def test_async_client_fetch(self):
        '''Test que se puede obtener cliente de forma async'''
        
        @async_to_sync
        async def get_client_async():
            return await Client.objects.acreate(
                company_name='Async Client',
                name='Test'
            )
        
        client = get_client_async()
        self.assertIsNotNone(client.id)
"""

# ============================================================================
# EJEMPLO 9: Snapshots/Golden files
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase
from django.test.client import Client as DjangoTestClient
import json

class ClientSnapshotTests(TestCase):
    '''Tests usando snapshots para cambios de API'''
    
    def test_client_json_response(self):
        '''Test que la respuesta JSON no ha cambiado'''
        from clients.models import Client
        
        client = Client.objects.create(
            company_name='Test',
            name='Test Contact',
            email='test@example.com'
        )
        
        response_data = {
            'id': client.id,
            'company_name': client.company_name,
            'name': client.name,
            'email': client.email,
        }
        
        # En producción, compararías con un archivo .json guardado
        expected_snapshot = {
            'company_name': 'Test',
            'name': 'Test Contact',
            'email': 'test@example.com',
        }
        
        self.assertEqual(
            response_data['company_name'],
            expected_snapshot['company_name']
        )
"""

# ============================================================================
# EJEMPLO 10: Mocking de dependencias externas
# ============================================================================

"""
# En: src/clients/tests.py

from django.test import TestCase
from unittest.mock import patch, MagicMock
from clients.models import Client

class ClientExternalServiceTests(TestCase):
    '''Tests que mockean servicios externos'''
    
    @patch('clients.views.send_email')
    def test_client_creation_sends_email(self, mock_send_email):
        '''Test que se envía email al crear cliente'''
        
        mock_send_email.return_value = True
        
        # Simular vista que envía email
        # response = self.client.post(reverse('clients:add'), data)
        
        # mock_send_email.assert_called_once()
        # args, kwargs = mock_send_email.call_args
        # self.assertIn('test@example.com', args)
    
    @patch('requests.get')
    def test_validate_with_external_api(self, mock_get):
        '''Test validación contra API externa'''
        
        mock_response = MagicMock()
        mock_response.json.return_value = {'valid': True}
        mock_get.return_value = mock_response
        
        # Código que llama a API externa
        client = Client(company_name='Test', name='Test')
        # validate_with_external_api(client)
        
        # mock_get.assert_called_once()
"""

# ============================================================================
# INSTALACIÓN DE DEPENDENCIAS
# ============================================================================

"""
Para usar los ejemplos anteriores, instala:

pip install factory-boy       # Para ClientFactory
pip install parameterized     # Para tests parametrizados
pip install django-waffle     # Para feature flags en tests
pip install responses         # Para mockear HTTP requests

O todo junto:
pip install -r requirements-testing.txt
"""
