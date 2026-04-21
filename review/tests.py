from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cakes.models import Category, Cake
from review.forms import ReviewForm
from review.models import Review

User = get_user_model()
# Create your tests here.
class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='x' *8)
        self.category = Category.objects.create(name='Bday', slug='bday')
        self.cake = Cake.objects.create(
            name='Test',
            slug='test-cake',
            description='Test Cake',
            price=Decimal(10.00),
            owner=self.user,
            category=self.category,
        )

    def test_review_comment(self):
        review = Review.objects.create(cake=self.cake, user=self.user, rating=5, comment='Test review')
        self.assertIn('testuser', str(review))

class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='x' * 8)
        self.category = Category.objects.create(name='Bday', slug='bday')
        self.cake = Cake.objects.create(
            name='Test2',
            slug='test-cake2',
            description='Test Cake2',
            price=Decimal(10.00),
            owner=self.user,
            category=self.category,
        )

    def test_valid_review(self):
        form = ReviewForm(data={'cake': self.cake.pk, 'rating': 4, 'comment': 'Test'})
        self.assertTrue(form.is_valid(), form.errors)


class ReviewViewTests(TestCase):
    def test_review_list(self):
        response = self.client.get(reverse('review:list'))
        self.assertEqual(response.status_code, 200)