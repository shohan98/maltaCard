from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create tokens for all existing users'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_count = 0
        existing_count = 0
        
        for user in users:
            token, created = Token.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created token for user: {user.username}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Token already exists for user: {user.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Token creation completed. Created: {created_count}, Existing: {existing_count}'
            )
        ) 