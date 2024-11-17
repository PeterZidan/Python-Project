import unittest
from unittest.mock import patch
from cart_service.app import app  # Import the Flask app
from flask_jwt_extended import create_access_token
from cart_service.models import add_item_to_cart, get_cart_by_user_id

class CartServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Push the app context to ensure Flask-related functionality works
        self.app_context = app.app_context()
        self.app_context.push()  # Push the app context before using JWT functionality
        
        # Create a mock user for testing
        self.mock_user_id = "1234"
        self.mock_token = create_access_token(identity=self.mock_user_id)  # Generate JWT token for the mock user

        # Set up the Flask testing client
        self.client = app.test_client()

    @patch('cart_service.app.get_cart_by_user_id')  # Mock the method used in app.py
    def test_get_cart(self, mock_get_cart):
        # Define the mock response with 'user_id' to match the expected structure
        mock_cart = {
            'user_id': self.mock_user_id,  # Add 'user_id' in the mock response
            'items': [
                {'item_name': 'Laptop', 'quantity': 1},
                {'item_name': 'Laptop', 'quantity': 1},
                {'item_name': 'Laptop', 'quantity': 1}
            ]
        }

        # Mock the get_cart_by_user_id method to return the mock cart
        mock_get_cart.return_value = mock_cart

        # Make the GET request to the /cart endpoint with the mock token
        response = self.client.get('/cart', headers={'Authorization': f'Bearer {self.mock_token}'})

        # Assert the response status and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_cart)

    @patch('cart_service.app.get_cart_by_user_id')  # Mock the method used in app.py
    def test_get_empty_cart(self, mock_get_cart):
        # Mock the get_cart_by_user_id method to return None (empty cart)
        mock_get_cart.return_value = None

        # Make the GET request to the /cart endpoint with the mock token
        response = self.client.get('/cart', headers={'Authorization': f'Bearer {self.mock_token}'})

        # Assert the response status code is 404 as no cart exists for the user
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'msg': 'Cart is empty'})

    @patch('cart_service.app.add_item_to_cart')  # Mock the method used in app.py
    def test_add_item_to_cart(self, mock_add_item):
        # Define the mock data
        item_data = {
            'item_name': 'Laptop',
            'quantity': 1
        }

        # Mock the response from add_item_to_cart (no actual return value needed)
        mock_add_item.return_value = None  # You can set a mock return value if needed

        # Make the POST request to the /cart endpoint with the mock token
        response = self.client.post('/cart', json=item_data, headers={'Authorization': f'Bearer {self.mock_token}'})

        # Assert that the response indicates the item was added to the cart
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'msg': 'Item added to cart'})

        # Ensure add_item_to_cart was called with the correct arguments
        mock_add_item.assert_called_once_with(self.mock_user_id, item_data['item_name'], item_data['quantity'])


if __name__ == '__main__':
    unittest.main()
