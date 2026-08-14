from django.db import models


class Product(models.Model):
    """A sellable product, e.g. 'Nike Air Max'."""

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    A specific variant of a product (e.g. size 42) with its own stock count.
    Products with no size variants (e.g. a laptop) can use a single
    variant with size='' to represent overall stock.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=20, blank=True, help_text="Leave blank if product has no sizes.")
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        size_label = self.size if self.size else 'default'
        return f"{self.product.name} - {size_label} ({self.stock_quantity} in stock)"
