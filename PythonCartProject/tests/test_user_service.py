import unittest
from unittest.mock import patch
from user_service.app import app

class TestUserService(unittest.TestCase):

    def setUp(self):
        # Set up the test client for Flask
        self.client = app.test_client()

    @patch("user_service.models.get_user_by_username")
    @patch("user_service.models.create_user")
    def test_register(self, mock_create_user, mock_get_user_by_username):
        # Case 1: User already exists
        mock_get_user_by_username.return_value = {"id": "existing_user_id"}  # Simulate that user already exists
        response = self.client.post(
            "/register", json={"username": "test_user", "password": "password123"}
        )
        # Assert that status code is 400 and the response message for user already exists
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"msg": "User already exists"})

        # Reset mocks for the next case
        mock_get_user_by_username.reset_mock()
        mock_create_user.reset_mock()


        
   
        
    @patch("user_service.auth.authenticate_user")
    def test_login(self, mock_authenticate_user):
        # Case 1: Invalid credentials
        mock_authenticate_user.return_value = None  # Authentication fails
        response = self.client.post(
            "/login", json={"username": "test_user", "password": "wrong_password"}
        )
        # Assert that status code is 401 and the response message for invalid credentials
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"msg": "Invalid username or password"})  # Correct error message

        # Case 2: Successful login
        mock_authenticate_user.return_value = {"id": "test_user_id"}  # Authentication succeeds
        response = self.client.post(
            "/login", json={"username": "test_user", "password": "password123"}
        )
        # Assert that status code is 200 (OK) and that we get an access token
        self.assertEqual(response.status_code, 200)
        # Expecting an access token, so we check for the presence of the 'access_token' key
        self.assertIn('access_token', response.json)
        self.assertIsInstance(response.json['access_token'], str)  # Access token should be a string

if __name__ == "__main__":
    unittest.main()
