from django import forms
from django.contrib.auth.forms import UserCreationForm

from cakes.models import Tag

from .models import Profile, User


class UserRegistrationForm(UserCreationForm):
    display_name = forms.CharField(
        max_length=150,
        required=False,
        label='Display name',
        help_text='Optional name shown on reviews and orders.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'How we should greet you',
            'autocomplete': 'name',
        }),
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='Required. Used for order updates only.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'display_name', 'password1', 'password2')
        labels = {
            'username': 'Username',
        }
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('password1', 'password2'):
            self.fields[name].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'username'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.display_name = self.cleaned_data.get('display_name') or ''
        if commit:
            user.save()
        return user


class UserDisplayNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('display_name', 'email')
        labels = {'display_name': 'Display name', 'email': 'Email'}
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    """Profile edit; username shown read-only."""

    username = forms.CharField(
        disabled=True,
        required=False,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    class Meta:
        model = Profile
        fields = ('bio', 'phone', 'avatar', 'favorite_tags')
        labels = {
            'bio': 'About you',
            'phone': 'Phone',
            'avatar': 'Profile photo',
            'favorite_tags': 'Favorite flavors / tags',
        }
        help_texts = {
            'bio': 'A short bio visible on your public profile.',
            'phone': 'Optional; staff may contact you about orders.',
            'avatar': 'Square images look best.',
            'favorite_tags': 'Helps us suggest cakes.',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about your sweet tooth'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 …'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.get_username()
        self.fields['favorite_tags'].widget.attrs.update({'class': 'form-select'})
        if self.instance and self.instance.pk:
            self.fields['favorite_tags'].queryset = Tag.objects.all()


class DeleteConfirmForm(forms.Form):
    """Confirmation step before destructive actions."""

    confirm = forms.BooleanField(
        required=True,
        label='I understand this cannot be undone',
        error_messages={'required': 'Please confirm before deleting.'},
    )
