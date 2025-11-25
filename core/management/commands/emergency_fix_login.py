from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Emergency fix for all login issues on deployed server'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== EMERGENCY LOGIN FIX ==='))
        
        # Fix admin account
        admin_emails = ['carlmarco19@gmail.com', 'admin@example.com']
        for email in admin_emails:
            try:
                user = User.objects.get(username=email)
                user.set_password('carlTzy1902')
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(f'FIXED ADMIN: {email} / carlTzy1902')
            except User.DoesNotExist:
                pass
        
        # Fix all restaurant accounts
        restaurant_accounts = [
            'elpomar@restaurant.com',
            'enjestkitchen@restaurant.com', 
            'manginasal@restaurant.com',
            'big_cup\'s@gmail.com',
            'testrestaurant@example.com'
        ]
        
        for email in restaurant_accounts:
            try:
                user = User.objects.get(username=email)
                user.set_password('test123')
                user.is_active = True  # Activate for testing
                user.save()
                
                # Ensure profile exists with restaurant role
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'restaurant', 'contact_number': '09123456789'}
                )
                if not created and profile.role != 'restaurant':
                    profile.role = 'restaurant'
                    profile.save()
                
                self.stdout.write(f'FIXED RESTAURANT: {email} / test123')
            except User.DoesNotExist:
                self.stdout.write(f'NOT FOUND: {email}')
        
        # Fix regular user accounts
        user_accounts = [
            'testuser@example.com',
            'jollibee@test.com',
            'newuser@test.com'
        ]
        
        for email in user_accounts:
            try:
                user = User.objects.get(username=email)
                user.set_password('test123')
                user.is_active = True  # Activate for testing
                user.save()
                
                # Ensure profile exists with user role
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'user', 'contact_number': '09123456789'}
                )
                if not created and profile.role not in ['user', 'restaurant']:
                    profile.role = 'user'
                    profile.save()
                
                self.stdout.write(f'FIXED USER: {email} / test123')
            except User.DoesNotExist:
                self.stdout.write(f'NOT FOUND: {email}')
        
        self.stdout.write(self.style.SUCCESS('\n=== ALL ACCOUNTS READY ==='))
        self.stdout.write('Admin: carlmarco19@gmail.com / carlTzy1902')
        self.stdout.write('Restaurants: [email] / test123')
        self.stdout.write('Users: [email] / test123')
        self.stdout.write('\nAll accounts are now ACTIVE and ready to login!')