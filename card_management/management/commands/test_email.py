from django.core.management.base import BaseCommand
from django.core.mail import send_mail, get_connection
from django.conf import settings
from card_management.models import Card, CardOrder
from authentication.models import CustomUser
import smtplib
import ssl


class Command(BaseCommand):
    help = 'Test email functionality with detailed diagnostics'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address to send test to')
        parser.add_argument('--test-smtp', action='store_true', help='Test SMTP connection directly')

    def handle(self, *args, **options):
        test_email = options.get('email', 'pyshohan@gmail.com')
        
        self.stdout.write('🔍 Testing email functionality...')
        
        # Test 1: Check email settings
        self.stdout.write('\n📧 Email Settings:')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD: {"*" * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD != "your-app-password" else "NOT SET"}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        
        # Test 2: Check if password is set
        if settings.EMAIL_HOST_PASSWORD == 'your-app-password':
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  EMAIL_HOST_PASSWORD is not set! You need to set your Gmail app password.'
                )
            )
            self.stdout.write(
                '📝 To fix this:'
            )
            self.stdout.write('   1. Go to https://myaccount.google.com/')
            self.stdout.write('   2. Enable 2-Step Verification')
            self.stdout.write('   3. Go to Security → App passwords')
            self.stdout.write('   4. Generate app password for "Mail"')
            self.stdout.write('   5. Set EMAIL_HOST_PASSWORD in your .env file')
            return
        
        # Test 3: Test SMTP connection directly
        if options.get('test_smtp'):
            self.stdout.write('\n🔌 Testing SMTP connection directly...')
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls(context=context)
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    self.stdout.write(
                        self.style.SUCCESS('✅ SMTP connection successful!')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ SMTP connection failed: {str(e)}')
                )
                return
        
        # Test 4: Test Django email sending
        self.stdout.write('\n📤 Testing Django email sending...')
        try:
            # Test simple email
            send_mail(
                subject='Test Email from MaltaCard',
                message='This is a test email from MaltaCard application.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Simple email sent successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send simple email: {str(e)}')
            )
            return
        
        # Test 5: Test order confirmation email
        orders = CardOrder.objects.all()
        if orders.exists():
            order = orders.first()
            self.stdout.write(f'\n📋 Found order: {order}')
            self.stdout.write(f'👤 Order user email: {order.user.email}')
            
            try:
                from card_management.signals import send_order_confirmation_email
                send_order_confirmation_email(order)
                self.stdout.write(
                    self.style.SUCCESS('✅ Order confirmation email sent successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send order confirmation email: {str(e)}')
                )
        else:
            self.stdout.write('No orders found in database')
        
        # Test 6: Check if using console backend
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Note: Emails are being sent to console. Check your terminal output!'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n✅ Emails should be sent to real email addresses!'
                )
            ) 