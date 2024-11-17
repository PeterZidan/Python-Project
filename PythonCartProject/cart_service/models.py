from shared.db import load_data, save_data

def add_item_to_cart(user_id, item_name, quantity):
    db = load_data()
    cart = next((c for c in db['carts'] if c['user_id'] == user_id), None)
    if not cart:
        cart = {'user_id': user_id, 'items': []}
        db['carts'].append(cart)

    cart['items'].append({'item_name': item_name, 'quantity': quantity})
    save_data(db)

def get_cart_by_user_id(user_id):
    db = load_data()
    return next((c for c in db['carts'] if c['user_id'] == user_id), None)