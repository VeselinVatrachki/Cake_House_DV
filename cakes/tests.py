from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cakes.forms import GalleryFilterForm
from cakes.models import Category, Cake

# Create your tests here.
User = get_user_model()


class CakeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='x' *8)
        self.category = Category.objects.create(name='Bday', slug='bday')

    def test_absolute_url(self):
        cake = Cake.objects.create(
            name='Test',
            slug='test-cake',
            description='Test Cake',
            price=Decimal(10.00),
            owner=self.user,
            category=self.category,
        )
        self.assertEqual('/cake/test-cake/', cake.get_absolute_url())


class GalleryViewTests(TestCase):
    def test_gallery_view(self):
        response = self.client.get(reverse('cakes:gallery'))
        self.assertEqual(response.status_code, 200)


class GalleryFilterTests(TestCase):
    def test_gallery_filter(self):
        test_filter = GalleryFilterForm({})
        self.assertTrue(test_filter.is_valid())