from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity','address','email','phone','payment_method']

class Vendor_requestForm(forms.ModelForm):
    class Meta:
        model = Vendor_request
        fields = ['username', 'email', 'phone', 'address', 'bank_account', 'citizenship', 'pan_no']