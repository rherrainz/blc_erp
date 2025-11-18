# Guía de uso (desarrollador & usuario)

Requisitos

- Python 3.11+
- Node/npm (para compilar estilos Tailwind)
- `venv` recomendado

Ejecución local (rápida)

1. Crear y activar entorno:

```pwsh
python -m venv ../venv
.\..\venv\Scripts\Activate.ps1
```

2. Instalar dependencias

```pwsh
pip install -r requirements.txt
```

3. Migraciones y datos iniciales

```pwsh
cd src
python manage.py migrate
python manage.py createsuperuser
```

4. Compilar estilos (opcional para desarrollo de CSS)

```pwsh
cd ui/static_src
npm install
npm run dev
```

5. Ejecutar servidor

```pwsh
cd ..\..
python manage.py runserver
```

Comandos útiles

- Ejecutar tests con Django: `python manage.py test`
- Ejecutar tests con pytest: `pytest -q` (desde `src` o raíz según `pytest.ini`)
- Ejemplo de dump/restore: `python manage.py dumpdata > data.json` / `python manage.py loaddata data.json`

Estructura de carpetas relevante

- `src/blc_erp/`  : configuración del proyecto
- `src/clients/`  : lógica de clientes
- `src/suppliers/` : lógica de proveedores
- `src/ui/templates/` : plantillas y componentes
