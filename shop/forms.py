from django import forms
from django.conf import settings
from django.forms.formsets import formset_factory

import stripe
from django_countries import countries
from django_countries.widgets import CountrySelectWidget

from shop.models import Order


class AddProductForm(forms.Form):
    """
    Form to select a ProdVariation and add to cart
    """
    quantity = forms.IntegerField(initial=1, localize=False, min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, product, *args, **kwargs):
        """
        Dynamically generate variation dropdown choices for product
        """
        super(AddProductForm, self).__init__(*args, **kwargs)

        self.fields['variation'] = forms.ChoiceField([
            (variation.sku, variation.size.upper() + 
                ' (' + variation.width.upper() + ' wide) - $' + "{0:.2f}".format(variation.price))
            for variation in product.variations.all().order_by('sort_order')
        ], widget=forms.Select(attrs={'class': 'form-control'}))


class CartCountryForm(forms.Form):
    """
    Form to select country for cart shipping calculation
    """
    country = forms.ChoiceField(choices=countries, widget=forms.Select(attrs={'class': 'form-control'}))


class CartItemForm(forms.Form):
    """
    Form to update a single item line in the cart
    """
    quantity = forms.IntegerField(
            localize=False,
            min_value=0,
            widget=forms.NumberInput(attrs={'class': 'form-control js-quantity'})
        )
    sku = forms.CharField(widget=forms.HiddenInput)

CartItemFormset = formset_factory(CartItemForm, extra=0)


class OrderPaymentForm(forms.Form):
    """
    Form to collect billing info to be passed to Stripe
    """
    cc_name = forms.CharField(
        max_length=128, label='Name on Card', required=True,
        widget=forms.TextInput(attrs={'class': 'form-control gray-outline','autofocus': 'autofocus'})
    )
    postal = forms.CharField(
        max_length=32, label='Billing Zip/Postal Code', required=True,
        widget=forms.TextInput(attrs={'class': 'form-control gray-outline'})
    )
    item_total = forms.DecimalField(required=True, min_value=0, widget=forms.HiddenInput())
    shipping_total = forms.DecimalField(required=True, min_value=0, widget=forms.HiddenInput())
    stripe_token = forms.CharField(max_length=128, required=True)

    def __init__(self, cart, *args, **kwargs):
        """
        Extends init to accept session cart from get_form_kwargs
        """
        super(OrderPaymentForm, self).__init__(*args, **kwargs)
        self.cart = cart

    def clean(self):
        """
        The Stripe charge is created and processed in the form's clean() method
        before moving on to the form wizard's done() so the user is brought back
        to the payment form in case of card errors or a declined charge
        """
        cleaned_data = super(OrderPaymentForm, self).clean()

        stripe.api_key = settings.STRIPE_KEY
        token = self.cleaned_data['stripe_token']

        item_total = self.cleaned_data['item_total']
        shipping_total = self.cleaned_data['shipping_total']

        if self.is_valid():
            # Make sure hidden total inputs = values in session
            if item_total + shipping_total != self.cart['shipping'] + self.cart['item_total']:
                raise forms.ValidationError(
                    'Order total does not match cart total',
                    code='total_matching_order'
                )

            # Process payment with Stripe
            try:
                charge = stripe.Charge.create(
                    amount=int(item_total * 100) + int(shipping_total * 100),
                    currency="usd",
                    source=token,
                    description="Uptown Hound Boutique Order"
                )
            except stripe.CardError as e:
                err = e.json_body['error']
                raise forms.ValidationError(err['message'], code='stripe_error')
 

class OrderShippingForm(forms.ModelForm):
    """
    Form for shipping & contact info from Order model
    """
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_street', 'customer_city',
            'customer_state', 'customer_nation', 'customer_postal',
            'customer_email', 'customer_phone', 'customer_comments',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'customer_street': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_city': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_state': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_nation': CountrySelectWidget(
                attrs={'class': 'form-control'}, layout='{widget}'
            ),
            'customer_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_comments': forms.Textarea(attrs={'class': 'form-control'}),
        }


class OrderStatusForm(forms.Form):
    """
    For for customer to lookup order status by invoice number & postal code
    """
    invoice_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
