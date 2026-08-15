from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductVariant


class StockSearchViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Nike Air Max', sku='NK-AIRMAX-001', category='Footwear',
        )
        ProductVariant.objects.create(product=self.product, size='42', stock_quantity=6)
        ProductVariant.objects.create(product=self.product, size='41', stock_quantity=0)

    def test_existing_product_with_available_variant(self):
        response = self.client.get(reverse('inventory:stock_search'), {
            'product_name': 'Nike Air Max', 'size': '42',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'In Stock')
        self.assertContains(response, '6')

    def test_existing_product_with_out_of_stock_variant(self):
        response = self.client.get(reverse('inventory:stock_search'), {
            'product_name': 'Nike Air Max', 'size': '41',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Out of Stock')

    def test_unknown_product_shows_error(self):
        response = self.client.get(reverse('inventory:stock_search'), {
            'product_name': 'Nonexistent Product',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No product found')

    def test_missing_product_name_shows_error(self):
        response = self.client.get(reverse('inventory:stock_search'), {'product_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a product name')

    def test_unknown_size_for_known_product_shows_error(self):
        response = self.client.get(reverse('inventory:stock_search'), {
            'product_name': 'Nike Air Max', 'size': '99',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not have a size')
