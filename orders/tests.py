from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cakes.models import Category, Cake
from orders.forms import OrderForm
from orders.models import Order, OrderLine

User = get_user_model()
# Create your tests here.
class OrderModelTests(TestCase):
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

    def test_order_total(self):
        order = Order.objects.create(user=self.user, event_date=date.today())
        OrderLine.objects.create(order=order, cake=self.cake, quantity=2)
        self.assertEqual(order.total, Decimal(20.00))


class OrderFormTests(TestCase):
    def test_order_form(self):
        form = OrderForm(data={'event_date': '2028-01-08', 'note': 'Test note'})
        self.assertTrue(form.is_valid(), form.errors)


class OrderViewTests(TestCase):
    def SetUp(self):
        self.user = User.objects.create_user(username='testuser', password='x' *8)
        self.client.login(username='testuser', password='x' *8)

    def test_order_list_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 302)


class ApiTests(TestCase):
    def test_cakes_api(self):
        response = self.client.get('/api/cakes/')
        self.assertIn(response.status_code, (200, 401))