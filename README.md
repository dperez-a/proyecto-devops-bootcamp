# Proyecto DevOps Bootcamp - Aplicación Flask

Proyecto final del Bootcamp DevOps de Qualentum. Despliegue completo de una aplicación web Flask con API REST y base de datos PostgreSQL mediante contenedores Docker.

## Autor

Daniel Pérez

## Estructura del proyecto
```
proyecto-devops-bootcamp/
├── app/                        # Código de la aplicación Flask
│   ├── __init__.py             # Factory pattern (create_app)
│   ├── config.py               # Configuraciones por entorno
│   ├── models.py               # Modelo SQLAlchemy (Data)
│   └── routes.py               # Endpoints REST API
├── docker/
│   ├── Dockerfile              # Imagen de la aplicación
│   └── docker-compose.yml      # Entorno local (app + PostgreSQL)
├── tests/
│   ├── conftest.py             # Configuración de tests (SQLite en memoria)
│   └── test_routes.py          # Tests unitarios de los endpoints
├── docs/                       # Documentación y diagramas
├── requirements.txt            # Dependencias Python
├── pytest.ini                  # Configuración de pytest
├── setup.cfg                   # Configuración de flake8
├── manage.py                   # Script de inicialización de BD
├── run.py                      # Entry point de la aplicación
└── README.md                   # Este archivo
```

## Requisitos

- Docker Desktop instalado
- Python 3.11+
- Git

## Desarrollo local con Docker

Levantar el entorno (app + PostgreSQL):
```bash
cd docker
docker compose up -d --build
```

Verificar que la aplicación está funcionando:
```bash
curl http://localhost:5001/data
```

Parar el entorno:
```bash
docker compose down
```

## API REST

| Método | Endpoint     | Descripción                        |
|--------|--------------|------------------------------------|
| GET    | /data        | Obtener todos los datos            |
| POST   | /data        | Insertar un dato nuevo             |
| DELETE | /data/<id>   | Eliminar un dato por su ID         |

### Ejemplos de uso

Insertar un dato:
```bash
curl -X POST http://localhost:5001/data -H "Content-Type: application/json" -d '{"name": "ejemplo"}'
```

Obtener todos los datos:
```bash
curl http://localhost:5001/data
```

Eliminar un dato:
```bash
curl -X DELETE http://localhost:5001/data/1
```

## Tests

Los tests se ejecutan con SQLite en memoria, sin necesidad de Docker ni PostgreSQL.

Crear y activar el entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov
```

Ejecutar tests con reporte de cobertura:
```bash
python -m pytest --cov=app --cov-report=term-missing
```

Resultado actual: 9 tests, 98% de cobertura.

## Linting

Verificar el código con flake8:
```bash
pip install flake8
flake8
```

## Documentación

El documento de arquitectura detallado se encuentra en `docs/arquitectura/`.