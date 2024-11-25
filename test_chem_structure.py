from fastapi.testclient import TestClient
from main import app
import re

client = TestClient(app)

UUID4_PATTERN = re.compile(
    '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
)

def is_valid_uuid4(uuid_string):
    return bool(UUID4_PATTERN.match(uuid_string.lower()))


def test_get_smile():
    response = client.get("/smiles/0002")
    assert response.status_code == 200
    assert response.json() == {"component": "c1ccccc1", "id": "0002"}


def test_get_smile_2():
    response = client.get("/smiles/0005")
    assert response.status_code == 404
    assert response.json() == {"msg": "Not found"}


def test_get_search_for_smile():
    response = client.get("/smiles/search/?substructure=CC(=O)O")
    assert response.status_code == 200
    assert response.json() == ["CC(=O)O", "CC(=O)Oc1ccccc1C(=O)O"]


def test_create_smile():
    new_smile = {
        "component": "CCC(=O)O",
    }
    response = client.post("/smiles/", json=new_smile)
    assert response.status_code == 200
    assert response.json()["component"] == "CCC(=O)O"
    assert is_valid_uuid4(response.json()["id"])

def test_update_smile():
    new_smile = {
        "component": "CCC(=O)O",
        "id": "a25bb5ca-0afe-4942-9dba-6a1a4471865c"
    }
    response = client.put("/smiles/0001", json=new_smile)
    assert response.status_code == 200
    assert response.json() == {"component": "CCC(=O)O", "id": "0001"}


def test_delete_smile():
    response = client.delete("/smiles/0003")
    assert response.status_code == 200
    assert response.json() == {"component": "CC(=O)O", "id": "0003"}
