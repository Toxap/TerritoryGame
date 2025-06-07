from django.db.models import Sum, Count, F

from .models import Order, OrderItem


def order_status_counts():
    """Return order counts grouped by status."""
    return Order.objects.values('status').annotate(count=Count('status'))


def total_revenue():
    """Return total revenue from paid orders."""
    result = OrderItem.objects.filter(order__is_paid=True).aggregate(
        total=Sum(F('price') * F('quantity'))
    )
    return result['total'] or 0


def top_products(limit=5):
    """Return most sold products by quantity."""
    return (
        OrderItem.objects.filter(order__is_paid=True)
        .values('product__name')
        .annotate(quantity=Sum('quantity'))
        .order_by('-quantity')[:limit]
    )
