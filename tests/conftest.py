import os
import pytest

# Esto se ejecuta ANTES de importar la app,
# así cuando create_app() lee DATABASE_URI ya tiene el SQLite
os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from app import create_app, db as _db
from app.models import Data


@pytest.fixture(scope="session")
def app():
    """Crea una instancia de la app Flask configurada para tests."""
    app = create_app("development")
    app.config["TESTING"] = True

    yield app


@pytest.fixture(scope="function", autouse=True)
def db(app):
    """Crea y elimina las tablas antes y después de cada test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """Cliente de pruebas de Flask para hacer peticiones HTTP."""
    return app.test_client()


@pytest.fixture()
def sample_data(db):
    """Inserta un dato de ejemplo en la base de datos."""
    dato = Data(name="Test User")
    db.session.add(dato)
    db.session.commit()
    return dato