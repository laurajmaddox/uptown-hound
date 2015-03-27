from django import forms
from django.forms.formsets import formset_factory

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
                ' (' + variation.width.upper() + ' wide) - $' + str(variation.price))
            for variation in product.variations.all()
        ], widget=forms.Select(attrs={'class': 'form-control'}))


class CartItemForm(forms.Form):
    """
    Form to update a single item line in the cart
    """
    quantity = forms.IntegerField(
            localize=False,
            min_value=0,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
    sku = forms.CharField(widget=forms.HiddenInput)

CartItemFormset = formset_factory(CartItemForm, extra=0)


class OrderPaymentForm(forms.Form):
    """
    Form to collect billing info to be passed to Stripe
    """
    cc_name = forms.CharField(max_length=128, required=True)
    postal = forms.CharField(max_length=32, required=True)
    stripe_token = forms.CharField(max_length=128, required=True)


class OrderShippingForm(forms.ModelForm):
    """
    Form for shipping & contact infrom from Order model
    """
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_street', 'customer_city',
            'customer_state', 'customer_nation', 'customer_postal',
            'customer_email', 'customer_phone', 'customer_comments',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_street': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_city': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_state': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_nation': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_comments': forms.Textarea(attrs={'class': 'form-control'}),
        }

