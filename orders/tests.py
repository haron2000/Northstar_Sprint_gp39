from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Order


class OrderStatusViewTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            order_number='NS10001',
            order_date=date(2026, 8, 8),
            status=Order.STATUS_IN_TRANSIT,
            expected_delivery=date(2026, 8, 15),
            courier='Northstar Express',
            tracking_number='NSE458921',
        )

    def test_valid_order_number_returns_order_details(self):
        response = self.client.get(reverse('orders:order_status'), {'order_number': 'NS10001'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NS10001')
        self.assertContains(response, 'In Transit')
        self.assertContains(response, 'NSE458921')

    def test_invalid_order_number_shows_error(self):
        response = self.client.get(reverse('orders:order_status'), {'order_number': 'NS99999'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No order found')
        self.assertIsNone(response.context['order'])

    def test_missing_order_number_shows_error(self):
        response = self.client.get(reverse('orders:order_status'), {'order_number': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter an order number')

    def test_no_search_submitted_shows_no_error(self):
        response = self.client.get(reverse('orders:order_status'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['error'])
