# 🚀 Quick Start - Testing

## 5 Minutos para Empezar

### 1️⃣ Activar Entorno Virtual
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 2️⃣ Ejecutar Tests
```bash
cd src
python manage.py test --verbosity=2
```

**Resultado esperado:**
```
Ran 61 tests in 0.406s
OK ✅
```

## Comandos Comunes

```bash
# Ver todos los tests
python manage.py test --verbosity=2

# Solo Client tests
python manage.py test clients

# Solo Supplier tests
python manage.py test suppliers

# Con cobertura
cd src
coverage run --source='.' manage.py test
coverage report

# Test específico
python manage.py test clients.tests.ClientViewsTests.test_client_list_view

# Run failing tests first
python manage.py test --failfast
```

## Estructura de Tests

```
Cada app tiene un archivo tests.py:

clients/tests.py:
  ├── ClientModelTests (5)
  ├── ClientFormTests (5)
  └── ClientViewsTests (12)

suppliers/tests.py:
  ├── SupplierModelTests (5)
  ├── SupplierFormTests (5)
  └── SupplierViewsTests (14)

core/tests.py:
  ├── EntityModelTests (11)
  └── CoreViewsTests (2)
```

## 📖 Documentación

- **[TESTING.md](TESTING.md)** - Guía completa
- **[TESTING_EXAMPLES.md](TESTING_EXAMPLES.md)** - Ejemplos avanzados
- **[CI_CD.md](CI_CD.md)** - Integración continua
- **[TEST_SUMMARY.md](TEST_SUMMARY.md)** - Resumen

## 🎯 Escribir Nuevo Test

### Ejemplo Simple

```python
# En: src/clients/tests.py

class ClientNewTests(TestCase):
    """Nuevo test para clientes"""
    
    def test_client_is_active_by_default(self):
        """Test que cliente está activo por defecto"""
        from clients.models import Client
        
        client = Client.objects.create(
            company_name="Test",
            name="Test"
        )
        
        self.assertTrue(client.is_active)
```

### Ejecutar Solo Tu Test

```bash
python manage.py test clients.tests.ClientNewTests.test_client_is_active_by_default
```

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named..."
```bash
pip install -r requirements.txt
```

### Error: "No such table..."
```bash
cd src
python manage.py migrate
```

### Tests muy lentos
```bash
# Tests en paralelo (requiere django-parallel)
python manage.py test --parallel
```

## 📊 Ver Cobertura

```bash
cd src
coverage run --source='.' manage.py test
coverage html
# Abre htmlcov/index.html en navegador
```

## 🔄 Auto-run en Cambios

```bash
# Instala watchdog
pip install watchdog[watchmedo]

# Crea test-watch.sh con el código de CI_CD.md
chmod +x test-watch.sh
./test-watch.sh
```

## ✅ Checklist Pre-Commit

Antes de hacer commit:
- [ ] Ejecuté `python manage.py test`
- [ ] Todos los tests pasaron
- [ ] Agregué tests para nuevas features
- [ ] La cobertura se mantuvo o mejoró

## 📱 Mobile Testing (Opcional)

```bash
# Probar en diferentes navegadores
pip install selenium
python -m pytest --cov
```

## 🐛 Debug de Tests

```bash
# Ver queries SQL
python manage.py test --debug-sql

# Con pdb (debugger)
python -m pdb manage.py test

# Verbose completo
python manage.py test --verbosity=3
```

## 📚 Recursos Rápidos

| Necesito... | Comando |
|-----------|---------|
| Ver todos los tests | `python manage.py test --verbosity=2` |
| Cobertura | `coverage report` |
| Tests de un modelo | `python manage.py test core.tests.EntityModelTests` |
| Test específico | `python manage.py test clients.tests.ClientViewsTests.test_client_list_view` |
| Sin parar en primer error | `python manage.py test` |
| Parar en primer error | `python manage.py test --failfast` |
| Tests nuevos solo | `python manage.py test --liveserver=localhost:8001` |

## 🎓 Aprender Más

1. Lee [TESTING.md](TESTING.md) para entender la estrategia
2. Mira [TESTING_EXAMPLES.md](TESTING_EXAMPLES.md) para patrones
3. Consulta [CI_CD.md](CI_CD.md) para automatización
4. Revisa [TEST_SUMMARY.md](TEST_SUMMARY.md) para estadísticas

## ✨ Comando Favorito

```bash
# Ejecuta tests + cobertura + abre reporte
cd src && python manage.py test && coverage report && coverage html && start htmlcov/index.html
```

---

**Ya estás listo para testear. ¡Adelante! 🚀**
