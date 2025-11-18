#!/usr/bin/env python
"""
Script para ejecutar tests del proyecto BLC ERP
Uso: python run_tests.py [opción]

Opciones:
  all              - Ejecutar todos los tests
  models           - Ejecutar solo tests de modelos
  forms            - Ejecutar solo tests de formularios
  views            - Ejecutar solo tests de vistas
  core             - Ejecutar tests de core
  clients          - Ejecutar tests de clients
  suppliers        - Ejecutar tests de suppliers
  coverage         - Ejecutar con coverage
  verbose          - Ejecutar con verbosity=2
  help             - Mostrar esta ayuda
"""

import os
import sys
import subprocess
from pathlib import Path

# Cambiar a directorio src
BASE_DIR = Path(__file__).resolve().parent / "src"
os.chdir(BASE_DIR)

def run_command(cmd):
    """Ejecutar comando y retornar código de salida"""
    print(f"\n{'='*70}")
    print(f"Ejecutando: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    return subprocess.call(cmd)

def run_all_tests():
    """Ejecutar todos los tests"""
    return run_command([sys.executable, "manage.py", "test", "--verbosity=2"])

def run_model_tests():
    """Ejecutar solo tests de modelos"""
    tests = [
        "core.tests.EntityModelTests",
        "clients.tests.ClientModelTests",
        "suppliers.tests.SupplierModelTests",
    ]
    return run_command([sys.executable, "manage.py", "test"] + tests + ["--verbosity=2"])

def run_form_tests():
    """Ejecutar solo tests de formularios"""
    tests = [
        "clients.tests.ClientFormTests",
        "suppliers.tests.SupplierFormTests",
    ]
    return run_command([sys.executable, "manage.py", "test"] + tests + ["--verbosity=2"])

def run_view_tests():
    """Ejecutar solo tests de vistas"""
    tests = [
        "clients.tests.ClientViewsTests",
        "suppliers.tests.SupplierViewsTests",
        "core.tests.CoreViewsTests",
    ]
    return run_command([sys.executable, "manage.py", "test"] + tests + ["--verbosity=2"])

def run_app_tests(app_name):
    """Ejecutar tests de una aplicación específica"""
    return run_command([sys.executable, "manage.py", "test", app_name, "--verbosity=2"])

def run_coverage():
    """Ejecutar tests con coverage"""
    try:
        return run_command(["coverage", "run", "--source=.", "manage.py", "test"])
    except FileNotFoundError:
        print("ERROR: coverage no está instalado")
        print("Instálalo con: pip install coverage")
        return 1

def show_coverage_report():
    """Mostrar reporte de coverage"""
    try:
        run_command(["coverage", "report"])
        run_command(["coverage", "html"])
        print("\n✓ Reporte HTML generado en htmlcov/index.html")
    except FileNotFoundError:
        pass

def show_help():
    """Mostrar ayuda"""
    print(__doc__)

def main():
    """Función principal"""
    args = sys.argv[1:]
    
    if not args or args[0] == "help":
        show_help()
        return 0
    
    option = args[0].lower()
    
    if option == "all":
        return run_all_tests()
    elif option == "models":
        return run_model_tests()
    elif option == "forms":
        return run_form_tests()
    elif option == "views":
        return run_view_tests()
    elif option == "core":
        return run_app_tests("core")
    elif option == "clients":
        return run_app_tests("clients")
    elif option == "suppliers":
        return run_app_tests("suppliers")
    elif option == "coverage":
        exit_code = run_coverage()
        if exit_code == 0:
            show_coverage_report()
        return exit_code
    elif option == "verbose":
        return run_all_tests()
    else:
        print(f"Opción desconocida: {option}")
        print("Usa 'help' para ver las opciones disponibles")
        return 1

if __name__ == "__main__":
    sys.exit(main())
