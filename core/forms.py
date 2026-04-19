from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search cakes...'}),
        error_messages={
            'max_length': 'Search is too long (max 100 characters).',
            'required': 'Please enter a search term.'
        }
    )
    

class DeleteConfirmForm(forms.Form):
    confirm = forms.BooleanField(
        label='Are you sure you want to delete this item?',
        required=True,
    )
