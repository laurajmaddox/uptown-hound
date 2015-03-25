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
    cart['order_total'] = item_total + shipping
    return cart