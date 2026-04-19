from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    created_at = forms.DateTimeField(disabled=True, required=False)

    class Meta:
        model = Order
        exclude = ['user']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data