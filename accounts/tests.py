from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserRegistrationForm
from accounts.models import Profile

User = get_user_model()

# Create your tests here.
class UserModelTests(TestCase):
    def test_public_name_fallback(self):
        u = User.objects.create_user(username='a1', password='x' * 8 )
        self.assertEqual(u.get_public_name(), 'a1')
        u.display_name = ' Chef '
        u.save()
        self.assertEqual(u.get_public_name(), 'Chef')


class RegistrationFormTests(TestCase):
    def test_valid_registration(self):
        form = UserRegistrationForm(
            data={
                'username': 'testuser',
                'email': 'n@example.com',
                'display_name': 'New User',
                'password1': 'SomePass!234',
                'password2': 'SomePass!234',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)


class AccountViewTests(TestCase):
    def test_register_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_profile(self):
        self.client.post(
            reverse('accounts:register'),
            {
                'username': 'testuser2',
                'email': 'n@example.com',
                'display_name': 'New User2',
                'password1': 'SomePass!234',
                'password2': 'SomePass!234',
            }
        )
        user = User.objects.get(username='testuser2')
        self.assertTrue(Profile.objects.filter(user=user).exists())
