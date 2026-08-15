from django.shortcuts import render

from .models import Product


def stock_search(request):
    """
    Searches for a product by name (case-insensitive partial match) and
    optional size. Handles: existing product, unavailable variant,
    unknown product, missing search input.
    """
    product_name = request.GET.get('product_name', '').strip()
    size = request.GET.get('size', '').strip()
    variants = []
    product = None
    error = None
    searched = 'product_name' in request.GET

    if searched:
        if not product_name:
            error = "Please enter a product name to search."
        else:
            product = Product.objects.filter(name__icontains=product_name).first()
            if not product:
                error = f"No product found matching '{product_name}'."
            else:
                variant_qs = product.variants.all()
                if size:
                    variant_qs = variant_qs.filter(size__iexact=size)
                variants = list(variant_qs)
                if size and not variants:
                    error = f"'{product.name}' does not have a size '{size}' on record."

    return render(request, 'inventory/stock_search.html', {
        'product': product,
        'variants': variants,
        'error': error,
        'submitted_product_name': product_name,
        'submitted_size': size,
    })