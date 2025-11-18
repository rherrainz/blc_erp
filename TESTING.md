# Guía de Testing - BLC ERP

## Visión General

Este documento describe la estrategia de testing para el sistema BLC ERP, incluyendo:
- Tests de modelos
- Tests de formularios
- Tests de vistas (HTTP)
- Tests de integración

## Estructura de Tests

Los tests están organizados en la carpeta `src/` bajo cada aplicación Django:

```
src/
├── core/
│   └── tests.py              # Tests para Entity model y vistas core
├── clients/
│   └── tests.py              # Tests para Client model, form y vistas
├── suppliers/
│   └── tests.py              # Tests para Supplier model, form y vistas
├── conftest.py               # Fixtures compartidas (pytest)
└── manage.py
```

## Tipos de Tests

### 1. Tests de Modelos

Validan la lógica de los modelos Django:

```bash
# Test solo modelos de Entity
python manage.py test core.tests.EntityModelTests

# Test solo modelos de Client
python manage.py test clients.tests.ClientModelTests

# Test solo modelos de Supplier
python manage.py test suppliers.tests.SupplierModelTests
```

**Qué se prueba:**
- Creación de registros
- Campos obligatorios vs opcionales
- Valores por defecto
- Validación de datos (email, CUIT, etc)
- Operaciones CRUD (Create, Read, Update, Delete)
- Representación en string (`__str__`)
- Filtrado de querysets

### 2. Tests de Formularios

Validan la lógica de validación en formularios:

```bash
# Test formularios de Client
python manage.py test clients.tests.ClientFormTests

# Test formularios de Supplier
python manage.py test suppliers.tests.SupplierFormTests
```

**Qué se prueba:**
- Validación de datos correctos
- Rechazo de datos inválidos
- Campos requeridos
- Validación de email
- Guardado de formulario
- Edición de instancias existentes

### 3. Tests de Vistas

Validan las vistas HTTP (rutas, templates, contextos):

```bash
# Test vistas de Client
python manage.py test clients.tests.ClientViewsTests

# Test vistas de Supplier
python manage.py test suppliers.tests.SupplierViewsTests

# Test vistas de Core
python manage.py test core.tests.CoreViewsTests
```

**Qué se prueba:**
- Status HTTP (200, 302, 404, etc)
- Templates renderizados
- Datos en el contexto
- Redirecciones post-operación
- Mensajes (messages framework)
- Métodos HTTP (GET, POST)

## Ejecutar Tests

### Ejecutar todos los tests
```bash
cd src
python manage.py test
```

### Ejecutar tests de una aplicación específica
```bash
python manage.py test clients
python manage.py test suppliers
python manage.py test core
```

### Ejecutar una clase de tests específica
```bash
python manage.py test clients.tests.ClientViewsTests
```

### Ejecutar un test específico
```bash
python manage.py test clients.tests.ClientViewsTests.test_client_list_view
```

### Ejecutar con verbosity (más detalles)
```bash
python manage.py test --verbosity=2
```

### Ejecutar con coverage (cobertura de código)
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

## Fixtures (pytest)

Se proporciona un archivo `conftest.py` con fixtures reutilizables:

```python
# conftest.py contiene:
- client_data: Datos de ejemplo para un cliente
- supplier_data: Datos de ejemplo para un proveedor
- client_obj: Fixture que crea un cliente en BD
- supplier_obj: Fixture que crea un proveedor en BD
- multiple_clients: Fixture que crea 5 clientes
- multiple_suppliers: Fixture que crea 5 proveedores
```

### Uso de fixtures (con pytest)
```bash
pip install pytest-django
pytest
```

## Casos de Prueba Cubiertos

### Entity Model
- ✅ Creación de entidades
- ✅ Campos obligatorios vs opcionales
- ✅ Valor por defecto de is_active
- ✅ Validación de email
- ✅ Actualización de registros
- ✅ Eliminación de registros
- ✅ Filtrado por estado (is_active)

### Client Model
- ✅ Creación con y sin notas
- ✅ Representación en string
- ✅ Actualización de notas
- ✅ Herencia de Entity

### Client Form
- ✅ Validación de datos correctos
- ✅ Campos requeridos
- ✅ Email inválido
- ✅ Guardado de nuevos registros
- ✅ Edición de registros existentes

### Client Views
- ✅ Listado (GET)
- ✅ Listado vacío
- ✅ Agregar - GET
- ✅ Agregar - POST válido
- ✅ Agregar - POST inválido
- ✅ Editar - GET
- ✅ Editar - POST
- ✅ Editar cliente inexistente (404)
- ✅ Detalle - GET
- ✅ Detalle cliente inexistente (404)
- ✅ Eliminar - POST
- ✅ Eliminar cliente inexistente (404)
- ✅ Seleccionar para editar

### Supplier (similar a Client)
- ✅ Model CRUD operations
- ✅ Form validation
- ✅ Views HTTP tests
- ✅ Messages framework

### Core Views
- ✅ Home page GET
- ✅ Template rendering

## Mejores Prácticas

1. **Usa setUp()** para inicializar datos comunes antes de cada test
2. **Usa fixtures** (pytest) o `@classmethod setUpClass()` para datos costosos
3. **Escribe tests pequeños y enfocados** - una cosa por test
4. **Nombre descriptivo** - `test_client_add_view_post_valid_data`
5. **Usa descriptores** en docstrings: `"""Test que se crea un cliente""""`
6. **Limpia datos** - tearDown() se ejecuta automáticamente
7. **Testa casos extremos** - valores nulos, strings vacíos, etc

## Ejemplo de Test

```python
def test_client_add_view_post(self):
    """Test POST en vista de agregar cliente"""
    client_data = {
        'company_name': 'Test Company',
        'name': 'Test Contact',
        'email': 'test@example.com',
    }
    response = self.test_client.post(reverse('clients:add'), client_data)
    
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertEqual(Client.objects.count(), 1)   # Verify creation
    created = Client.objects.first()
    self.assertEqual(created.company_name, 'Test Company')  # Verify data
```

## Troubleshooting

### Error: "No such table: ..."
Asegúrate de que las migraciones se ejecutaron en la BD de tests:
```bash
python manage.py migrate
```

### Error: "Reverse for 'view_name' not found"
Verifica que los nombres de las URLs en `urls.py` coincidan con los usados en `reverse()`.

### Test muy lento
- Usa `@classmethod setUpClass()` en lugar de `setUp()` para datos costosos
- Considera usar índices en modelos para querysets
- Usa `django.test.TransactionTestCase` solo si es necesario

## Cobertura Actual

Se proporciona testing comprehensivo para:

| Componente | Tests | Cobertura |
|-----------|-------|----------|
| Entity Model | 11 | ~95% |
| Client Model | 5 | ~90% |
| Client Form | 5 | ~95% |
| Client Views | 12 | ~95% |
| Supplier Model | 5 | ~90% |
| Supplier Form | 5 | ~95% |
| Supplier Views | 12 | ~95% |
| Core Views | 2 | ~90% |
| **TOTAL** | **57** | **~92%** |

## Próximos Pasos

Para mejorar la cobertura:
1. Tests de templatetags (form_filters.py)
2. Tests de integración end-to-end
3. Tests de performance/carga
4. Tests de seguridad (CSRF, XSS, etc)
