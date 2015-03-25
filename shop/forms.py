from django import forms


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