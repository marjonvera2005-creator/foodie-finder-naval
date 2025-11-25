from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant

class Command(BaseCommand):
    help = 'Restore original database and implement approval system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== RESTORING ORIGINAL DATABASE ==='))
        
        # 1. Ensure admin exists and is working
        admin_user, created = User.objects.get_or_create(
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
        admin_user.set_password('carlTzy1902')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        self.stdout.write(f'[ADMIN] {admin_user.email} / carlTzy1902 - READY')
        
        # 2. Create/restore restaurant accounts with their restaurants
        restaurants_data = [
            {
                'email': 'elpomar@restaurant.com',
                'name': 'El Pomar Restaurant',
                'restaurant_name': 'El Pomar',
                'category': 'Filipino',
                'location': 'Naval Proper'
            },
            {
                'email': 'enjestkitchen@restaurant.com', 
                'name': 'Enjest Kitchen Restaurant',
                'restaurant_name': 'Enjest Kitchen',
                'category': 'Filipino',
                'location': 'Naval Proper'
            },
            {
                'email': 'manginasal@restaurant.com',
                'name': 'Mang Inasal Restaurant', 
                'restaurant_name': 'Mang Inasal',
                'category': 'Filipino',
                'location': 'Naval Proper'
            },
            {
                'email': 'big_cup\'s@gmail.com',
                'name': 'Big Daddy\'s Cup',
                'restaurant_name': 'Big Daddy\'s Cup',
                'category': 'Cafe',
                'location': 'Naval Proper'
            }
        ]
        
        for data in restaurants_data:
            # Create or get user
            user, created = User.objects.get_or_create(
                username=data['email'],
                defaults={
                    'email': data['email'],
                    'first_name': data['name'].split()[0],
                    'last_name': ' '.join(data['name'].split()[1:]),
                    'is_active': True  # Make active for now
                }
            )
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            # Create or get restaurant
            restaurant, created = Restaurant.objects.get_or_create(
                name=data['restaurant_name'],
                defaults={
                    'location': data['location'],
                    'category': data['category'],
                    'open_time': '08:00',
                    'close_time': '22:00',
                    'description': f'Welcome to {data["restaurant_name"]}!',
                    'is_approved': True
                }
            )
            
            # Create or update profile
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
            
            self.stdout.write(f'[RESTAURANT] {user.email} / test123 - READY')
        
        # 3. Create test regular users
        regular_users = [
            ('testuser@example.com', 'Test', 'User'),
            ('jollibee@test.com', 'Jollibee', 'Manager'),
        ]
        
        for email, first_name, last_name in regular_users:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True  # Make active for now
                }
            )
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'user',
                    'contact_number': '09123456789'
                }
            )
            if not created:
                profile.role = 'user'
                profile.save()
            
            self.stdout.write(f'[USER] {user.email} / test123 - READY')
        
        self.stdout.write(self.style.SUCCESS('\n=== DATABASE RESTORED ==='))
        self.stdout.write('All accounts are ACTIVE and ready to login!')
        self.stdout.write('\nADMIN: carlmarco19@gmail.com / carlTzy1902')
        self.stdout.write('RESTAURANTS: [email] / test123') 
        self.stdout.write('USERS: [email] / test123')
        self.stdout.write('\nApproval system is ready - new registrations will need approval.')