from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant


class Command(BaseCommand):
    help = 'Create test restaurant account'

    def handle(self, *args, **options):
        email = 'jollibee@test.com'
        password = 'test123'
        
        # Delete existing if exists
        User.objects.filter(username=email).delete()
        
        # Create restaurant user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name='Jollibee',
            last_name='Manager',
            is_active=True
        )
        
        # Create restaurant
        restaurant = Restaurant.objects.create(
            name='Jollibee Naval',
            location='Naval Proper, Biliran',
            open_time='06:00',
            close_time='22:00',
            category='Fast Food',
            description='The home of the world-famous Chickenjoy!',
            featured=True,
            is_approved=True
        )
        
        # Create profile
        Profile.objects.create(
            user=user,
            role='restaurant',
            contact_number='09123456789',
            restaurant=restaurant
        )
        
        self.stdout.write(self.style.SUCCESS(f'Test restaurant account created:'))
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Restaurant: {restaurant.name}')