from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant, Dish

class Command(BaseCommand):
    help = 'Show final complete database status'

    def handle(self, *args, **options):
        self.stdout.write('=== COMPLETE DATABASE STATUS ===\n')
        
        # Admin
        self.stdout.write('ADMIN ACCOUNT:')
        self.stdout.write('Email: carlmarco19@gmail.com')
        self.stdout.write('Password: carlTzy1902')
        self.stdout.write('Access: Admin Dashboard\n')
        
        # Restaurants with dishes
        self.stdout.write('RESTAURANT ACCOUNTS:')
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            profile = Profile.objects.filter(restaurant=restaurant).first()
            if profile:
                self.stdout.write(f'Restaurant: {restaurant.name}')
                self.stdout.write(f'Email: {profile.user.email}')
                self.stdout.write(f'Password: test123')
                self.stdout.write(f'Dishes: {restaurant.dishes.count()}')
                self.stdout.write(f'Category: {restaurant.category}')
                self.stdout.write(f'Access: Restaurant Dashboard')
                self.stdout.write('---')
        
        # Regular users
        self.stdout.write('\nREGULAR USER ACCOUNTS:')
        users = User.objects.filter(profile__role='user', is_active=True)
        for user in users:
            self.stdout.write(f'Name: {user.get_full_name()}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Password: test123')
            self.stdout.write(f'Access: Main Foodie Page')
            self.stdout.write('---')
        
        # Statistics
        self.stdout.write('\nDATABASE STATISTICS:')
        self.stdout.write(f'Total Restaurants: {Restaurant.objects.count()}')
        self.stdout.write(f'Total Dishes: {Dish.objects.count()}')
        self.stdout.write(f'Total Users: {User.objects.count()}')
        self.stdout.write(f'Active Users: {User.objects.filter(is_active=True).count()}')
        
        self.stdout.write('\n=== ALL SYSTEMS READY ===')
        self.stdout.write('Website: https://foodie-finder-naval-2zqm.onrender.com/')
        self.stdout.write('Login: https://foodie-finder-naval-2zqm.onrender.com/login/')
        self.stdout.write('Admin: https://foodie-finder-naval-2zqm.onrender.com/console/')