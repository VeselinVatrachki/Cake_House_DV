from django import forms
from django.utils.text import slugify

from .models import Cake, Category, Tag, validate_image_size


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ('name', 'slug', 'image', 'description', 'price', 'category', 'tags')
        labels = {
            'name': 'Cake name',
            'slug': 'URL slug',
            'image': 'Photo',
            'description': 'Description',
            'price': 'Price (EUR)',
            'category': 'Category',
            'tags': 'Tags',
        }
        # help_texts = {
        #     'slug': 'Leave blank to auto-generate from the name.',
        #     'tags': 'Hold Ctrl/Cmd to select multiple.',
        # }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Velvet Dream'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-filled if empty'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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
