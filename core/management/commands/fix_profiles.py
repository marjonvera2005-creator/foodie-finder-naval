from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = 'Fix users without profiles'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        
        for user in users_without_profiles:
            # Determine role based on user attributes
            if user.is_superuser:
                role = 'admin'
            else:
                role = 'user'
            
            Profile.objects.create(
                user=user,
                role=role,
                contact_number='Not provided'
            )
            self.stdout.write(f'Created profile for {user.username} with role {role}')
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {users_without_profiles.count()} users'))