# CI/CD - Integración Continua para Testing

## GitHub Actions

Crea un archivo `.github/workflows/tests.yml`:

```yaml
name: Django Tests

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r src/requirements.txt
        pip install -r requirements-testing.txt
    
    - name: Run tests
      run: |
        cd src
        python manage.py test --verbosity=2
    
    - name: Generate coverage report
      run: |
        cd src
        coverage run --source='.' manage.py test
        coverage report
        coverage xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

## GitLab CI

Crea un archivo `.gitlab-ci.yml`:

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r src/requirements.txt
    - pip install -r requirements-testing.txt
  script:
    - cd src
    - python manage.py test --verbosity=2
    - coverage run --source='.' manage.py test
    - coverage report
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

## Jenkins

Archivo `Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                script {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r src/requirements.txt
                        pip install -r requirements-testing.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        cd src
                        python manage.py test --verbosity=2
                    '''
                }
            }
        }
        
        stage('Coverage') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        cd src
                        coverage run --source='.' manage.py test
                        coverage report
                        coverage html
                    '''
                }
            }
        }
    }
    
    post {
        always {
            junit 'test-results/*.xml'
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
    }
}
```

## CircleCI

Archivo `.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    
    steps:
      - checkout
      
      - restore_cache:
          keys:
            - v1-dependencies-{{ checksum "src/requirements.txt" }}
            - v1-dependencies-
      
      - run:
          name: Install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r src/requirements.txt
            pip install -r requirements-testing.txt
      
      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum "src/requirements.txt" }}
      
      - run:
          name: Run tests
          command: |
            . venv/bin/activate
            cd src
            python manage.py test --verbosity=2
      
      - run:
          name: Generate coverage report
          command: |
            . venv/bin/activate
            cd src
            coverage run --source='.' manage.py test
            coverage report
      
      - store_artifacts:
          path: htmlcov
          destination: coverage

workflows:
  test:
    jobs:
      - test
```

## Pre-commit Hook

Crea un archivo `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Script para ejecutar tests antes de hacer commit

echo "Ejecutando tests..."

cd src
python manage.py test --failfast

if [ $? -ne 0 ]; then
    echo "❌ Tests fallaron. Commit cancelado."
    exit 1
fi

echo "✅ Tests exitosos. Continuando con el commit."
exit 0
```

Hazlo ejecutable:
```bash
chmod +x .git/hooks/pre-commit
```

## Makefile para Desarrollo

Crea un archivo `Makefile`:

```makefile
.PHONY: test coverage test-models test-forms test-views clean help

help:
	@echo "Comandos disponibles:"
	@echo "  make test           - Ejecutar todos los tests"
	@echo "  make test-models    - Tests solo de modelos"
	@echo "  make test-forms     - Tests solo de formularios"
	@echo "  make test-views     - Tests solo de vistas"
	@echo "  make coverage       - Ejecutar con cobertura"
	@echo "  make clean          - Limpiar archivos generados"

test:
	cd src && python manage.py test --verbosity=2

test-models:
	cd src && python manage.py test \
		core.tests.EntityModelTests \
		clients.tests.ClientModelTests \
		suppliers.tests.SupplierModelTests \
		--verbosity=2

test-forms:
	cd src && python manage.py test \
		clients.tests.ClientFormTests \
		suppliers.tests.SupplierFormTests \
		--verbosity=2

test-views:
	cd src && python manage.py test \
		clients.tests.ClientViewsTests \
		suppliers.tests.SupplierViewsTests \
		core.tests.CoreViewsTests \
		--verbosity=2

coverage:
	cd src && coverage run --source='.' manage.py test
	cd src && coverage report
	cd src && coverage html
	@echo "Reporte en: htmlcov/index.html"

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov
	rm -f .coverage
```

Uso:
```bash
make test
make coverage
make test-models
```

## Scripts de Testing

### `test-watch.sh` - Ejecutar tests automáticamente

```bash
#!/bin/bash
# test-watch.sh - Ejecuta tests cada vez que hay cambios

if ! command -v watchmedo &> /dev/null; then
    pip install watchdog[watchmedo]
fi

watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='cd src && clear && python manage.py test --verbosity=2' \
    .
```

Uso:
```bash
chmod +x test-watch.sh
./test-watch.sh
```

### `test-parallel.sh` - Tests en paralelo

```bash
#!/bin/bash
# test-parallel.sh - Ejecuta tests en paralelo

pip install pytest-xdist

cd src
pytest -n auto
```

## Configuración de IDEs

### VSCode - `.vscode/settings.json`

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "src"
    ],
    "python.testing.unittestEnabled": false,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--django-settings-module=blc_erp.settings"
    ]
}
```

### PyCharm

1. File → Settings → Tools → Python Integrated Tools
2. Default test runner → pytest
3. Django support → ✓ Enable Django support
4. Django project root: `/path/to/src`
5. Settings module: `blc_erp.settings`

## Cobertura Mínima

Configura un threshold mínimo en `src/setup.cfg`:

```ini
[coverage:run]
source = .
omit =
    */migrations/*
    */tests/*
    manage.py
    */wsgi.py
    */asgi.py

[coverage:report]
fail_under = 80
precision = 2
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

## Reporting

### Generar reportes HTML

```bash
cd src
coverage html
# Abre htmlcov/index.html
```

### Badge de cobertura

En `README.md`:

```markdown
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)
```

## Monitoreo de Performance

```bash
cd src
python manage.py test --verbosity=2 --debug-sql
```

Esto mostrará todas las queries SQL ejecutadas durante los tests.

## Troubleshooting

### Tests lentos
```bash
cd src
python manage.py test --parallel
```

### Tests fallidos en CI pero no localmente
```bash
# Usa la BD en memoria exacta de tests
python manage.py test --keepdb
```

### Debugging de tests
```bash
python -m pdb manage.py test
python manage.py test --debug-mode
```

## Recursos

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [GitHub Actions Python Testing](https://github.com/actions/setup-python)
