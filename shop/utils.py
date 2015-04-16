from decimal import Decimal

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from shop.models import OrderItem, ProdCategory, ProdVariation


def add_to_cart(cart, new_item):
    """
    Check if item is already in cart and update quantity or add new item
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

def calculate_cart_shipping(locale, item_total):
    """
    Calculate shipping cost based on cart total & customer's location
    """
    DOMESTIC_SHIP_NATIONS = ['AS', 'CA', 'FM', 'GU', 'MH', 'MP', 'PR', 'PW', 'US', 'VI']
    DOMESTIC_SHIP_PRICES = ((100, 9), (75, 7), (50, 6), (25, 5), (0, 3)) 
    INTL_SHIP_PRICES = ((100, 12), (75, 10), (50, 9), (25, 8), (0, 5))
    if not locale:
        return 0
    else:
        if locale in DOMESTIC_SHIP_NATIONS:
            prices = DOMESTIC_SHIP_PRICES
        else:
            prices = INTL_SHIP_PRICES
        for price in prices:
            if item_total > price[0]:
                return price[1]

def create_order(form_list, form_dict):
    """
    Create Order object from OrderWizard form data
    """
    order = form_dict['shipping'].save(commit=False)

    payment_data = form_dict['payment'].data
    item_total = Decimal(payment_data['payment-item_total'])
    shipping_total = Decimal(payment_data['payment-shipping_total'])
    order.item_total = item_total
    order.shipping_total = shipping_total
    order.order_total = item_total + shipping_total
    order.save()
    return order

def create_order_items(cart, order):
    """
    Create & save OrderItems from items in session cart
    """
    for item in cart['items']:
        variation = ProdVariation.objects.get(sku=item['sku'])
        order_item = OrderItem(
            order=order,
            price=variation.price,
            product=variation.product,
            quantity=item['quantity'],
            size=variation.size,
            sku=variation.sku,
            width=variation.width
        )
        order_item.save()

def generate_crumbs(path):
    """
    Create navigation crumbs based on the URL path or current product view.
    If generating from path, checks that each level in the URL path exists or
    returns 404
    """
    crumbs = []

    if path:
        categories = path.rstrip('/').split('/')
        for slug in categories:
            if not crumbs:
                parent = None
            else:
                parent = crumbs[-1]['category']
            category = get_object_or_404(ProdCategory, slug=slug, parent=parent)
            crumbs.append({'category': category, 'path': category.path()})

    return crumbs

def send_order_confirmation(order):
    """
    Send order confirmation email to customer & email copy to shop to let us 
    know there's a new order
    """
    html_message = render_to_string('email/order_thankyou.html', {'order': order})
    text_message = render_to_string('email/order_thankyou_textonly.html', {'order': order})
    send_mail(
        subject='Uptown Hound Boutique order confirmation',
        message=text_message,
        from_email='Uptown Hound <orders@uptownhoundboutique.com>',
        recipient_list=[order.customer_email], 
        fail_silently=True,
        html_message=html_message
    )
    send_mail(
        subject='Uptown Hound Boutique order confirmation',
        message=text_message,
        from_email='Uptown Hound <orders@uptownhoundboutique.com>',
        recipient_list=['orders@uptownhoundboutique.com'], 
        fail_silently=True,
        html_message=html_message
    )

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
    item_count, item_total = 0, 0

    for item in cart['items']:
        item_count += item['quantity']
        item_total += item['line_total']
    
    shipping = calculate_cart_shipping(cart.get('locale', None), item_total)

    cart['item_count'] = item_count
    cart['item_total'] = item_total
    cart['shipping'] = shipping
    cart['order_total'] = item_total + shipping
    
    return cart