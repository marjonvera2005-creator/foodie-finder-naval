from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = 'Reset restaurant passwords to test123'

    def handle(self, *args, **options):
        restaurant_users = User.objects.filter(profile__role='restaurant')
        
        for user in restaurant_users:
            user.set_password('test123')
            user.is_active = True
            user.save()
            self.stdout.write(f'Reset password for: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('All restaurant passwords reset to: test123'))
        self.stdout.write('Restaurant accounts:')
        for user in restaurant_users:
            self.stdout.write(f'  Email: {user.username} | Password: test123')