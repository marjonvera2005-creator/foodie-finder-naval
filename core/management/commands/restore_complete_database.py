from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant, Dish, DishServing, Category

class Command(BaseCommand):
    help = 'Restore complete original database with all restaurants and dishes'

    def handle(self, *args, **options):
        self.stdout.write('=== RESTORING COMPLETE DATABASE ===')
        
        # Create categories
        categories = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Drinks', 'Desserts', 'Filipino', 'Fast Food', 'Cafe']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        
        # Create admin
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
        
        # Restaurant data with dishes
        restaurants_data = [
            {
                'email': 'elpomar@restaurant.com',
                'name': 'El Pomar Restaurant',
                'restaurant_name': 'El Pomar',
                'category': 'Filipino',
                'location': 'Naval Proper',
                'description': 'Authentic Filipino cuisine in the heart of Naval',
                'dishes': [
                    {'name': 'Adobo', 'price': 120, 'description': 'Classic Filipino adobo'},
                    {'name': 'Sinigang', 'price': 150, 'description': 'Sour soup with pork'},
                    {'name': 'Lechon Kawali', 'price': 180, 'description': 'Crispy pork belly'},
                    {'name': 'Pancit Canton', 'price': 100, 'description': 'Stir-fried noodles'},
                ]
            },
            {
                'email': 'enjestkitchen@restaurant.com',
                'name': 'Enjest Kitchen Restaurant',
                'restaurant_name': 'Enjest Kitchen',
                'category': 'Filipino',
                'location': 'Naval Proper',
                'description': 'Home-style Filipino cooking',
                'dishes': [
                    {'name': 'Kare-Kare', 'price': 200, 'description': 'Oxtail stew with peanut sauce'},
                    {'name': 'Bulalo', 'price': 250, 'description': 'Beef bone marrow soup'},
                    {'name': 'Crispy Pata', 'price': 300, 'description': 'Deep-fried pork leg'},
                    {'name': 'Sisig', 'price': 160, 'description': 'Sizzling pork sisig'},
                ]
            },
            {
                'email': 'manginasal@restaurant.com',
                'name': 'Mang Inasal Restaurant',
                'restaurant_name': 'Mang Inasal',
                'category': 'Fast Food',
                'location': 'Naval Proper',
                'description': 'Famous for grilled chicken and unlimited rice',
                'dishes': [
                    {'name': 'Chicken Inasal', 'price': 99, 'description': 'Grilled chicken with rice'},
                    {'name': 'Pork BBQ', 'price': 89, 'description': 'Grilled pork skewers'},
                    {'name': 'Bangus Sisig', 'price': 120, 'description': 'Milkfish sisig'},
                    {'name': 'Halo-Halo', 'price': 65, 'description': 'Mixed ice dessert'},
                ]
            },
            {
                'email': 'bigcup@restaurant.com',
                'name': 'Big Daddy Cup',
                'restaurant_name': 'Big Daddy\'s Cup',
                'category': 'Cafe',
                'location': 'Naval Proper',
                'description': 'Coffee, pastries and light meals',
                'dishes': [
                    {'name': 'Iced Coffee', 'price': 80, 'description': 'Cold brew coffee'},
                    {'name': 'Cappuccino', 'price': 95, 'description': 'Espresso with steamed milk'},
                    {'name': 'Chocolate Cake', 'price': 120, 'description': 'Rich chocolate cake slice'},
                    {'name': 'Club Sandwich', 'price': 150, 'description': 'Triple-layer sandwich'},
                ]
            }
        ]
        
        for data in restaurants_data:
            # Create user
            user, created = User.objects.get_or_create(
                username=data['email'],
                defaults={
                    'email': data['email'],
                    'first_name': data['name'].split()[0],
                    'last_name': ' '.join(data['name'].split()[1:]),
                    'is_active': True
                }
            )
            user.set_password('test123')
            user.is_active = True
            user.save()
            
            # Create restaurant
            restaurant, created = Restaurant.objects.get_or_create(
                name=data['restaurant_name'],
                defaults={
                    'location': data['location'],
                    'category': data['category'],
                    'open_time': '08:00',
                    'close_time': '22:00',
                    'description': data['description'],
                    'is_approved': True,
                    'featured': True
                }
            )
            
            # Create profile
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
            
            # Create dishes
            for dish_data in data['dishes']:
                dish, created = Dish.objects.get_or_create(
                    name=dish_data['name'],
                    restaurant=restaurant,
                    defaults={
                        'description': dish_data['description']
                    }
                )
                
                # Create serving size
                DishServing.objects.get_or_create(
                    dish=dish,
                    serving_size='solo',
                    defaults={'price': dish_data['price']}
                )
            
            self.stdout.write(f'[RESTAURANT] {data["restaurant_name"]} - {len(data["dishes"])} dishes')
        
        # Create regular users
        users = [
            ('testuser@example.com', 'Test', 'User'),
            ('jollibee@test.com', 'Jollibee', 'Manager'),
            ('customer1@test.com', 'John', 'Doe'),
            ('customer2@test.com', 'Jane', 'Smith'),
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
        
        self.stdout.write('=== DATABASE RESTORED ===')
        self.stdout.write('ADMIN: carlmarco19@gmail.com / carlTzy1902')
        self.stdout.write('RESTAURANTS: [email] / test123')
        self.stdout.write('USERS: [email] / test123')
        self.stdout.write(f'Total Restaurants: {Restaurant.objects.count()}')
        self.stdout.write(f'Total Dishes: {Dish.objects.count()}')
        self.stdout.write(f'Total Users: {User.objects.count()}')