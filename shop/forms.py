from django import forms


class AddProductForm(forms.Form):
    """
    Form to select a ProdVariation and add to cart
    """
    quantity = forms.IntegerField(initial=1, localize=False, min_value=1)

    def __init__(self, product, *args, **kwargs):
        """
        Dynamically generate variation dropdown choices for product
        """
        super(AddProductForm, self).__init__(*args, **kwargs)

        self.fields['variation'] = forms.ChoiceField([
            (variation.size, variation.size + ' x ' + variation.width + ' - $' + str(variation.price))
            for variation in product.variations.all()
        ])