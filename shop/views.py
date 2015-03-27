from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from shop.forms import AddProductForm, CartItemFormset, OrderPaymentForm, OrderShippingForm
from shop.models import Product, ProdCategory, ProdVariation
from shop.utils import add_to_cart, update_cart_items, update_totals

def cart(request):
    """
    View for customer's cart/shopping bag
    """
    cart = request.session.get('cart', {'items': []})

    if request.method == 'POST':
        formset = CartItemFormset(request.POST, initial=cart['items'])
        if formset.is_valid():
            cart = update_cart_items(cart, formset.cleaned_data)
            cart = update_totals(cart)
            request.session['cart'] = cart
            formset = CartItemFormset(initial=cart['items'])
    else:
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

def checkout(request):
    """
    Order checkout process
    """
    form = OrderShippingForm()
    return render(request, 'checkout.html', {'form': form})

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
            cart = add_to_cart(cart, cart_item)
            request.session['cart'] = update_totals(cart)
    else:
        form = AddProductForm(product)

    return render(request, 'product.html', { 
        'form': form,
        'product': product,
        'variations': variations
    })


class OrderWizard(SessionWizardView):
    """
    Wizard for managing order checkout forms & flow
    """
    form_list = [
        ('payment', OrderPaymentForm),
        ('shipping', OrderShippingForm)
    ]

    def get_template_names(self):
        TEMPLATES = {
            'payment': 'checkout/payment.html',
            'shipping': 'checkout/shipping.html'
        }
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        return HttpResponseRedirect('/checkout/')