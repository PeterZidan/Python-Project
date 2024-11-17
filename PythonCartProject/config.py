import os

# Shared secret key for JWT authentication 
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')  # Use a default for dev

# Path to the shared file-based database
DB_PATH = 'db.json'  


USER_SERVICE_URL = 'http://127.0.0.1:5001/'  # URL of the User Service which is running on port 5001
CART_SERVICE_URL = 'http://127.0.0.1:5002/'  # URL of the Cart Service which is running on port 5002


DEBUG_MODE = True  # Set to False in production

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')  
