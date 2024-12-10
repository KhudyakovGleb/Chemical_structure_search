import re

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app.database import Base, get_db
from app.models.smile import Smile

SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

UUID4_PATTERN = re.compile(
    "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def is_valid_uuid4(uuid_string):
    return bool(UUID4_PATTERN.match(uuid_string.lower()))


def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def populate_test_data(db):
    smiles = [
        Smile(id="0001", component="CCO"),
        Smile(id="0002", component="c1ccccc1"),
        Smile(id="0003", component="CC(=O)O"),
        Smile(id="0004", component="CC(=O)Oc1ccccc1C(=O)O"),
    ]
    db.add_all(smiles)
    db.commit()


def test_get_smile():
    setup_database()
    with TestingSessionLocal() as db:
        populate_test_data(db)
    response = client.get("/smiles/0002")
    assert response.status_code == 200
    assert response.json() == {"component": "c1ccccc1", "id": "0002"}


def test_get_smile_2():
    setup_database()
    with TestingSessionLocal() as db:
        populate_test_data(db)
    response = client.get("/smiles/0005")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


def test_get_search_for_smile():
    setup_database()
    with TestingSessionLocal() as db:
        populate_test_data(db)
    response = client.get("/smiles/search/?substructure=CC(=O)O")
    assert response.status_code == 200
    assert response.json() == ["CC(=O)O", "CC(=O)Oc1ccccc1C(=O)O"]


def test_update_smile():
    setup_database()
    with TestingSessionLocal() as db:
        populate_test_data(db)
    new_smile = {"component": "CCC(=O)O", "id": "0001"}
    response = client.put("/smiles/0001", json=new_smile)
    assert response.status_code == 200
    assert response.json() == {"component": "CCC(=O)O", "id": "0001"}


def test_delete_smile():
    setup_database()
    with TestingSessionLocal() as db:
        populate_test_data(db)
    response = client.delete("/smiles/0003")
    assert response.status_code == 200
    assert response.json() == {"component": "CC(=O)O", "id": "0003"}
