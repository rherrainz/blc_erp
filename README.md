# BLC ERP - Gestión de Clientes y Proveedores

Sistema de gestión web desarrollado como proyecto académico para la materia **Práctica Profesional** – Carrera **Tecnicatura en Tecnologías de la Información**, Universidad Kennedy.

Autor: **Rodrigo Herrainz**

---

## 🛠 Tecnologías utilizadas

- **Python 3.11**
- **Django 4.x**
- **SQLite (por defecto)**
- **Tailwind CSS + DaisyUI**
- **django-tailwind** para integración front-end
- `venv` como entorno virtual

---

## 🚀 Instrucciones de instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu_usuario/blc-erp.git
cd blc-erp/src
```

2. **Crear entorno virtual**

```bash
python -m venv ../venv
source ../venv/bin/activate  # o .\venv\Scripts\activate en Windows
```

3. **Instalar dependencias**

```bash
pip install -r ../requirements.txt
```

4. **Configurar Tailwind**

```bash
cd ui/static_src
npm install
npm run dev  # dejar corriendo para compilar estilos
```

5. **Migraciones iniciales**

```bash
cd ../..
python manage.py migrate
```

6. **Crear superusuario**

```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor**

```bash
python manage.py runserver
```

---

## 🧪 Testing

El proyecto incluye una suite completa de **61 tests** que cubren:
- ✅ Modelos (Entity, Client, Supplier)
- ✅ Formularios (ClientForm, SupplierForm)
- ✅ Vistas HTTP (CRUD operations)

### Ejecutar Tests

```bash
cd src
python manage.py test --verbosity=2
```

**Resultado:** 61 tests en ~0.4 segundos ⚡

### Cobertura

```bash
cd src
coverage run --source='.' manage.py test
coverage report
coverage html  # Abre htmlcov/index.html
```

**Cobertura:** ~92%

### Script Auxiliar

```bash
python run_tests.py help
python run_tests.py all      # Todos los tests
python run_tests.py models   # Solo modelos
python run_tests.py coverage # Con cobertura
```

### 📚 Documentación Completa de Testing

Toda la documentación de testing se encuentra en la carpeta [`docs/testing/`](docs/testing/):

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| **[INDEX.md](docs/testing/INDEX.md)** | 📖 Índice y guía de navegación | 1 min |
| **[QUICK_START.md](docs/testing/QUICK_START.md)** | 🚀 Guía rápida para comenzar | 5 min |
| **[TESTING.md](docs/testing/TESTING.md)** | 📘 Guía completa y detallada | 15 min |
| **[TESTING_EXAMPLES.md](docs/testing/TESTING_EXAMPLES.md)** | 📙 10 patrones y ejemplos avanzados | 20 min |
| **[CI_CD.md](docs/testing/CI_CD.md)** | 📕 Integración continua (GitHub, GitLab, Jenkins) | 25 min |
| **[TEST_SUMMARY.md](docs/testing/TEST_SUMMARY.md)** | 📓 Resumen ejecutivo y estadísticas | 10 min |
| **[TESTING_CHECKLIST.md](docs/testing/TESTING_CHECKLIST.md)** | ✅ Checklist de completitud | 5 min |

---

- **Panel de administración**: http://localhost:8000/admin
- **Sistema**: http://localhost:8000/

---

## 📁 Estructura del proyecto

```
pp/
├── src/
│   ├── blc_erp/        # Proyecto Django
│   ├── core/           # App base (home, layout)
│   ├── clients/        # App de clientes
│   ├── suppliers/      # App de proveedores
│   └── ui/             # App de integración Tailwind
├── venv/               # Entorno virtual (ignorado)
├── requirements.txt
├── .gitignore
└── README.md
```

---
---

## ♻️ Diseño del sistema: reutilización y buenas prácticas

Para mantener el sistema limpio, modular y fácilmente escalable, se implementaron las siguientes prácticas:

### 📦 Reutilización de componentes

- **Componentes visuales compartidos**:
  - Carpeta `ui/templates/components/` para formularios (`form.html`), tarjetas (`list_card.html`), títulos de páginas (`page.html`), etc.
  - Utilizados con `{% include %}` y `with` para pasar contexto dinámico.

- **Partial views**:
  - `partials/navbar.html` y `partials/footer.html` definen el layout superior e inferior, incluidos en `base.html`.

- **Estilo centralizado**:
  - `custom.css` sobrescribe estilos de DaisyUI para mantener coherencia (inputs blancos, bordes visibles, etc.).
  - Archivo generado por Tailwind en `ui/static/css/dist/styles.css`.

---

### 🧱 Herencia de templates

- Se usa `base.html` como plantilla base general, desde donde se extienden todas las vistas.
- Cada vista (`add.html`, `edit_select.html`, `list.html`, `detail.html`) hereda de `base.html` y carga solo su contenido dinámico.
- Bloques como `{% block content %}` y `{% block title %}` facilitan la sobreescritura local sin duplicar HTML.

---

### 📐 Convenciones y arquitectura

- **Separación de responsabilidades**:
  - Cada app (`clients`, `suppliers`) gestiona su lógica de modelos, formularios y vistas.
  - `core` contiene vistas globales y la home del sistema.

- **Modelos reutilizables**:
  - `Entity` en `core.models` funciona como clase base para `Client` y `Supplier`.
  - Evita duplicación de campos como `name`, `email`, `address`, etc.

- **Nombres de rutas consistentes**:
  - Se usan `namespace:name` para cada app (ej. `clients:add`, `suppliers:list`).
  - URLs organizadas en `urls.py` propios y conectadas desde el enrutador global.

- **Estilo y diseño**:
  - Tailwind con clases utilitarias para control preciso de espaciado, tipografía, colores y distribución.
  - Uso de breakpoints (`md:`, `xl:`) para responsive design.
  - Ancho máximo del sistema limitado con `max-w-screen-lg` y centrado con `mx-auto`.

---

## ♻️ Diseño del sistema: reutilización y buenas prácticas

Para mantener el sistema limpio, modular y fácilmente escalable, se implementaron las siguientes prácticas:

### 📦 Reutilización de componentes

- **Componentes visuales compartidos**:
  - Carpeta `ui/templates/components/` para formularios (`form.html`), tarjetas (`list_card.html`), títulos de páginas (`page.html`), etc.
  - Utilizados con `{% include %}` y `with` para pasar contexto dinámico.

- **Partial views**:
  - `partials/navbar.html` y `partials/footer.html` definen el layout superior e inferior, incluidos en `base.html`.

- **Estilo centralizado**:
  - `custom.css` sobrescribe estilos de DaisyUI para mantener coherencia (inputs blancos, bordes visibles, etc.).
  - Archivo generado por Tailwind en `ui/static/css/dist/styles.css`.

---

### 🧱 Herencia de templates

- Se usa `base.html` como plantilla base general, desde donde se extienden todas las vistas.
- Cada vista (`add.html`, `edit_select.html`, `list.html`, `detail.html`) hereda de `base.html` y carga solo su contenido dinámico.
- Bloques como `{% block content %}` y `{% block title %}` facilitan la sobreescritura local sin duplicar HTML.

---

### 📐 Convenciones y arquitectura

- **Separación de responsabilidades**:
  - Cada app (`clients`, `suppliers`) gestiona su lógica de modelos, formularios y vistas.
  - `core` contiene vistas globales y la home del sistema.

- **Modelos reutilizables**:
  - `Entity` en `core.models` funciona como clase base para `Client` y `Supplier`.
  - Evita duplicación de campos como `name`, `email`, `address`, etc.

- **Nombres de rutas consistentes**:
  - Se usan `namespace:name` para cada app (ej. `clients:add`, `suppliers:list`).
  - URLs organizadas en `urls.py` propios y conectadas desde el enrutador global.

- **Estilo y diseño**:
  - Tailwind con clases utilitarias para control preciso de espaciado, tipografía, colores y distribución.
  - Uso de breakpoints (`md:`, `xl:`) para responsive design.
  - Ancho máximo del sistema limitado con `max-w-screen-lg` y centrado con `mx-auto`.

---


## 📄 Licencia

Este proyecto se entrega exclusivamente con fines académicos y no posee licencia de uso comercial.
