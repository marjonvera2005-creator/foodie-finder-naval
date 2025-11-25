from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant

class Command(BaseCommand):
    help = 'Fix restaurant account links to their specific restaurants'

    def handle(self, *args, **options):
        # Restaurant mappings
        restaurant_mappings = [
            ('elpomar@restaurant.com', 'El Pomar'),
            ('enjestkitchen@restaurant.com', 'Enjest Kitchen'),
            ('manginasal@restaurant.com', 'Mang Inasal'),
            ('bigcup@restaurant.com', 'Big Daddy\'s Cup'),
        ]
        
        for email, restaurant_name in restaurant_mappings:
            try:
                # Get user
                user = User.objects.get(username=email)
                
                # Get or create restaurant
                restaurant, created = Restaurant.objects.get_or_create(
                    name=restaurant_name,
                    defaults={
                        'location': 'Naval Proper',
                        'category': 'Filipino',
                        'open_time': '08:00',
                        'close_time': '22:00',
                        'description': f'Welcome to {restaurant_name}!',
                        'is_approved': True,
                        'featured': True
                    }
                )
                
                # Update profile to link to restaurant
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': 'restaurant',
                        'contact_number': '09123456789',
                        'restaurant': restaurant
                    }
                )
                
                if not created:
                    profile.role = 'restaurant'
                    profile.restaurant = restaurant
                    profile.save()
                
                self.stdout.write(f'[LINKED] {email} -> {restaurant_name}')
                
            except User.DoesNotExist:
                self.stdout.write(f'[NOT FOUND] {email}')
        
        self.stdout.write('Restaurant links updated!')