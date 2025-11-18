from django.test import TestCase, Client as DjangoTestClient
from django.urls import reverse
from .models import Client
from .forms import ClientForm


class ClientModelTests(TestCase):
    """Tests para el modelo Client"""

    def setUp(self):
        """Configuración inicial"""
        self.client = Client.objects.create(
            company_name="Empresa Test",
            name="Contacto Test",
            email="contact@test.com",
            phone="+54 11 1234-5678",
            address="Calle Test 123",
            tax_id="20-12345678-9",
            notes="Notas de prueba"
        )

    def test_client_creation(self):
        """Test creación de cliente"""
        self.assertIsNotNone(self.client.id)
        self.assertEqual(self.client.company_name, "Empresa Test")
        self.assertEqual(self.client.notes, "Notas de prueba")

    def test_client_notes_field(self):
        """Test que notes puede ser nulo"""
        client = Client.objects.create(
            company_name="Test",
            name="Test"
        )
        self.assertIsNone(client.notes)

    def test_client_string_representation(self):
        """Test __str__"""
        expected = "Empresa Test - Contacto Test"
        self.assertEqual(str(self.client), expected)

    def test_client_with_empty_notes(self):
        """Test cliente con notas vacías"""
        client = Client.objects.create(
            company_name="Test",
            name="Test",
            notes=""
        )
        self.assertEqual(client.notes, "")

    def test_client_update_notes(self):
        """Test actualización de notas"""
        self.client.notes = "Nuevas notas"
        self.client.save()
        self.client.refresh_from_db()
        self.assertEqual(self.client.notes, "Nuevas notas")


class ClientFormTests(TestCase):
    """Tests para el formulario ClientForm"""

    def test_form_valid_data(self):
        """Test formulario con datos válidos"""
        form = ClientForm(data={
            'company_name': 'Test Company',
            'name': 'Test Name',
            'email': 'test@example.com',
            'phone': '+54 11 1234',
            'address': 'Test Address',
            'tax_id': '20-12345678-9',
            'notes': 'Test notes',
            'is_active': True
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_required_field(self):
        """Test formulario sin campo obligatorio"""
        form = ClientForm(data={
            'name': 'Test Name',
            'email': 'test@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_form_invalid_email(self):
        """Test formulario con email inválido"""
        form = ClientForm(data={
            'company_name': 'Test',
            'name': 'Test',
            'email': 'invalid-email'
        })
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        """Test guardar formulario"""
        form = ClientForm(data={
            'company_name': 'Test Company',
            'name': 'Test Name',
            'email': 'test@example.com',
            'phone': '+54 11 1234',
            'address': 'Test Address',
            'tax_id': '20-12345678-9',
            'is_active': True
        })
        self.assertTrue(form.is_valid())
        client = form.save()
        self.assertIsNotNone(client.id)
        self.assertEqual(Client.objects.count(), 1)

    def test_form_edit(self):
        """Test editar a través del formulario"""
        client = Client.objects.create(
            company_name='Original',
            name='Original Name'
        )
        
        form = ClientForm(data={
            'company_name': 'Updated',
            'name': 'Updated Name',
            'is_active': True
        }, instance=client)
        
        self.assertTrue(form.is_valid())
        updated_client = form.save()
        self.assertEqual(updated_client.company_name, 'Updated')


class ClientViewsTests(TestCase):
    """Tests para las vistas de Client"""

    def setUp(self):
        """Configuración inicial"""
        self.client_data = {
            'company_name': 'Test Company',
            'name': 'Test Contact',
            'email': 'test@example.com',
            'phone': '+54 11 1234',
            'address': 'Test Address',
            'tax_id': '20-12345678-9'
        }
        self.test_client = DjangoTestClient()

    def test_client_list_view(self):
        """Test vista de listado"""
        Client.objects.create(**self.client_data)
        response = self.test_client.get(reverse('clients:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/list.html')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_client_list_empty(self):
        """Test lista vacía"""
        response = self.test_client.get(reverse('clients:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)

    def test_client_add_view_get(self):
        """Test GET en vista de agregar"""
        response = self.test_client.get(reverse('clients:add'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/add.html')
        self.assertIsInstance(response.context['form'], ClientForm)

    def test_client_add_view_post(self):
        """Test POST en vista de agregar"""
        response = self.test_client.post(reverse('clients:add'), self.client_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.count(), 1)
        created_client = Client.objects.first()
        self.assertEqual(created_client.company_name, 'Test Company')

    def test_client_add_view_invalid_data(self):
        """Test POST con datos inválidos"""
        invalid_data = {'name': 'Test'}
        response = self.test_client.post(reverse('clients:add'), invalid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Client.objects.count(), 0)

    def test_client_edit_view_get(self):
        """Test GET en vista de editar"""
        client = Client.objects.create(**self.client_data)
        response = self.test_client.get(reverse('clients:edit', args=[client.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/edit.html')
        self.assertEqual(response.context['form'].instance.id, client.id)

    def test_client_edit_view_post(self):
        """Test POST en vista de editar"""
        client = Client.objects.create(**self.client_data)
        updated_data = self.client_data.copy()
        updated_data['company_name'] = 'Updated Company'
        
        response = self.test_client.post(
            reverse('clients:edit', args=[client.id]),
            updated_data
        )
        
        self.assertEqual(response.status_code, 302)
        client.refresh_from_db()
        self.assertEqual(client.company_name, 'Updated Company')

    def test_client_edit_nonexistent(self):
        """Test editar cliente inexistente"""
        response = self.test_client.get(reverse('clients:edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_client_detail_view(self):
        """Test vista de detalle"""
        client = Client.objects.create(**self.client_data)
        response = self.test_client.get(reverse('clients:detail', args=[client.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/detail.html')
        self.assertEqual(response.context['entity'].id, client.id)

    def test_client_detail_nonexistent(self):
        """Test detalle de cliente inexistente"""
        response = self.test_client.get(reverse('clients:detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_client_delete_view(self):
        """Test vista de eliminar"""
        client = Client.objects.create(**self.client_data)
        response = self.test_client.post(reverse('clients:delete', args=[client.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.count(), 0)

    def test_client_delete_nonexistent(self):
        """Test eliminar cliente inexistente"""
        response = self.test_client.post(reverse('clients:delete', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_client_edit_select_view(self):
        """Test vista de seleccionar cliente para editar"""
        Client.objects.create(**self.client_data)
        response = self.test_client.get(reverse('clients:edit_select'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/edit_select.html')
        self.assertEqual(len(response.context['clients']), 1)
