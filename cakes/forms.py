from django import forms
from django.utils.text import slugify

from .models import Cake, Category, Tag, validate_image_size


class CakeForm(forms.ModelForm):
    """
    Form for creating and updating Cake objects.

    Key features:
    - Slug is optional and auto-generated from name
    - Category is entered as text and created if it doesn't exist
    - Tags are entered as a comma-separated string and created/reused
    - Image size is validated
    - Owner is automatically assigned on creation
    """
    
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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Velvet Dream'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-filled if empty'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

        # Replace category dropdown with text input
        self.fields['category'] = forms.CharField(
            label='Category',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Birthday'}),
        )
        # Pre-fill category when editing existing object
        if self.instance and self.instance.pk and self.instance.category_id:
            self.fields['category'].initial = self.instance.category.name

        # Replace tags field with comma-separated text input
        self.fields['tags'] = forms.CharField(
            required=False,
            label='Tags',
            help_text='Comma-separated. Existing tags are reused; new ones are created automatically.',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. chocolate, vegan, birthday'}),
        )
        # Pre-fill tags when editing
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join(t.name for t in self.instance.tags.all())

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        name = self.cleaned_data.get('name', '')
        
        # Auto-generate slug if missing
        if not slug and name:
            slug = slugify(name)
        if not slug:
            raise forms.ValidationError('Provide a slug or a name to generate one.')
        return slug

    def clean_category(self):
        """
        Converts category name into a Category object.
        """
        
        name = self.cleaned_data['category'].strip()
        slug = slugify(name)
        if not slug:
            raise forms.ValidationError('Enter a valid category name.')
        # Get existing or create new category
        cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        return cat

    def clean_tags(self):
        """
        Processes comma-separated tags into Tag objects.
        """
        tags_str = self.cleaned_data.get('tags', '').strip()
        if not tags_str:
            return []
        result = []
        for name in tags_str.split(','):
            name = name.strip()
            if name:
                slug = slugify(name)
                if slug:
                    tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
                    result.append(tag)
        return result

    def clean_image(self):
        """
        Validates uploaded image size using custom validator.
        """
        image = self.cleaned_data.get('image')
        if image:
            validate_image_size(image)
        return image

    def save(self, commit=True):
        """
        Saves the Cake instance.
        """
        obj = super().save(commit=False)
        if self.user and not obj.pk:
            obj.owner = self.user
        if commit:
            obj.save()
            obj.tags.set(self.cleaned_data.get('tags', []))
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
