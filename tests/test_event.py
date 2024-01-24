from fastapi.testclient import TestClient
import pytest
from main import app
from uuid import uuid4
#from classes.schema_dto import CategoryNoID


client = TestClient(app)

@pytest.fixture
def test_event_valide():
    return {
        "title": "Test Event",
        "description": "test",
        "location": "test",
        "date_time": "2022-01-01T12:00:00",
        "category": "Test Category "
    }

@pytest.fixture
def test_event():
    return {
        "title": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "date_time": "2022-01-01T12:00:00",
        "category": "Test Category",
    }

# Test GET events
def test_get_events(auth_user):
    response = client.get("/events/", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200
    assert response.json() == []

# Test POST event
def test_create_event_valide_category(auth_user, test_event_valide):
    category_data = {"name": "Test Category ", "description": "Test Description "}
    reqponse1 = client.post("/categories/", json=category_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert reqponse1.status_code == 201
    response = client.post("/events/", json=test_event_valide, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Event"
    return response.json()["id"]

def test_create_event_unvalide_category(auth_user, test_event):
    response = client.post("/events/", json=test_event, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 404

def test_create_event_invalid_user(auth_user, test_event):
    response = client.post("/categories/", json=test_event, headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401

# Test GET event by ID
def test_get_event_by_id(auth_user):
    event_id = test_create_event_valide_category(auth_user, {
        "title": "Test Event",
        "description": "test",
        "location": "test",
        "date_time": "2022-01-01T12:00:00",
        "category": "Test Category "
    })
    # create_response = client.post("/events/", json=test_event, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    # assert create_response.status_code == 201
    response = client.get(f"/events/{event_id}", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200 


# Test GET events by category
def test_get_events_by_category(auth_user, test_event_valide):
    create_response = client.post("/events/", json=test_event_valide, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert create_response.status_code == 201
    response = client.get("/events/by_category/Test%20Category ", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200
    #assert response.json() == [test_event_valide]

# Test PATCH event
def test_update_event(auth_user):
    event_id = test_create_event_valide_category(auth_user, {
        "title": "Test Event",
        "description": "test",
        "location": "test",
        "date_time": "2022-01-01T12:00:00",
        "category": "Test Category "
    })
    update_data = {"title": "Updated Event", "description": "test updated", "location": "updated location", "date_time": "2022-01-01T12:00:00", "category": "Test Category "}
    response = client.patch(f"/events/{event_id}", json=update_data, headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 200

# Test DELETE event
def test_delete_event(auth_user):
    event_id = test_create_event_valide_category(auth_user, {
        "title": "Test Event",
        "description": "test",
        "location": "test",
        "date_time": "2022-01-01T12:00:00",
        "category": "Test Category "
    })
    response = client.delete(f"/events/{event_id}", headers= {'Authorization': f"Bearer {auth_user['access_token']}"})
    assert response.status_code == 202
    assert response.json() == "Event deleted"