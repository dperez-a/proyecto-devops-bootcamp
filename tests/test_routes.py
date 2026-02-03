"""
Tests unitarios para los endpoints de la API REST.

Endpoints testeados:
    - POST   /data  → insertar datos (éxito + duplicado)
    - GET    /data  → obtener todos los datos (vacío + con datos)
    - DELETE /data/<id> → eliminar dato (éxito + no encontrado)
"""
import json


class TestGetData:
    """Tests para el endpoint GET /data."""

    def test_get_data_vacio(self, client):
        """GET /data retorna lista vacía cuando no hay datos."""
        response = client.get("/data")
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_data_con_datos(self, client, sample_data):
        """GET /data retorna los datos existentes."""
        response = client.get("/data")
        data = response.get_json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["name"] == "Test User"
        assert "id" in data[0]

    def test_get_data_multiples(self, client, db):
        """GET /data retorna todos los datos cuando hay varios."""
        from app.models import Data
        db.session.add_all([
            Data(name="Usuario 1"),
            Data(name="Usuario 2"),
            Data(name="Usuario 3"),
        ])
        db.session.commit()

        response = client.get("/data")
        data = response.get_json()
        assert response.status_code == 200
        assert len(data) == 3


class TestPostData:
    """Tests para el endpoint POST /data."""

    def test_post_data_exitoso(self, client):
        """POST /data crea un nuevo dato correctamente."""
        payload = json.dumps({"name": "Nuevo Usuario"})
        response = client.post(
            "/data",
            data=payload,
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.get_json()["message"] == "Data inserted successfully"

    def test_post_data_aparece_en_get(self, client):
        """El dato creado con POST aparece al hacer GET."""
        client.post(
            "/data",
            data=json.dumps({"name": "Verificacion"}),
            content_type="application/json"
        )
        response = client.get("/data")
        datos = response.get_json()
        nombres = [d["name"] for d in datos]
        assert "Verificacion" in nombres

    def test_post_data_duplicado(self, client, sample_data):
        """POST /data retorna 409 si el dato ya existe."""
        payload = json.dumps({"name": "Test User"})
        response = client.post(
            "/data",
            data=payload,
            content_type="application/json"
        )
        assert response.status_code == 409
        assert response.get_json()["message"] == "Data already exists"


class TestDeleteData:
    """Tests para el endpoint DELETE /data/<id>."""

    def test_delete_data_exitoso(self, client, sample_data):
        """DELETE /data/<id> elimina el dato correctamente."""
        dato_id = sample_data.id
        response = client.delete(f"/data/{dato_id}")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Data deleted successfully"

    def test_delete_data_no_existe_en_get(self, client, sample_data):
        """El dato eliminado ya no aparece en GET."""
        dato_id = sample_data.id
        client.delete(f"/data/{dato_id}")

        response = client.get("/data")
        datos = response.get_json()
        ids = [d["id"] for d in datos]
        assert dato_id not in ids

    def test_delete_data_no_encontrado(self, client):
        """DELETE /data/<id> retorna 404 si el dato no existe."""
        response = client.delete("/data/9999")
        assert response.status_code == 404
        assert response.get_json()["message"] == "Data not found"