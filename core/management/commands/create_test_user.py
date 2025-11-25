from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Create a test user for approval system testing'

    def handle(self, *args, **options):
        # Create test regular user
        email = 'testuser@example.com'
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(
                username=email,
                email=email,
                password='test123',
                first_name='Test',
                last_name='User',
                is_active=False  # Needs approval
            )
            
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'contact_number': '09123456789',
                    'role': 'user'
                }
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created test user: {email} (password: test123)')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Test user {email} already exists')
            )
        
        # Create test restaurant user
        email = 'testrestaurant@example.com'
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(
                username=email,
                email=email,
                password='test123',
                first_name='Test',
                last_name='Restaurant',
                is_active=False  # Needs approval
            )
            
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'contact_number': '09987654321',
                    'role': 'restaurant'
                }
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created test restaurant user: {email} (password: test123)')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Test restaurant user {email} already exists')
            )