from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Show all working accounts with credentials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== ALL WORKING ACCOUNTS ===\n'))
        
        # Admin accounts
        self.stdout.write(self.style.ERROR('ADMIN ACCOUNTS:'))
        admin_users = User.objects.filter(is_superuser=True, is_active=True)
        for user in admin_users:
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: carlTzy1902')
            self.stdout.write(f'Redirect: Admin Dashboard')
            self.stdout.write('---')
        
        # Restaurant accounts
        self.stdout.write(self.style.WARNING('\nRESTAURANT ACCOUNTS:'))
        restaurant_users = User.objects.filter(profile__role='restaurant', is_active=True)
        for user in restaurant_users:
            profile = user.profile
            self.stdout.write(f'Name: {user.get_full_name()}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: test123')
            self.stdout.write(f'Restaurant: {profile.restaurant.name if profile.restaurant else "None"}')
            self.stdout.write(f'Redirect: Restaurant Dashboard')
            self.stdout.write('---')
        
        # Regular users
        self.stdout.write(self.style.SUCCESS('\nREGULAR USER ACCOUNTS:'))
        regular_users = User.objects.filter(profile__role='user', is_active=True)
        for user in regular_users:
            self.stdout.write(f'Name: {user.get_full_name()}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: test123')
            self.stdout.write(f'Redirect: Main Foodie Page')
            self.stdout.write('---')
        
        self.stdout.write(self.style.SUCCESS('\n=== SUMMARY ==='))
        self.stdout.write(f'Total Active Users: {User.objects.filter(is_active=True).count()}')
        self.stdout.write(f'Admin Users: {admin_users.count()}')
        self.stdout.write(f'Restaurant Users: {restaurant_users.count()}')
        self.stdout.write(f'Regular Users: {regular_users.count()}')
        self.stdout.write('\nAll accounts are ACTIVE and ready to login!')
        self.stdout.write('Login URL: https://foodie-finder-naval-2zqm.onrender.com/login/')