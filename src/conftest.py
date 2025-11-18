"""
Configuración y fixtures comunes para tests.

NOTA: Este archivo es opcional para tests con Django TestCase.
Si quieres usar pytest fixtures, instala: pip install pytest-django

Para los tests actuales con Django TestCase, este archivo no es necesario
pero está disponible para futuros tests con pytest.
"""

try:
    import pytest
    
    @pytest.fixture
    def client_data():
        """Datos de cliente para tests"""
        from clients.models import Client
        return {
            'company_name': 'Test Company',
            'name': 'Test Contact',
            'email': 'test@example.com',
            'phone': '+54 11 1234-5678',
            'address': 'Test Address 123',
            'tax_id': '20-12345678-9',
        }

    @pytest.fixture
    def supplier_data():
        """Datos de proveedor para tests"""
        from suppliers.models import Supplier
        return {
            'company_name': 'Test Supplier',
            'name': 'Test Contact',
            'email': 'supplier@example.com',
            'phone': '+54 11 5678-1234',
            'address': 'Supplier Address 456',
            'tax_id': '30-87654321-2',
        }

    @pytest.fixture
    def client_obj(db, client_data):
        """Crea un cliente para tests"""
        from clients.models import Client
        return Client.objects.create(**client_data)

    @pytest.fixture
    def supplier_obj(db, supplier_data):
        """Crea un proveedor para tests"""
        from suppliers.models import Supplier
        return Supplier.objects.create(**supplier_data)

    @pytest.fixture
    def multiple_clients(db, client_data):
        """Crea múltiples clientes para tests"""
        from clients.models import Client
        clients = []
        for i in range(5):
            data = client_data.copy()
            data['company_name'] = f"{data['company_name']} {i}"
            data['name'] = f"{data['name']} {i}"
            data['email'] = f"client{i}@example.com"
            clients.append(Client.objects.create(**data))
        return clients

    @pytest.fixture
    def multiple_suppliers(db, supplier_data):
        """Crea múltiples proveedores para tests"""
        from suppliers.models import Supplier
        suppliers = []
        for i in range(5):
            data = supplier_data.copy()
            data['company_name'] = f"{data['company_name']} {i}"
            data['name'] = f"{data['name']} {i}"
            data['email'] = f"supplier{i}@example.com"
            suppliers.append(Supplier.objects.create(**data))
        return suppliers

except ImportError:
    # pytest no está instalado, lo cual es OK para tests con Django TestCase
    # Si quieres usar pytest fixtures, instala: pip install pytest-django
    pass
