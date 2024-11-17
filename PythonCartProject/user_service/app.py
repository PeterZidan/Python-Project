from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import os
from user_service.models import create_user, get_user_by_username
from .auth import authenticate_user
import uuid
import requests

app = Flask(__name__)

# Load the JWT secret key from environment variables
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')  # Use a default for dev
jwt = JWTManager(app)

# JWT token expiration time for 1 hour
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Checking if the username already exists
    if get_user_by_username(username):
        return jsonify({"msg": "User already exists"}), 400

    # Creating a new user
    user_id = str(uuid.uuid4())  # Generating a unique user ID
    create_user(user_id, username, password)

    return jsonify({"msg": "User registered successfully"}), 201

# Endpoint for user login it generates a JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token)

# Run the Flask app on port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)
