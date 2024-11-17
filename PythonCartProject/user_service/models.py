import bcrypt
from shared.db import load_data, save_data

def create_user(user_id, username, password):
    db = load_data()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        'id': user_id,
        'username': username,
        'password': hashed_password  # Store the hashed password
    }
    db['users'].append(new_user)
    save_data(db)

def get_user_by_username(username):
    db = load_data()
    for user in db['users']:
        if user['username'] == username:
            return user
    return None