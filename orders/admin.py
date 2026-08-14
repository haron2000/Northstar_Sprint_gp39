from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'order_date', 'expected_delivery', 'courier')
    list_filter = ('status',)
    search_fields = ('order_number', 'tracking_number')