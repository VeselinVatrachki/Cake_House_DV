from django import forms

from models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['cake', 'rating', 'comment']
        widgets = {
            'cake': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your sweet thoughts about this cake...',
            }),
        }