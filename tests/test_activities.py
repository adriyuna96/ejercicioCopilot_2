def test_get_activities(client):
    # Arrange
    # (No setup needed; data from app default state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    response_check = client.get("/activities")
    assert email in response_check.json()[activity_name]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_not_found_activity(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "foo@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participant?email={email_to_remove}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email_to_remove} from {activity_name}"

    response_check = client.get("/activities")
    assert email_to_remove not in response_check.json()[activity_name]["participants"]


def test_delete_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "notfound@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participant?email={email_to_remove}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
