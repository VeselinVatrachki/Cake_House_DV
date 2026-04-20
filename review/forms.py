from django import forms

from cakes.models import Cake

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('cake', 'rating', 'comment')
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
                'rows': 4,
                'placeholder': 'Share your sweet thoughts…',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].choices = [(i, str(i)) for i in range(1, 6)]
        self.fields['cake'].queryset = Cake.objects.all()


class ReviewSearchForm(forms.Form):
    cake = forms.ModelChoiceField(
        queryset=Cake.objects.none(),
        required=False,
        label='Filter by cake',
        empty_label='All cakes',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    min_rating = forms.TypedChoiceField(
        coerce=int,
        required=False,
        choices=[('', 'Any rating')] + [(i, f'{i}+ stars') for i in range(1, 6)],
        label='Minimum rating',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cake'].queryset = Cake.objects.all()
