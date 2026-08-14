from django.shortcuts import render

from .models import Order


def order_status(request):
    """
    Looks up an order by order number, entered via a GET query param.
    Handles: valid order, invalid/unknown order, missing input.
    """
    order_number = request.GET.get('order_number', '').strip()
    order = None
    error = None

    if 'order_number' in request.GET:
        if not order_number:
            error = "Please enter an order number."
        else:
            try:
                order = Order.objects.get(order_number__iexact=order_number)
            except Order.DoesNotExist:
                error = f"No order found with number '{order_number}'. Please check and try again."

    return render(request, 'orders/order_status.html', {
        'order': order,
        'error': error,
        'submitted_order_number': order_number,
    })
