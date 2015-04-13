from collections import OrderedDict

from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, render_to_response, get_object_or_404

from shop.forms import AddProductForm, CartCountryForm, CartItemFormset, OrderPaymentForm, OrderShippingForm
from shop.models import OrderItem, Product, ProdCategory, ProdVariation
from shop.utils import add_to_cart, create_order, create_order_items, send_order_confirmation, update_cart_items, update_totals

def cart(request):
    """
    View for customer's cart/shopping bag
    """
    cart = request.session.get('cart', {'items': []})

    if request.method == 'POST' and 'country' in request.POST:
        cart['locale'] = request.POST['country']
        cart = update_totals(cart)
        request.session['cart'] = cart

    if request.method == 'POST' and 'country' not in request.POST:
        formset = CartItemFormset(request.POST, initial=cart['items'])
        if formset.is_valid():
            cart = update_cart_items(cart, formset.cleaned_data)
            cart = update_totals(cart)
            request.session['cart'] = cart
            formset = CartItemFormset(initial=cart['items'])
    else:
        formset = CartItemFormset(initial=cart['items'])

    country_form = CartCountryForm

    return render(request, 'cart.html', {
        'formset': formset, 'country_form': country_form
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
            'shipping': cart['shipping'],
            'order_total': cart['order_total']
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


def confirm_order(request, invoice_number):
    """
    Thank you page after successful order payment processing
    """
    return render(request, 'checkout/confirm_order.html', {'invoice_number': invoice_number})


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
        ('shipping', OrderShippingForm),
        ('payment', OrderPaymentForm),
    ]

    def get_form_initial(self, step):
        cart = self.request.session['cart']
        initial_dict = {
            'payment': {
                'item_total': cart['item_total'],
                'shipping_total': cart['shipping'],
            }
        }
        return initial_dict.get(step, {})

    def get_form_kwargs(self, step):
        step_kwargs = {
            'payment': {
                'cart': self.request.session['cart']
            }
        }
        return step_kwargs.get(step, {})

    def get_template_names(self):
        TEMPLATES = {
            'payment': 'checkout/payment.html',
            'shipping': 'checkout/shipping.html',
        }
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(OrderWizard, self).get_context_data(form=form, **kwargs)
        BUTTON_TEXT = {
            'shipping': 'Continue to payment',
            'payment': 'Place order',
        }
        context.update({
            'button_text': BUTTON_TEXT[self.steps.current],
            'shipping_info': self.get_cleaned_data_for_step('shipping'),
        })
        return context

    def render_done(self, form, **kwargs):
        """
        Overriding render_done to skip form re-validation to avoid processing
        the Stripe payment a second time in the clean() method for OrderPaymentForm
        """
        final_forms = OrderedDict()

        for form_key in self.get_form_list():
            form_obj = self.get_form(step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key))
            final_forms[form_key] = form_obj

        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def done(self, form_list, form_dict, **kwargs):
        order = create_order(form_list, form_dict)
        create_order_items(self.request.session['cart'], order)

        del self.request.session['cart']

        send_order_confirmation(order)

        return HttpResponseRedirect('thankyou/' + str(order.id) + '/')
