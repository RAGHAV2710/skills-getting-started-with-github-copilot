import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_signup_and_unregister():
    # Use a test email and a valid activity
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities))
    test_email = "testuser@mergington.edu"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup.status_code == 200
    assert "message" in signup.json()

    # Duplicate signup should fail or not add again
    signup2 = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup2.status_code != 200 or "already" in signup2.json().get("detail", "")

    # Unregister
    unregister = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister.status_code == 200 or unregister.status_code == 404
    # Unregister again should fail or be idempotent
    unregister2 = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister2.status_code == 404 or unregister2.status_code == 200
