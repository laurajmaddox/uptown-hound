def add_to_cart(cart, new_item):
    """
    Check if item already exists in cart
    """
    in_cart = False

    for item in cart['items']:
        if item['sku'] == new_item['sku']:
            item['quantity'] += new_item['quantity']
            in_cart = True
            break
    
    if not in_cart:
        cart['items'].append(new_item)

    return cart


def update_cart_items(cart, updated_items):
    """
    Replace items in cart with updated quantities
    """
    cart_items = cart['items']

    updates = {item['sku']: item['quantity'] for item in updated_items}

    for item in cart_items:
        sku = item['sku']
        quantity = updates[sku]
        item['quantity'] = quantity
        item['line_total'] = quantity * item['price']

    cart['items'] = [item for item in cart_items if item['quantity'] != 0]

    return cart

def update_totals(cart):
    """
    Calculate item, shippping & order toals for session cart
    """
    item_count, item_total, shipping = 0, 0, 0

    for item in cart['items']:
        item_count += item['quantity']
        item_total += item['line_total']
    
    cart['item_count'] = item_count
    cart['item_total'] = item_total
    cart['shipping'] = shipping
    
    return cart