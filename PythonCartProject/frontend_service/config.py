import os

USER_SERVICE_URL = 'http://127.0.0.1:5001/'
CART_SERVICE_URL = 'http://127.0.0.1:5002/'

# Ensure secret is loaded from environment variables
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')  # Change it for production
