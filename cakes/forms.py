from django import forms
from .models import Cake, Category


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Cake name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Cake description'}),
        }
        labels = {
            'name': 'Cake Name',
        }
        help_texts = {
            'name': 'Enter the name of the cake',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long.')
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'