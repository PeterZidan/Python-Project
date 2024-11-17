from flask import Flask, jsonify, request
import requests
from frontend_service.config import USER_SERVICE_URL, CART_SERVICE_URL

app = Flask(__name__)

# Helper function to extract and validate token
def get_token_from_header():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return None
    return token.split(" ")[1]

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = requests.post(f'{USER_SERVICE_URL}/register', json=data)

    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify(response.json()), response.status_code

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = requests.post(f'{USER_SERVICE_URL}/login', json=data)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

# Endpoint for adding an item to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    token = get_token_from_header()
    
    if not token:
        return jsonify({"msg": "Missing or invalid token"}), 400
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{CART_SERVICE_URL}/cart', json=data, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

# Endpoint for retrieving the user's cart
@app.route('/cart', methods=['GET'])
def get_cart():
    token = get_token_from_header()
    
    if not token:
        return jsonify({"msg": "Missing or invalid token"}), 400

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{CART_SERVICE_URL}/cart', headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

# Run the Flask app on port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
