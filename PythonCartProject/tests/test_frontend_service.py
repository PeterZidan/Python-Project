import unittest
from unittest.mock import patch
from frontend_service.app import app


class TestFrontendService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("requests.post")
    def test_register(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"msg": "User registered successfully"}

        response = self.client.post(
            "/register", json={"username": "test_user", "password": "password123"}
        )
        self.assertEqual(response.status_code, 201)

    @patch("requests.post")
    def test_login(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test_token"}

        response = self.client.post(
            "/login", json={"username": "test_user", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)

    @patch("requests.post")
    def test_add_to_cart(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"msg": "Item added to cart"}

        response = self.client.post(
            "/cart",
            json={"item_name": "Test Item", "quantity": 2},
            headers={"Authorization": "Bearer test_token"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("requests.get")
    def test_get_cart(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "user_id": "test_user_id",
            "items": [{"item_name": "Test Item", "quantity": 2}],
        }

        response = self.client.get("/cart", headers={"Authorization": "Bearer test_token"})
        self.assertEqual(response.status_code, 200)
