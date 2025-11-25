from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reset all user passwords and activate accounts'

    def handle(self, *args, **options):
        # Reset all non-admin user passwords to 'test123'
        users = User.objects.filter(is_superuser=False)
        
        for user in users:
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            profile = getattr(user, 'profile', None)
            role = profile.get_role_display() if profile else 'Unknown'
            self.stdout.write(f'Fixed: {user.email} - {role} - Password: test123')
        
        # Reset admin password
        admin_user = User.objects.filter(email='carlmarco19@gmail.com').first()
        if admin_user:
            admin_user.set_password('carlTzy1902')
            admin_user.is_active = True
            admin_user.save()
            self.stdout.write(f'Fixed: {admin_user.email} - Admin - Password: carlTzy1902')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {users.count()} user passwords')
        )