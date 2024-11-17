import json
import os

DB_PATH = 'db.json'

def init_db():
    """ Initializes the database if not already present """
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({'users': [], 'carts': []}, f)

def load_data():
    """ Loads the data from the JSON database file """
    init_db()  # Ensure DB is initialized
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    """ Saves data to the JSON database file """
    with open(DB_PATH, 'w') as f:
        json.dump(data, f)