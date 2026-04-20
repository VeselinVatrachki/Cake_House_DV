from django import forms
from django.forms import inlineformset_factory

from cakes.models import Cake

from .models import Order, OrderLine


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('event_date', 'note')
        labels = {
            'event_date': 'Event / pickup date',
            'note': 'Special requests',
        }
        help_texts = {
            'note': 'Allergies, inscription text, delivery details…',
        }
        widgets = {
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes for the bakery'}),
        }


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('cake', 'quantity')
        # labels = {'cake': 'Cake', 'quantity': 'Qty'}
        widgets = {
            'cake': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cake'].queryset = Cake.objects.select_related('category').all()


OrderLineFormSet = inlineformset_factory(
    Order,
    OrderLine,
    form=OrderLineForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=False,
)

