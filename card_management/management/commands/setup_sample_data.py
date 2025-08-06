from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from card_management.models import Card, CardOrder
from authentication.models import UserProfile
from core.models import CardType

class Command(BaseCommand):
    help = 'Set up sample data for the card management system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up sample data...')
        
        # Create sample card types
        card_types_data = [
            {
                'name': 'Basic Weekly',
                'description': 'Basic card type for weekly usage',
                'duration_type': 'weekly',
                'price': 4.99,
                'features': ['Basic transactions', 'Weekly limits'],
                'max_transactions': 100,
                'daily_limit': 500.00,
                'monthly_limit': 2000.00,
                'is_popular': False,
                'sort_order': 1,
            },
            {
                'name': 'Premium Monthly',
                'description': 'Premium card type for monthly usage with enhanced features',
                'duration_type': 'monthly',
                'price': 19.99,
                'features': ['Premium transactions', 'Monthly limits', 'Rewards program'],
                'max_transactions': 500,
                'daily_limit': 2000.00,
                'monthly_limit': 10000.00,
                'is_popular': True,
                'sort_order': 2,
            },
            {
                'name': 'Enterprise Yearly',
                'description': 'Enterprise card type for yearly usage with unlimited features',
                'duration_type': 'yearly',
                'price': 199.99,
                'features': ['Unlimited transactions', 'Yearly limits', 'Premium rewards', 'Priority support'],
                'max_transactions': 10000,
                'daily_limit': 10000.00,
                'monthly_limit': 100000.00,
                'is_popular': True,
                'sort_order': 3,
            },
        ]
        
        for card_type_data in card_types_data:
            card_type, created = CardType.objects.get_or_create(
                name=card_type_data['name'],
                defaults=card_type_data
            )
            if created:
                self.stdout.write(f'Created card type: {card_type.name}')
            else:
                self.stdout.write(f'Card type already exists: {card_type.name}')
        
        # Create sample cards
        cards_data = [
            {
                'name': 'Virtual Debit Card',
                'card_type': 'virtual',
                'description': 'Instant virtual debit card for online transactions',
                'price': 9.99,
                'is_active': True,
            },
            {
                'name': 'Virtual Credit Card',
                'card_type': 'virtual',
                'description': 'Virtual credit card with rewards program',
                'price': 19.99,
                'is_active': True,
            },
            {
                'name': 'Physical Debit Card',
                'card_type': 'physical',
                'description': 'Physical debit card with chip and contactless',
                'price': 29.99,
                'is_active': True,
            },
            {
                'name': 'Physical Credit Card',
                'card_type': 'physical',
                'description': 'Premium physical credit card with travel benefits',
                'price': 49.99,
                'is_active': True,
            },
            {
                'name': 'Student Virtual Card',
                'card_type': 'virtual',
                'description': 'Budget-friendly virtual card for students',
                'price': 4.99,
                'is_active': True,
            },
        ]
        
        # Get card types for linking
        basic_weekly = CardType.objects.get(name='Basic Weekly')
        premium_monthly = CardType.objects.get(name='Premium Monthly')
        enterprise_yearly = CardType.objects.get(name='Enterprise Yearly')
        
        for i, card_data in enumerate(cards_data):
            # Link cards to card types based on price
            if card_data['price'] <= 10:
                card_data['card_type_config'] = basic_weekly
            elif card_data['price'] <= 30:
                card_data['card_type_config'] = premium_monthly
            else:
                card_data['card_type_config'] = enterprise_yearly
            
            card, created = Card.objects.get_or_create(
                name=card_data['name'],
                defaults=card_data
            )
            if created:
                self.stdout.write(f'Created card: {card.name}')
            else:
                self.stdout.write(f'Card already exists: {card.name}')
        
        # Create a sample user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write('Created demo user: demo_user (password: demo123)')
        
        # Create sample orders
        sample_orders = [
            {
                'user': user,
                'card': Card.objects.get(name='Virtual Debit Card'),
                'quantity': 1,
                'status': 'pending',
            },
            {
                'user': user,
                'card': Card.objects.get(name='Physical Credit Card'),
                'quantity': 2,
                'status': 'processing',
                'shipping_address': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10001',
                'country': 'USA',
                'phone_number': '+1234567890',
            },
        ]
        
        for order_data in sample_orders:
            order, created = CardOrder.objects.get_or_create(
                user=order_data['user'],
                card=order_data['card'],
                status=order_data['status'],
                defaults=order_data
            )
            if created:
                self.stdout.write(f'Created order: {order}')
            else:
                self.stdout.write(f'Order already exists: {order}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data setup completed successfully!')
        ) 