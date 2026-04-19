from django import forms
from .models import Cake, Category


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ('name', 'slug', 'image', 'description', 'price',  'category', 'tags',)
        labels = {
            'name': 'Cake Name',
            'slug': 'URL Slug',
            'image': 'Photo',
            'description': 'Description',
            'price': 'Price',
            'category': 'Category',
            'tags': 'Tags',
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from the name.',
            'tags': 'Hold down "Control", or "Command" on a Mac, to select more than one tag.'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Cake name'}),
            'slug': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Auto generated'}),
            'description': forms.Textarea(attrs={'class': 'form_control', 'placeholder': 'Cake description'}),
            'price': forms.NumberInput(attrs={'class': 'form_control'}),
            'category': forms.Select(attrs={'class': 'form_select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form_select', 'size': '6'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form_control'}),
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