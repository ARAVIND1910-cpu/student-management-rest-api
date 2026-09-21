import os

# Keep tests isolated from the default local database.
os.environ["DATABASE_URL"] = "sqlite:///./test_students.db"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def test_list_students():
    with TestClient(app) as client:
        response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_student():
    payload = {
        "name": "Meera Nair",
        "email": "meera.nair@example.com",
        "department": "Civil Engineering",
        "year": 2,
        "cgpa": 8.2,
    }
    with TestClient(app) as client:
        response = client.post("/students", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]


def test_get_missing_student():
    with TestClient(app) as client:
        response = client.get("/students/999999")
    assert response.status_code == 404


def test_invalid_student():
    payload = {
        "name": "A",
        "email": "not-an-email",
        "department": "CS",
        "year": 8,
        "cgpa": 11,
    }
    with TestClient(app) as client:
        response = client.post("/students", json=payload)
    assert response.status_code == 422
