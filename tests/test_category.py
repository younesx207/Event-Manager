import json
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_categories(auth_user):
    response = client.get("/categories/", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200
    assert type(response.json()) is list

def test_get_categories_invalid_user(auth_user):
    response = client.get("/categories/", headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401

def test_create_category(auth_user):
    category_data = {"name": "Test Category ", "description": "Test Description "}
    response = client.post("/categories/", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Category "
    return response.json()["id"]

def test_create_category_invalid_user(auth_user):
    category_data = {"name": "Test Category", "description": "Test Description"}
    response = client.post("/categories/", json=category_data, headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401

# def test_create_category_duplicate_name(auth_user):
#     category_data = {"name": "Test Category ", "description": "Test Description"}
#     client.post("/categories/", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
#     response = client.post("/categories/", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
#     assert response.status_code == 422

def test_update_category(auth_user):
    category_data = {"name": "Updated Category", "description": "Updated Description"}
    category_id = test_create_category(auth_user)
    response = client.patch(f"/categories/{category_id}", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Category"

def test_update_category_not_found(auth_user):
    category_data = {"name": "Updated Category", "description": "Updated Description"}
    response = client.patch("/categories/nonexistent_id", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 404

def test_delete_category(auth_user):
    category_id = test_create_category(auth_user)
    response = client.delete(f"/categories/{category_id}", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 202
    assert response.json() == "Category deleted"


def test_delete_category_not_found(auth_user):
    response = client.delete("/categories/nonexistent_id", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 404