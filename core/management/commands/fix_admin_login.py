from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = 'Fix admin login issues'

    def handle(self, *args, **options):
        email = 'carlmarco19@gmail.com'
        password = 'carlTzy1902'
        
        # Get or create admin user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        # Update user properties
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        
        # Get or create admin profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'admin',
                'contact_number': '09123456789'
            }
        )
        
        # Update profile
        profile.role = 'admin'
        profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'Admin login fixed: {email} / {password}'))
        self.stdout.write(self.style.SUCCESS('Admin can now login and access /console/'))