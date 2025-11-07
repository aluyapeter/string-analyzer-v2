import pytest
from fastapi.testclient import TestClient
from .main import app
from . import database
import json

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    database.db.clear()
    database.save_db()

    yield

    database.db.clear()
    database.save_db()


def test_create_string_success():
    payload = {"value": "racecar"}

    response = client.post("/strings", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["value"] == "racecar"
    assert data["properties"]["is_palindrome"] == True
    assert data["id"] in database.db

def test_create_string_conflict():
    client.post("/strings", json={"value": "hello"})

    response = client.post("/strings", json={"value": "hello"})

    assert response.status_code == 409
    assert response.json()["detail"] == "String already exists in the system"

def test_get_string_not_found():
    response = client.get("/strings/not-a-real-string")
    assert response.status_code == 404

def test_filtering_and_nl():
    client.post("/strings", json={"value": "racecar"})
    client.post("/strings", json={"value": "hello world"})
    client.post("/strings", json={"value": "madam"})

    response = client.get("/strings?is_palindrome=true&min_length=5")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["filters_applied"]["is_palindrome"] == True

    response_nl = client.get("/strings/filter-by-natural-language?query=palindromic strings")

    assert response_nl.status_code == 200
    data_nl = response_nl.json()
    assert data_nl["count"] == 2
    assert data_nl["interpreted_query"]["parsed_filters"]["is_palindrome"] == True