from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class OfferForm(forms.Form):
    code = forms.CharField()
