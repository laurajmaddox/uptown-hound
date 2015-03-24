from django.shortcuts import render, get_object_or_404

from shop.forms import AddProductForm
from shop.models import Product, ProdCategory


def cart(request):
    """
    View for customer's cart/shopping bag
    """
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})

def index(request):
    """
    View for landing/home page
    """
    return render(request, 'index.html')

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

def product(request, product_slug):
    """
    View for product detail page
    """
    product = get_object_or_404(Product, slug=product_slug)
    variations = product.variations.all()

    if request.method == 'POST':
        form = AddProductForm(product, data=request.POST)
        if form.is_valid():
            cart_item = {
                'product': product.name,
                'url': product.slug,
                'image': product.main_img.image.url,
                'variation': form.cleaned_data['variation'],
                'quantity': form.cleaned_data['quantity']
            }
            cart = request.session.get('cart', [])
            cart.append(cart_item)
            request.session['cart'] = cart
    else:
        form = AddProductForm(product)

    return render(request, 'product.html', { 
        'form': form,
        'product': product,
        'variations': variations
    })
