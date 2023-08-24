from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class CouponApplyForm(forms.Form):
    code = forms.CharField()
