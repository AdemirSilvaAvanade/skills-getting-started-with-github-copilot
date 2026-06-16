import pytest


class TestGetActivitiesEndpoint:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_success(self, client):
        """Test that GET /activities returns HTTP 200"""
        # Arrange
        expected_status = 200
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary"""
        # Arrange
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """Test that activities list contains expected activities"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_has_correct_structure(self, client):
        """Test that each activity has required fields"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activity = response.json()["Chess Club"]
        
        # Assert
        for field in required_fields:
            assert field in activity
        assert isinstance(activity["participants"], list)


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success_returns_200(self, client):
        """Test successful signup returns HTTP 200"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_signup_success_returns_confirmation_message(self, client):
        """Test that successful signup returns appropriate message"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds participant to the list"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response_before = client.get("/activities")
        initial_count = len(response_before.json()[activity_name]["participants"])
        
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        response_after = client.get("/activities")
        final_count = len(response_after.json()[activity_name]["participants"])
        
        # Assert
        assert final_count == initial_count + 1
        assert email in response_after.json()[activity_name]["participants"]

    def test_signup_with_duplicate_email_returns_400(self, client):
        """Test that duplicate signup returns HTTP 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_signup_with_duplicate_email_returns_error_message(self, client):
        """Test that duplicate signup returns appropriate error message"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns HTTP 404"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_for_nonexistent_activity_returns_error_message(self, client):
        """Test that signup for non-existent activity returns error message"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]


class TestUnregisterEndpoint:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success_returns_200(self, client):
        """Test successful unregister returns HTTP 200"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_unregister_success_returns_confirmation_message(self, client):
        """Test that successful unregister returns appropriate message"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister actually removes participant from the list"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response_before = client.get("/activities")
        initial_count = len(response_before.json()[activity_name]["participants"])
        
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        response_after = client.get("/activities")
        final_count = len(response_after.json()[activity_name]["participants"])
        
        # Assert
        assert final_count == initial_count - 1
        assert email not in response_after.json()[activity_name]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns HTTP 404"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_unregister_from_nonexistent_activity_returns_error_message(self, client):
        """Test that unregister from non-existent activity returns error message"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered_student_returns_400(self, client):
        """Test that unregistering a non-registered student returns HTTP 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_unregister_not_registered_student_returns_error_message(self, client):
        """Test that unregistering a non-registered student returns error message"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "not registered" in data["detail"]
