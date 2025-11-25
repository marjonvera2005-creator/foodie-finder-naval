from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant

class Command(BaseCommand):
    help = 'Create all accounts immediately on deployed server'

    def handle(self, *args, **options):
        # Create or update admin
        admin, created = User.objects.get_or_create(
            username='carlmarco19@gmail.com',
            defaults={
                'email': 'carlmarco19@gmail.com',
                'first_name': 'Carl',
                'last_name': 'Marco',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        admin.set_password('carlTzy1902')
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.save()
        
        # Create restaurant accounts
        restaurants = [
            ('elpomar@restaurant.com', 'El Pomar', 'Restaurant', 'El Pomar'),
            ('enjestkitchen@restaurant.com', 'Enjest Kitchen', 'Restaurant', 'Enjest Kitchen'),
            ('manginasal@restaurant.com', 'Mang Inasal', 'Restaurant', 'Mang Inasal'),
            ('bigcup@restaurant.com', 'Big Daddy Cup', 'Restaurant', 'Big Daddy Cup'),
        ]
        
        for email, name, last_name, resto_name in restaurants:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': name,
                    'last_name': last_name,
                    'is_active': True
                }
            )
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            restaurant, created = Restaurant.objects.get_or_create(
                name=resto_name,
                defaults={
                    'location': 'Naval Proper',
                    'category': 'Filipino',
                    'open_time': '08:00',
                    'close_time': '22:00',
                    'description': f'Welcome to {resto_name}!',
                    'is_approved': True
                }
            )
            
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'restaurant',
                    'contact_number': '09123456789',
                    'restaurant': restaurant
                }
            )
        
        # Create regular users
        users = [
            ('testuser@example.com', 'Test', 'User'),
            ('jollibee@test.com', 'Jollibee', 'Manager'),
        ]
        
        for email, first_name, last_name in users:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True
                }
            )
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'user',
                    'contact_number': '09123456789'
                }
            )
        
        self.stdout.write('ACCOUNTS CREATED:')
        self.stdout.write('Admin: carlmarco19@gmail.com / carlTzy1902')
        self.stdout.write('Restaurants: elpomar@restaurant.com / test123')
        self.stdout.write('Restaurants: enjestkitchen@restaurant.com / test123')
        self.stdout.write('Restaurants: manginasal@restaurant.com / test123')
        self.stdout.write('Restaurants: bigcup@restaurant.com / test123')
        self.stdout.write('Users: testuser@example.com / test123')
        self.stdout.write('Users: jollibee@test.com / test123')