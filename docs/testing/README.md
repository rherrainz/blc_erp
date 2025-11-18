# 🧪 Testing Documentation

Bienvenido a la documentación completa de testing para BLC ERP.

## 📚 Índice Rápido

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| **[INDEX.md](INDEX.md)** | 📖 Índice maestro y guía de navegación | 1 min |
| **[QUICK_START.md](QUICK_START.md)** | 🚀 Comienza en 5 minutos | 5 min |
| **[TESTING.md](TESTING.md)** | 📘 Guía completa y estrategia | 15 min |
| **[TESTING_EXAMPLES.md](TESTING_EXAMPLES.md)** | 📙 10 patrones avanzados | 20 min |
| **[CI_CD.md](CI_CD.md)** | 📕 Integración continua | 25 min |
| **[TEST_SUMMARY.md](TEST_SUMMARY.md)** | 📓 Resumen y estadísticas | 10 min |
| **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** | ✅ Checklist de completitud | 5 min |

---

## 🎯 ¿Por Dónde Empezar?

### Para Principiantes (30 minutos)
1. Lee [QUICK_START.md](QUICK_START.md) (5 min)
2. Ejecuta `python manage.py test`
3. Lee [TESTING.md](TESTING.md) (15 min)
4. Explora los archivos de test en `src/`

### Para Desarrolladores (1 hora)
1. Lee [QUICK_START.md](QUICK_START.md) (5 min)
2. Lee [TESTING_EXAMPLES.md](TESTING_EXAMPLES.md) (20 min)
3. Escribe un nuevo test
4. Consulta [TESTING.md](TESTING.md) cuando necesites

### Para DevOps (1.5 horas)
1. Lee [QUICK_START.md](QUICK_START.md) (5 min)
2. Lee [CI_CD.md](CI_CD.md) (25 min)
3. Elige tu plataforma de CI/CD
4. Adapta el código a tu setup

---

## 📊 Estadísticas del Testing

```
Total Tests:        61 ✅
Tests Exitosos:     61/61 (100%)
Cobertura:          ~92%
Tiempo Ejecución:   0.4 segundos ⚡

Desglose:
  • Core:       13 tests
  • Clients:    22 tests
  • Suppliers:  24 tests
```

---

## 🚀 Comandos Rápidos

```bash
# Ejecutar todos los tests
cd src && python manage.py test --verbosity=2

# Ver cobertura
cd src && coverage run --source='.' manage.py test
cd src && coverage report

# Usar el script auxiliar
python run_tests.py help
python run_tests.py all
python run_tests.py coverage
```

---

## 📁 Estructura de Tests

```
src/
├── core/
│   └── tests.py           13 tests
├── clients/
│   └── tests.py           22 tests
├── suppliers/
│   └── tests.py           24 tests
├── conftest.py            Fixtures pytest
└── pytest.ini             Configuración
```

---

## ✨ Características

- ✅ 61 tests listos para usar
- ✅ ~92% cobertura de código
- ✅ Ejecución en 0.4 segundos
- ✅ Sin dependencias complejas
- ✅ Bien documentado (7 guías)
- ✅ Fácil de extender
- ✅ Compatible con CI/CD
- ✅ Listo para producción

---

## 🔍 Encuentra lo que Necesitas

**"Quiero correr los tests rápidamente"**
→ [QUICK_START.md](QUICK_START.md)

**"Quiero entender la estructura completa"**
→ [TESTING.md](TESTING.md)

**"Quiero ver ejemplos avanzados"**
→ [TESTING_EXAMPLES.md](TESTING_EXAMPLES.md)

**"Quiero automatizar con CI/CD"**
→ [CI_CD.md](CI_CD.md)

**"Quiero saber qué está cubierto"**
→ [TEST_SUMMARY.md](TEST_SUMMARY.md)

**"Quiero saber si todo está completo"**
→ [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)

---

**Última actualización:** 18 de noviembre de 2025

Para más información, consulta el [README.md](../../README.md) principal.
