from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Set all non-admin users as inactive for testing approval system'

    def handle(self, *args, **options):
        # Set all non-admin users as inactive
        users = User.objects.filter(is_superuser=False, is_staff=False)
        count = users.update(is_active=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully set {count} users as inactive')
        )
        
        # Show which users were affected
        for user in users:
            self.stdout.write(f'- {user.email} ({user.get_full_name() or user.username})')