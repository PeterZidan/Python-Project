from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import os
from cart_service.models import add_item_to_cart, get_cart_by_user_id

app = Flask(__name__)

# Load the JWT secret key from environment variables
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')  # Use a default for dev
jwt = JWTManager(app)

# JWT token expiration time for 1 hour
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  

# Endpoint for adding an item to the cart it requires JWT token
@app.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    # Validating the requested data
    if not item_name or not quantity:
        return jsonify({"msg": "Item name and quantity are required"}), 400

    # Adding item to the cart
    add_item_to_cart(current_user_id, item_name, quantity)
    return jsonify({"msg": "Item added to cart"}), 200

# Endpoint to get the user's cart it requires JWT token
@app.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    current_user_id = get_jwt_identity()
    cart = get_cart_by_user_id(current_user_id)

    if not cart:
        return jsonify({"msg": "Cart is empty"}), 404

    return jsonify(cart), 200

# Run the Flask app on port 5002
if __name__ == '__main__':
    app.run(debug=True, port=5002)
