from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from authentication.models import UserProfile
from card_management.models import CardType, Card, CardOrder
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed database with dummy data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--cards',
            type=int,
            default=5,
            help='Number of card types to create (default: 5)'
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=20,
            help='Number of card orders to create (default: 20)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@maltacard.com',
                password='admin123'
            )
            Token.objects.create(user=admin_user)
            UserProfile.objects.create(
                user=admin_user,
                phone_number='+356 1234 5678',
                address='123 Admin Street',
                city='Valletta',
                state='Valletta',
                postal_code='VLT 1234',
                country='Malta'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: admin/admin123'))
        
        # Create card types
        card_types_data = [
            {
                'name': 'Standard Malta Card',
                'description': 'Basic Malta identification card with standard features',
                'price': 25.00,
                'validity_period': 5,
                'features': 'Basic identification, photo, personal details'
            },
            {
                'name': 'Premium Malta Card',
                'description': 'Enhanced Malta card with additional security features',
                'price': 50.00,
                'validity_period': 10,
                'features': 'Advanced security, biometric data, digital signature'
            },
            {
                'name': 'Student Malta Card',
                'description': 'Special card for students with educational benefits',
                'price': 15.00,
                'validity_period': 3,
                'features': 'Student discounts, library access, transport benefits'
            },
            {
                'name': 'Senior Malta Card',
                'description': 'Card designed for senior citizens with special privileges',
                'price': 20.00,
                'validity_period': 7,
                'features': 'Senior discounts, healthcare benefits, priority services'
            },
            {
                'name': 'Business Malta Card',
                'description': 'Professional card for business and corporate use',
                'price': 75.00,
                'validity_period': 8,
                'features': 'Business privileges, corporate access, enhanced security'
            }
        ]
        
        card_types = []
        for card_data in card_types_data:
            card_type, created = CardType.objects.get_or_create(
                name=card_data['name'],
                defaults=card_data
            )
            card_types.append(card_type)
            if created:
                self.stdout.write(f'Created card type: {card_type.name}')
        
        # Create users with profiles
        users_data = [
            {
                'username': 'john.doe',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'password123',
                'profile': {
                    'phone_number': '+356 2345 6789',
                    'address': '456 Main Street',
                    'city': 'Sliema',
                    'state': 'Sliema',
                    'postal_code': 'SLM 2345',
                    'country': 'Malta'
                }
            },
            {
                'username': 'jane.smith',
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'password123',
                'profile': {
                    'phone_number': '+356 3456 7890',
                    'address': '789 Oak Avenue',
                    'city': 'St. Julian\'s',
                    'state': 'St. Julian\'s',
                    'postal_code': 'STJ 3456',
                    'country': 'Malta'
                }
            },
            {
                'username': 'mike.wilson',
                'email': 'mike.wilson@example.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'password': 'password123',
                'profile': {
                    'phone_number': '+356 4567 8901',
                    'address': '321 Pine Road',
                    'city': 'Mdina',
                    'state': 'Mdina',
                    'postal_code': 'MDN 4567',
                    'country': 'Malta'
                }
            },
            {
                'username': 'sarah.jones',
                'email': 'sarah.jones@example.com',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'password': 'password123',
                'profile': {
                    'phone_number': '+356 5678 9012',
                    'address': '654 Elm Street',
                    'city': 'Rabat',
                    'state': 'Rabat',
                    'postal_code': 'RBT 5678',
                    'country': 'Malta'
                }
            },
            {
                'username': 'david.brown',
                'email': 'david.brown@example.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'password': 'password123',
                'profile': {
                    'phone_number': '+356 6789 0123',
                    'address': '987 Maple Drive',
                    'city': 'Mosta',
                    'state': 'Mosta',
                    'postal_code': 'MST 6789',
                    'country': 'Malta'
                }
            }
        ]
        
        users = []
        for user_data in users_data:
            profile_data = user_data.pop('profile')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                Token.objects.create(user=user)
                UserProfile.objects.create(user=user, **profile_data)
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)
        
        # Create additional random users
        additional_users = options['users'] - len(users_data)
        for i in range(additional_users):
            user_num = i + 1
            user = User.objects.create_user(
                username=f'user{user_num}',
                email=f'user{user_num}@example.com',
                first_name=f'User{user_num}',
                last_name=f'Test',
                password='password123'
            )
            Token.objects.create(user=user)
            UserProfile.objects.create(
                user=user,
                phone_number=f'+356 {7000 + user_num:04d} {1000 + user_num:04d}',
                address=f'{100 + user_num} Test Street',
                city=random.choice(['Valletta', 'Sliema', 'St. Julian\'s', 'Mdina', 'Rabat']),
                state=random.choice(['Valletta', 'Sliema', 'St. Julian\'s', 'Mdina', 'Rabat']),
                postal_code=f'TEST {1000 + user_num:04d}',
                country='Malta'
            )
            users.append(user)
            self.stdout.write(f'Created additional user: {user.username}')
        
        # Create card orders
        order_statuses = ['pending', 'processing', 'approved', 'rejected', 'completed']
        payment_methods = ['credit_card', 'bank_transfer', 'cash', 'paypal']
        
        for i in range(options['orders']):
            user = random.choice(users)
            card_type = random.choice(card_types)
            order_date = timezone.now() - timedelta(days=random.randint(0, 30))
            
            order = CardOrder.objects.create(
                user=user,
                card_type=card_type,
                quantity=random.randint(1, 3),
                total_amount=card_type.price * random.randint(1, 3),
                status=random.choice(order_statuses),
                payment_method=random.choice(payment_methods),
                order_date=order_date,
                delivery_address=f'{random.randint(100, 999)} {random.choice(["Street", "Avenue", "Road", "Drive"])}',
                delivery_city=random.choice(['Valletta', 'Sliema', 'St. Julian\'s', 'Mdina', 'Rabat']),
                delivery_postal_code=f'DEL {random.randint(1000, 9999):04d}',
                special_instructions=random.choice(['', 'Handle with care', 'Leave at reception', 'Call before delivery'])
            )
            
            # Create cards for completed orders
            if order.status == 'completed':
                for j in range(order.quantity):
                    Card.objects.create(
                        order=order,
                        card_number=f'MC{order.id:06d}{j+1:02d}',
                        status='active',
                        issue_date=order.order_date + timedelta(days=random.randint(1, 7)),
                        expiry_date=order.order_date + timedelta(days=card_type.validity_period * 365)
                    )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with:'))
        self.stdout.write(f'- {User.objects.count()} users')
        self.stdout.write(f'- {CardType.objects.count()} card types')
        self.stdout.write(f'- {CardOrder.objects.count()} card orders')
        self.stdout.write(f'- {Card.objects.count()} cards')
        self.stdout.write(f'- {Token.objects.count()} authentication tokens')
        
        self.stdout.write(self.style.SUCCESS('\nSeed data creation completed!'))
        self.stdout.write(self.style.WARNING('\nDefault admin credentials:'))
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        self.stdout.write(self.style.WARNING('\nDefault user credentials:'))
        self.stdout.write('Username: john.doe (or any created user)')
        self.stdout.write('Password: password123') 