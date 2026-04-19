from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from cakes.models import Tag
from .models import User, Profile


class UserRegistrationForm(UserCreationForm):
    display_name = forms.CharField(
        max_length=255,
        required=False,
        label='Display Name',
        help_text='This will be displayed on your reviews and orders.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Display Name',
            'autocomplete': 'name'
        }),
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='This will be used for orders confirmations and password reset.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'display_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('password1', 'password2'):
            self.fields[name].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'username'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.display_name = self.cleaned_data['display_name'] or ''
        if commit:
            user.save()
        return user


class UserDisplayNamesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('display_name', 'email')
        labels = {
            'display_name': 'Display Name',
            'email': 'Email',
        }
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
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
            'bio': 'About You',
            'phone': 'Phone Number',
            'avatar': 'Profile Picture',
            'favorite_tags': 'Favorite Flavors',
        }
        help_texts = {
            'bio': 'A short bio visible on your public profile.',
            'phone': 'Optional; staff may contact you at this number about your order.',
            'avatar': 'A photo of yourself, for your profile.',
            'favorite_tags': 'Help us find cakes that match your taste!'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Tell us about your sweet tooth...'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-456-7890'}),
        }

    def __init__(self, *args, user=None,**kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.get_username()
        self.fields['favorite_tags'].widget.attrs.update({'class': 'form-control'})
        if self.instance and self.instance.pk:
            self.fields['favorite_tags'].queryset = Tag.objects.all()


class DeleteConfirmForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label='I understand this cannot be undone.',
        error_messages={'required': 'Please confirm before deleting.'},
    )

