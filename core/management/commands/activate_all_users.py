from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Activate all inactive users'

    def handle(self, *args, **options):
        inactive_users = User.objects.filter(is_active=False, is_superuser=False)
        count = inactive_users.update(is_active=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully activated {count} users')
        )
        
        for user in inactive_users:
            profile = getattr(user, 'profile', None)
            role = profile.get_role_display() if profile else 'Unknown'
            self.stdout.write(f'- {user.email} ({role})')