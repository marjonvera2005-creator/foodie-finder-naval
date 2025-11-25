#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodie_finder.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Restaurant, Profile

def create_restaurant_accounts():
    """Create all restaurant accounts with proper linking"""
    
    # Restaurant data
    restaurants_data = [
        ('elpomar@restaurant.com', 'El Pomar', 'El Pomar'),
        ('enjestkitchen@restaurant.com', 'Enjest Kitchen', 'Enjest Kitchen'),
        ('manginasal@restaurant.com', 'Mang Inasal', 'Mang Inasal'),
        ('bigcup@restaurant.com', 'Big Daddy Cup', 'Big Daddy Cup'),
    ]
    
    print("Creating restaurant accounts...")
    
    for email, name, resto_name in restaurants_data:
        print(f"\nProcessing {email}...")
        
        # Create or get user
        user, user_created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': name,
                'last_name': 'Restaurant',
                'is_active': True
            }
        )
        
        # Set password
        user.set_password('test123')
        user.is_active = True
        user.save()
        
        print(f"  User {'created' if user_created else 'updated'}: {user.email}")
        
        # Create or get restaurant
        restaurant, resto_created = Restaurant.objects.get_or_create(
            name=resto_name,
            defaults={
                'location': 'Naval Proper',
                'category': 'Filipino',
                'open_time': '08:00',
                'close_time': '22:00',
                'description': f'Welcome to {resto_name}!',
                'is_approved': True,
                'featured': True
            }
        )
        
        print(f"  Restaurant {'created' if resto_created else 'found'}: {restaurant.name}")
        
        # Create or update profile
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'restaurant',
                'contact_number': '09123456789',
                'restaurant': restaurant
            }
        )
        
        # Update existing profile if needed
        if not profile_created:
            profile.role = 'restaurant'
            profile.restaurant = restaurant
            profile.save()
        
        print(f"  Profile {'created' if profile_created else 'updated'}: {profile.role}")
        print(f"  ✓ Account ready: {email} / test123")
    
    print(f"\n✅ All restaurant accounts created successfully!")
    print("\nLogin credentials:")
    for email, _, _ in restaurants_data:
        print(f"  {email} / test123")

if __name__ == '__main__':
    create_restaurant_accounts()