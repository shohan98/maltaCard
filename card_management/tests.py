from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from .models import Card, CardType, CardOrder


class CardOrderTestCase(TestCase):
    """Test cases for card order functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create test card type
        self.card_type = CardType.objects.create(
            name='Premium Card',
            description='Premium card with high limits',
            duration_type='monthly',
            price=99.99,
            features=['High limits', 'Priority support'],
            max_transactions=5000,
            daily_limit=5000.00,
            monthly_limit=50000.00,
            is_popular=True,
            sort_order=1
        )
        
        # Create test card
        self.card = Card.objects.create(
            name='Premium Virtual Card',
            card_type=self.card_type,
            description='Premium virtual card for online transactions',
            price=99.99,
            total_orders=0
        )
    
    def test_card_total_orders_increment_on_order_creation(self):
        """Test that card total_orders increases when order is created"""
        initial_orders = self.card.total_orders
        
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=2,
            total_amount=199.98
        )
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Check that total_orders increased by quantity
        self.assertEqual(self.card.total_orders, initial_orders + 2)
    
    def test_card_total_orders_decrement_on_order_deletion(self):
        """Test that card total_orders decreases when order is deleted"""
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=3,
            total_amount=299.97
        )
        
        # Refresh card from database
        self.card.refresh_from_db()
        orders_after_creation = self.card.total_orders
        
        # Delete the order
        order.delete()
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Check that total_orders decreased by quantity
        self.assertEqual(self.card.total_orders, orders_after_creation - 3)
    
    def test_card_total_orders_never_goes_below_zero(self):
        """Test that card total_orders never goes below zero"""
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=5,
            total_amount=499.95
        )
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Delete the order
        order.delete()
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Check that total_orders is not negative
        self.assertGreaterEqual(self.card.total_orders, 0)
    
    def test_order_confirmation_email_sent_on_creation(self):
        """Test that order confirmation email is sent when order is created"""
        # Clear mail outbox
        mail.outbox.clear()
        
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=1,
            total_amount=99.99
        )
        
        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email details
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Order Confirmation - {self.card.name}")
        self.assertEqual(email.to, [self.user.email])
        self.assertIn("Order Confirmation", email.body)
    
    def test_order_status_update_email_sent_on_status_change(self):
        """Test that status update email is sent when order status changes"""
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=1,
            total_amount=99.99
        )
        
        # Clear mail outbox
        mail.outbox.clear()
        
        # Update order status
        order.status = 'processing'
        order.save()
        
        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email details
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Order Status Update - {self.card.name} (Order #{order.id})")
        self.assertEqual(email.to, [self.user.email])
        self.assertIn("Order Status Update", email.body)
    
    def test_no_email_sent_on_other_field_changes(self):
        """Test that no email is sent when other fields change (not status)"""
        # Create an order
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=1,
            total_amount=99.99
        )
        
        # Clear mail outbox
        mail.outbox.clear()
        
        # Update order quantity (not status)
        order.quantity = 2
        order.save()
        
        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)
    
    def test_order_total_amount_calculation(self):
        """Test that order total amount is calculated correctly"""
        # Create an order without total_amount
        order = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=3
        )
        
        # Check that total_amount was calculated correctly
        expected_total = self.card.price * 3
        self.assertEqual(order.total_amount, expected_total)
    
    def test_multiple_orders_affect_total_orders_correctly(self):
        """Test that multiple orders affect total_orders correctly"""
        # Create multiple orders
        order1 = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=2,
            total_amount=199.98
        )
        
        order2 = CardOrder.objects.create(
            user=self.user,
            card=self.card,
            quantity=1,
            total_amount=99.99
        )
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Check total orders
        self.assertEqual(self.card.total_orders, 3)
        
        # Delete one order
        order1.delete()
        
        # Refresh card from database
        self.card.refresh_from_db()
        
        # Check total orders after deletion
        self.assertEqual(self.card.total_orders, 1)
