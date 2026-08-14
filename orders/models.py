from django.db import models


class Order(models.Model):
    """
    A customer order that can be looked up by order number.
    Covers the 'Order Status' support category only (no returns/refunds).
    """

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_IN_TRANSIT = 'in_transit'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_IN_TRANSIT, 'In Transit'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    order_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="e.g. NS10001",
    )
    order_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    expected_delivery = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if not yet known (e.g. order still pending).",
    )
    courier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.order_number} ({self.get_status_display()})"