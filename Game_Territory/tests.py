from django.test import TestCase, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .signals import create_user_profile, save_user_profile

from .models import Product, Order, OrderItem
from . import analytics

settings.MIGRATION_MODULES = {"Game_Territory": None}

@override_settings(MIGRATION_MODULES={"Game_Territory": None})
class AnalyticsTests(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        self.user = User.objects.create_user(username="tester")
        self.product = Product.objects.create(
            name="Test",
            description="test",
            price=10,
            stock=5,
        )
        self.order = Order.objects.create(
            customer=self.user,
            status="processed",
            delivery_method="pickup",
            full_name="Tester",
            phone="123",
            is_paid=True,
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=10,
        )

    def test_total_revenue(self):
        self.assertEqual(analytics.total_revenue(), 20)

    def test_order_status_counts(self):
        counts = {c["status"]: c["count"] for c in analytics.order_status_counts()}
        self.assertEqual(counts.get("processed"), 1)

    def test_top_products(self):
        top = analytics.top_products(1)[0]
        self.assertEqual(top["product__name"], "Test")
        self.assertEqual(top["quantity"], 2)


