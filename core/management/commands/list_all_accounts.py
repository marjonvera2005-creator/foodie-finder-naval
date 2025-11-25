from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'List all registered accounts with their credentials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== ALL REGISTERED ACCOUNTS ===\n'))
        
        # Admin accounts
        self.stdout.write(self.style.ERROR('ADMIN ACCOUNTS:'))
        admin_users = User.objects.filter(is_superuser=True)
        for user in admin_users:
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: carlTzy1902 (for carlmarco19@gmail.com)')
            self.stdout.write(f'Status: {"Active" if user.is_active else "Inactive"}')
            self.stdout.write('---')
        
        # Restaurant accounts
        self.stdout.write(self.style.WARNING('\nRESTAURANT ACCOUNTS:'))
        restaurant_users = User.objects.filter(profile__role='restaurant')
        for user in restaurant_users:
            profile = user.profile
            self.stdout.write(f'Name: {user.get_full_name() or user.username}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: test123')
            self.stdout.write(f'Status: {"Active" if user.is_active else "Inactive (needs approval)"}')
            if profile.restaurant:
                self.stdout.write(f'Restaurant: {profile.restaurant.name}')
            self.stdout.write('---')
        
        # Regular user accounts
        self.stdout.write(self.style.SUCCESS('\nREGULAR USER ACCOUNTS:'))
        regular_users = User.objects.filter(profile__role='user')
        for user in regular_users:
            self.stdout.write(f'Name: {user.get_full_name() or user.username}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: test123')
            self.stdout.write(f'Status: {"Active" if user.is_active else "Inactive (needs approval)"}')
            self.stdout.write('---')
        
        # Test accounts
        self.stdout.write(self.style.HTTP_INFO('\nTEST ACCOUNTS:'))
        test_emails = ['testuser@example.com', 'testrestaurant@example.com']
        for email in test_emails:
            try:
                user = User.objects.get(username=email)
                profile = user.profile
                self.stdout.write(f'Email: {email}')
                self.stdout.write(f'Password: test123')
                self.stdout.write(f'Role: {profile.get_role_display()}')
                self.stdout.write(f'Status: {"Active" if user.is_active else "Inactive (needs approval)"}')
                self.stdout.write('---')
            except User.DoesNotExist:
                pass
        
        self.stdout.write(self.style.SUCCESS('\n=== SUMMARY ==='))
        self.stdout.write(f'Total Users: {User.objects.count()}')
        self.stdout.write(f'Active Users: {User.objects.filter(is_active=True).count()}')
        self.stdout.write(f'Pending Approval: {User.objects.filter(is_active=False).count()}')