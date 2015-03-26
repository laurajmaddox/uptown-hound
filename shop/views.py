from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from shop.forms import AddProductForm, CartItemFormset
from shop.models import Product, ProdCategory, ProdVariation
from shop.utils import update_totals

def cart(request):
    """
    View for customer's cart/shopping bag
    """
    cart = request.session.get('cart', {'items': []})
    formset = CartItemFormset(initial=cart['items'])
    return render(request, 'cart.html', {
        'cart': cart,
        'formset': formset
    })

def cart_remove(request):
    """
    View that handles GET or Ajax POST requests to remove items 
    from the session cart
    """
    if request.method == 'POST':
        sku = request.POST.get('id', '')
    else:
        sku = request.GET.get('id', '')

    cart = request.session.get('cart', {'items': []})
    cart['items'] = [item for item in cart['items'] if item['sku'] != sku]
    cart = update_totals(cart)
    request.session['cart'] = cart
    
    if request.is_ajax(): 
        return JsonResponse({
            'item_count': cart['item_count'],
            'item_total': cart['item_total'],
            'order_total': cart['order_total'],
            'shipping': cart['shipping']
        })

    return redirect('cart')

def category(request, cat_slugs):
    """
    View for category browsing page
    """
    cat_slugs, crumbs = cat_slugs.split('/'), []

    for i in range(len(cat_slugs)):
        if not crumbs:
            parent = None
        else:
            parent = crumbs[-1][0]
        category = get_object_or_404(ProdCategory, slug=cat_slugs[i], parent=parent)
        crumbs.append([category, '/'.join(cat_slugs[:i + 1])])

    return render(request, 'category.html', {
        'crumbs': crumbs,
    })

def index(request):
    """
    View for landing/home page
    """
    return render(request, 'index.html')

def product(request, product_slug):
    """
    View for product detail page
    """
    product = get_object_or_404(Product, slug=product_slug)
    variations = product.variations.all()

    if request.method == 'POST':
        form = AddProductForm(product, data=request.POST)
        if form.is_valid():
            sku = form.cleaned_data['variation']
            quantity = form.cleaned_data['quantity']
            variation = ProdVariation.objects.get(sku=sku)
            cart_item = {
                'image': product.main_img.image.url,
                'line_total': float(variation.price * quantity),
                'price': float(variation.price),
                'product': product.name,
                'quantity': quantity,
                'sku': sku,
                'url': product.slug,
                'size': variation.size
            }
            cart = request.session.get('cart', {'items': []})
            cart['items'].append(cart_item)
            request.session['cart'] = update_totals(cart)
    else:
        form = AddProductForm(product)

    return render(request, 'product.html', { 
        'form': form,
        'product': product,
        'variations': variations
    })
