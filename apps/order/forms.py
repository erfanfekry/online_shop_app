from django import forms
from .models import *

class MakeOrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'postal_code', 'province', 'city']