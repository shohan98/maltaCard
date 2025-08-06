from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from core.models import BaseModel
from model_utils import FieldTracker

User = get_user_model()

class CardType(BaseModel):
    """Model for card types with duration and pricing"""
    DURATION_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES, default='monthly')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)  # List of features
    max_transactions = models.PositiveIntegerField(default=1000)
    daily_limit = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    is_popular = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.get_duration_type_display()})"
    
    class Meta:
        ordering = ['sort_order', 'name']


class Card(BaseModel):
    """Model for different types of cards"""

    name = models.CharField(max_length=100)
    card_type = models.ForeignKey(
        CardType, 
        on_delete=models.CASCADE, 
        related_name='cards',
        null=True,
        blank=True
    )
    total_orders = models.PositiveIntegerField(default=0)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.card_type})"
    
    def recalculate_total_orders(self):
        """Recalculate total_orders based on actual order quantities"""
        from .models import CardOrder
        total = CardOrder.objects.filter(card=self).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        self.total_orders = total
        self.save(update_fields=['total_orders'])
        return self.total_orders
    
    class Meta:
        ordering = ['name']

class CardOrder(BaseModel):
    """Model for card orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Address fields for physical cards
    shipping_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Phone number for contact
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    
    order_date = models.DateTimeField(auto_now_add=True)
    
    # Field tracker for detecting changes
    tracker = FieldTracker(fields=['status', 'quantity'])
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.card.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount if not set or if quantity changed
        if not self.total_amount or (self.pk and self.tracker.has_changed('quantity')):
            self.total_amount = self.card.price * self.quantity
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-order_date']
