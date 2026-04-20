from django import forms
from django.utils.text import slugify

from .models import Cake, Category, validate_image_size, Tag


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

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        name = self.cleaned_data.get('name', '')
        if not slug and name:
            slug = slugify(name)
        if not slug:
            raise forms.ValidationError('Provide a slug or a name to generate one.')
        return slug

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image_size(image)
        return image

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.user and not obj.pk:
            obj.owner = self.user
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class GalleryFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search cakes…',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label='Category',
        empty_label='All categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        label='Tag',
        empty_label='All tags',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Newest first'),
            ('price_asc', 'Price: low to high'),
            ('price_desc', 'Price: high to low'),
            ('name', 'Name A–Z'),
        ],
        label='Sort',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['tag'].queryset = Tag.objects.all()
