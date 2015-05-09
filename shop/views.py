# ===============================================
# shop/views.py
# ===============================================

from collections import OrderedDict

from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import (
    redirect, render, get_object_or_404
)

import watson

from shop.models import Order, Product, ProdVariation
from shop.forms import (
    AddProductForm, CartCountryForm, CartItemFormset, OrderPaymentForm,
    OrderShippingForm, OrderStatusForm
)
from shop.utils import (
    add_to_cart, create_order, create_order_items, generate_crumbs,
    send_order_confirmation, update_cart_items, update_totals
)


def cart(request):
    """
    Customer's cart/shopping bag
    """
    cart = request.session.get('cart', {'items': []})

    # Handle form submit to update shipping calculation
    if request.method == 'POST' and 'country' in request.POST:
        form = CartCountryForm(request.POST)
        if form.is_valid():
            cart['locale'] = form.cleaned_data['country']

    # Handle form submit to update cart quantities
    if request.method == 'POST' and 'country' not in request.POST:
        formset = CartItemFormset(request.POST, initial=cart['items'])
        if formset.is_valid():
            cart = update_cart_items(cart, formset.cleaned_data)
            formset = CartItemFormset(initial=cart['items'])
    else:
        formset = CartItemFormset(initial=cart['items'])

    # Update cart totals & re-save in session
    request.session['cart'] = update_totals(cart)

    return render(request, 'cart.html', {
        'formset': formset, 'country_form': CartCountryForm
    })


def cart_remove(request):
    """
    Handle GET or Ajax POST requests to remove a cart item
    """
    if request.method == 'POST':
        sku = request.POST.get('id', '')
    else:
        sku = request.GET.get('id', '')

    cart = request.session.get('cart', {'items': []})
    cart['items'] = [item for item in cart['items'] if item['sku'] != sku]

    # Update totals & re-save after removing the item
    request.session['cart'] = update_totals(cart)

    if request.is_ajax():
        return JsonResponse({
            'item_count': cart['item_count'],
            'item_total': cart['item_total'],
            'shipping': cart['shipping'],
            'order_total': cart['order_total']
        })

    return redirect('cart')


def category(request, category_path):
    """
    Browse Products in a particular ProdCategory
    """
    crumbs = generate_crumbs(path=category_path)

    # Get the leaf in the category path
    category = crumbs[-1]['category']

    products = category.product_set.all().order_by('-date_added')

    return render(request, 'category.html', {
        'category': category,
        'crumbs': crumbs,
        'products': products,
    })


def confirm_order(request, invoice_number):
    """
    Thank you page after successfully processing payment for an Order
    """
    return render(request, 'checkout/confirm_order.html', {
        'invoice_number': invoice_number
    })


def order_status(request):
    """
    View for customer to look up status, contents, and tracking
    info for an Order
    """
    form, order = OrderStatusForm(request.POST or None), None

    if request.method == 'POST' and form.is_valid():
        try:
            order = Order.objects.get(
                pk=form.cleaned_data['invoice_number'],
                customer_postal=form.cleaned_data['postal_code']
            )
        except:
            form.add_error(None, 'We couldn\'t find that order.')

    return render(request, 'order_status.html', {
        'form': form,
        'order': order
    })


def product(request, product_slug):
    """
    Detail & purchase page for an individual Product
    """
    product = get_object_or_404(Product, slug=product_slug)
    cart_item = None

    form = AddProductForm(product, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
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
        request.session['cart'] = update_totals(add_to_cart(cart, cart_item))

    return render(request, 'product.html', {
        'crumbs': generate_crumbs(product.first_child().path()),
        'form': form,
        'cart_item': cart_item,
        'product': product,
        'variations': product.variations.all()
    })


def search(request):
    """
    Display Product search results
    """
    query = request.GET.get('term', '')
    results = watson.search(query)
    return render(request, 'search_results.html', {
        'results': results,
        'search_term': query
    })


class OrderWizard(SessionWizardView):
    """
    Wizard for managing checkout flow & forms for Order processing
    """
    form_list = [
        ('shipping', OrderShippingForm),
        ('payment', OrderPaymentForm),
    ]

    def get_form_initial(self, step):
        """
        Provide initial data for forms handled by the wizard
        """
        cart = self.request.session['cart']

        # Recalculate shipping based on form data before continuing to payment
        if step == 'payment':
            shipping_info = self.get_cleaned_data_for_step('shipping')
            cart['locale'] = shipping_info['customer_nation']
            cart = update_totals(cart)
            self.request.session['cart'] = cart

        initial_dict = {
            'payment': {
                'item_total': cart['item_total'],
                'shipping_total': cart['shipping'],
            }
        }
        return initial_dict.get(step, {})

    def get_form_kwargs(self, step):
        """
        Add keywords for __init__ method for forms handled by the wizard
        """
        step_kwargs = {
            'payment': {
                'cart': self.request.session['cart']
            }
        }
        return step_kwargs.get(step, {})

    def get_template_names(self):
        """
        Name the checkout step templates for the wizard
        """
        templates = {
            'payment': 'checkout/payment.html',
            'shipping': 'checkout/shipping.html',
        }
        return [templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        """
        Add context variables to checkout step templates
        """
        context = super(OrderWizard, self).get_context_data(
            form=form, **kwargs
        )

        button_text = {
            'shipping': 'Continue to payment',
            'payment': 'Place order',
        }
        context.update({
            'button_text': button_text[self.steps.current],
            'shipping_info': self.get_cleaned_data_for_step('shipping'),
        })
        return context

    def render_done(self, form, **kwargs):
        """
        Override render_done to skip form re-validation to avoid processing the
        Stripe payment a second time in the clean() method for OrderPaymentForm
        """
        final_forms = OrderedDict()

        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            final_forms[form_key] = form_obj

        done_response = self.done(
            final_forms.values(), form_dict=final_forms, **kwargs
        )
        self.storage.reset()
        return done_response

    def done(self, form_list, form_dict, **kwargs):
        """
        Create on Order & add OrderItems to the database, delete the session
        cart after successful payment processing; redirect to thank you page
        """
        order = create_order(form_list, form_dict)
        create_order_items(self.request.session['cart'], order)

        del self.request.session['cart']

        # Send confirmation email to customer
        send_order_confirmation(order)

        return HttpResponseRedirect('thankyou/' + str(order.id) + '/')
