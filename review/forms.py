from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['cake', 'rating', 'comment']
        labels = {
            'cake': 'Cake',
            'rating': 'Rating',
            'comment': 'Your review',
        }
        help_texts = {
            'rating': '1 = lowest, 5 = highest',
            'comment': 'Be kind and specific.',
        }
        widgets = {
            'cake': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Share your sweet thoughts about this cake...'}),
        }