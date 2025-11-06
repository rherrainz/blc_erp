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

## 🔍 Acceso

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

## 📄 Licencia

Este proyecto se entrega exclusivamente con fines académicos y no posee licencia de uso comercial.
