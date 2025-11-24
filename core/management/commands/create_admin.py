from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = 'Create or fix admin user'

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
        
        if not created:
            # Update existing user
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()
        else:
            user.set_password(password)
            user.save()
        
        # Create or update profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'admin',
                'contact_number': '09123456789'
            }
        )
        
        if not created:
            profile.role = 'admin'
            profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'Admin user ready: {email} / {password}'))