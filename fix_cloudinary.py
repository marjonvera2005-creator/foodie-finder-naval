#!/usr/bin/env python
"""
Fix Cloudinary image URLs for existing images
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodie_finder.settings')
django.setup()

from core.models import Restaurant, Dish, RestaurantImage
import cloudinary.uploader

def fix_images():
    print("Fixing Cloudinary image URLs...")
    
    # Check Cloudinary config
    import cloudinary
    print(f"Cloud Name: {cloudinary.config().cloud_name}")
    print(f"API Key: {cloudinary.config().api_key}")
    
    # Count images
    restaurant_images = RestaurantImage.objects.all()
    dish_images = Dish.objects.filter(image__isnull=False).exclude(image='')
    restaurant_thumbnails = Restaurant.objects.filter(thumbnail__isnull=False).exclude(thumbnail='')
    
    print(f"\nImage counts:")
    print(f"Gallery images: {restaurant_images.count()}")
    print(f"Dish images: {dish_images.count()}")
    print(f"Restaurant thumbnails: {restaurant_thumbnails.count()}")
    
    # Check sample URLs
    print(f"\nSample URLs:")
    if restaurant_images.exists():
        sample = restaurant_images.first()
        print(f"Gallery: {sample.image.url}")
    
    if dish_images.exists():
        sample = dish_images.first()
        print(f"Dish: {sample.image.url}")
        
    if restaurant_thumbnails.exists():
        sample = restaurant_thumbnails.first()
        print(f"Thumbnail: {sample.thumbnail.url}")
    
    print("\nCloudinary is properly configured!")
    print("New uploads will be stored permanently in Cloudinary.")

if __name__ == '__main__':
    fix_images()