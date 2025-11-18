from django.test import TestCase, Client as DjangoTestClient
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Supplier
from .forms import SupplierForm


class SupplierModelTests(TestCase):
    """Tests para el modelo Supplier"""

    def setUp(self):
        """Configuración inicial"""
        self.supplier = Supplier.objects.create(
            company_name="Proveedor Test",
            name="Contacto Proveedor",
            email="supplier@test.com",
            phone="+54 11 5678-1234",
            address="Calle Proveedor 456",
            tax_id="30-87654321-2",
            notes="Notas de proveedor"
        )

    def test_supplier_creation(self):
        """Test creación de proveedor"""
        self.assertIsNotNone(self.supplier.id)
        self.assertEqual(self.supplier.company_name, "Proveedor Test")
        self.assertEqual(self.supplier.notes, "Notas de proveedor")

    def test_supplier_notes_field(self):
        """Test que notes puede ser nulo"""
        supplier = Supplier.objects.create(
            company_name="Test",
            name="Test"
        )
        self.assertIsNone(supplier.notes)

    def test_supplier_string_representation(self):
        """Test __str__"""
        expected = "Proveedor Test - Contacto Proveedor"
        self.assertEqual(str(self.supplier), expected)

    def test_supplier_with_empty_notes(self):
        """Test proveedor con notas vacías"""
        supplier = Supplier.objects.create(
            company_name="Test",
            name="Test",
            notes=""
        )
        self.assertEqual(supplier.notes, "")

    def test_supplier_update_notes(self):
        """Test actualización de notas"""
        self.supplier.notes = "Nuevas notas de proveedor"
        self.supplier.save()
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.notes, "Nuevas notas de proveedor")


class SupplierFormTests(TestCase):
    """Tests para el formulario SupplierForm"""

    def test_form_valid_data(self):
        """Test formulario con datos válidos"""
        form = SupplierForm(data={
            'company_name': 'Test Supplier',
            'name': 'Test Name',
            'email': 'supplier@example.com',
            'phone': '+54 11 5678',
            'address': 'Test Address',
            'tax_id': '30-87654321-2',
            'notes': 'Test notes',
            'is_active': True
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_required_field(self):
        """Test formulario sin campo obligatorio"""
        form = SupplierForm(data={
            'name': 'Test Name',
            'email': 'supplier@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_form_invalid_email(self):
        """Test formulario con email inválido"""
        form = SupplierForm(data={
            'company_name': 'Test',
            'name': 'Test',
            'email': 'invalid-email'
        })
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        """Test guardar formulario"""
        form = SupplierForm(data={
            'company_name': 'Test Supplier',
            'name': 'Test Name',
            'email': 'supplier@example.com',
            'phone': '+54 11 5678',
            'address': 'Test Address',
            'tax_id': '30-87654321-2',
            'is_active': True
        })
        self.assertTrue(form.is_valid())
        supplier = form.save()
        self.assertIsNotNone(supplier.id)
        self.assertEqual(Supplier.objects.count(), 1)

    def test_form_edit(self):
        """Test editar a través del formulario"""
        supplier = Supplier.objects.create(
            company_name='Original',
            name='Original Name'
        )
        
        form = SupplierForm(data={
            'company_name': 'Updated',
            'name': 'Updated Name',
            'is_active': True
        }, instance=supplier)
        
        self.assertTrue(form.is_valid())
        updated_supplier = form.save()
        self.assertEqual(updated_supplier.company_name, 'Updated')


class SupplierViewsTests(TestCase):
    """Tests para las vistas de Supplier"""

    def setUp(self):
        """Configuración inicial"""
        self.supplier_data = {
            'company_name': 'Test Supplier',
            'name': 'Test Contact',
            'email': 'supplier@example.com',
            'phone': '+54 11 5678',
            'address': 'Test Address',
            'tax_id': '30-87654321-2'
        }
        self.test_client = DjangoTestClient()

    def test_supplier_list_view(self):
        """Test vista de listado"""
        Supplier.objects.create(**self.supplier_data)
        response = self.test_client.get(reverse('suppliers:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/list.html')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_supplier_list_empty(self):
        """Test lista vacía"""
        response = self.test_client.get(reverse('suppliers:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)

    def test_supplier_add_view_get(self):
        """Test GET en vista de agregar"""
        response = self.test_client.get(reverse('suppliers:add'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/add.html')
        self.assertIsInstance(response.context['form'], SupplierForm)

    def test_supplier_add_view_post(self):
        """Test POST en vista de agregar"""
        response = self.test_client.post(reverse('suppliers:add'), self.supplier_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Supplier.objects.count(), 1)
        created_supplier = Supplier.objects.first()
        self.assertEqual(created_supplier.company_name, 'Test Supplier')

    def test_supplier_add_view_post_with_messages(self):
        """Test POST con mensaje de éxito"""
        response = self.test_client.post(reverse('suppliers:add'), self.supplier_data, follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Proveedor creado correctamente.")

    def test_supplier_add_view_invalid_data(self):
        """Test POST con datos inválidos"""
        invalid_data = {'name': 'Test'}
        response = self.test_client.post(reverse('suppliers:add'), invalid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_supplier_edit_view_get(self):
        """Test GET en vista de editar"""
        supplier = Supplier.objects.create(**self.supplier_data)
        response = self.test_client.get(reverse('suppliers:edit', args=[supplier.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/edit.html')
        self.assertEqual(response.context['form'].instance.id, supplier.id)

    def test_supplier_edit_view_post(self):
        """Test POST en vista de editar"""
        supplier = Supplier.objects.create(**self.supplier_data)
        updated_data = self.supplier_data.copy()
        updated_data['company_name'] = 'Updated Supplier'
        
        response = self.test_client.post(
            reverse('suppliers:edit', args=[supplier.id]),
            updated_data
        )
        
        self.assertEqual(response.status_code, 302)
        supplier.refresh_from_db()
        self.assertEqual(supplier.company_name, 'Updated Supplier')

    def test_supplier_edit_nonexistent(self):
        """Test editar proveedor inexistente"""
        response = self.test_client.get(reverse('suppliers:edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_supplier_detail_view(self):
        """Test vista de detalle"""
        supplier = Supplier.objects.create(**self.supplier_data)
        response = self.test_client.get(reverse('suppliers:detail', args=[supplier.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/detail.html')
        self.assertEqual(response.context['entity'].id, supplier.id)

    def test_supplier_detail_nonexistent(self):
        """Test detalle de proveedor inexistente"""
        response = self.test_client.get(reverse('suppliers:detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_supplier_delete_view(self):
        """Test vista de eliminar"""
        supplier = Supplier.objects.create(**self.supplier_data)
        response = self.test_client.post(reverse('suppliers:delete', args=[supplier.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_supplier_delete_with_messages(self):
        """Test eliminar con mensaje de éxito"""
        supplier = Supplier.objects.create(**self.supplier_data)
        response = self.test_client.post(reverse('suppliers:delete', args=[supplier.id]), follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Proveedor eliminado correctamente.")

    def test_supplier_delete_nonexistent(self):
        """Test eliminar proveedor inexistente"""
        response = self.test_client.post(reverse('suppliers:delete', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_supplier_edit_select_view(self):
        """Test vista de seleccionar proveedor para editar"""
        Supplier.objects.create(**self.supplier_data)
        response = self.test_client.get(reverse('suppliers:edit_select'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/edit_select.html')
        self.assertEqual(len(response.context['suppliers']), 1)
