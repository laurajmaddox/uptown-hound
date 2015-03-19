from django.shortcuts import render, get_object_or_404

from shop.models import Product, ProdCategory


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
    return render(request, 'product.html', { 'product': product })
