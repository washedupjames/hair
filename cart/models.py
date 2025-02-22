from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # For logged-in users
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'product'), ('session_key', 'product'))  # Prevent duplicate items per user/session

    def __str__(self):
        return f"{self.quantity} x {self.product.title} for {self.user or self.session_key}"