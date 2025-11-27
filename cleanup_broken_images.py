#!/usr/bin/env python
"""
Clean up broken image references that point to non-existent Cloudinary URLs
"""
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodie_finder.settings')
django.setup()

from core.models import Restaurant, Dish, RestaurantImage

def check_url_exists(url):
    """Check if a URL returns 200 OK"""
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def cleanup_broken_images():
    print("Cleaning up broken image references...")
    
    # Check restaurant gallery images
    broken_gallery = []
    gallery_images = RestaurantImage.objects.all()
    
    print(f"Checking {gallery_images.count()} gallery images...")
    for img in gallery_images:
        if not check_url_exists(img.image.url):
            broken_gallery.append(img)
            print(f"Broken gallery image: {img.image.url}")
    
    # Check dish images
    broken_dishes = []
    dish_images = Dish.objects.filter(image__isnull=False).exclude(image='')
    
    print(f"Checking {dish_images.count()} dish images...")
    for dish in dish_images:
        if not check_url_exists(dish.image.url):
            broken_dishes.append(dish)
            print(f"Broken dish image: {dish.image.url}")
    
    # Check restaurant thumbnails
    broken_thumbnails = []
    restaurant_thumbnails = Restaurant.objects.filter(thumbnail__isnull=False).exclude(thumbnail='')
    
    print(f"Checking {restaurant_thumbnails.count()} restaurant thumbnails...")
    for restaurant in restaurant_thumbnails:
        if not check_url_exists(restaurant.thumbnail.url):
            broken_thumbnails.append(restaurant)
            print(f"Broken thumbnail: {restaurant.thumbnail.url}")
    
    print(f"\nSummary:")
    print(f"Broken gallery images: {len(broken_gallery)}")
    print(f"Broken dish images: {len(broken_dishes)}")
    print(f"Broken thumbnails: {len(broken_thumbnails)}")
    
    # Clean up broken references
    if broken_gallery:
        print(f"\nDeleting {len(broken_gallery)} broken gallery images...")
        for img in broken_gallery:
            img.delete()
    
    if broken_dishes:
        print(f"Clearing {len(broken_dishes)} broken dish images...")
        for dish in broken_dishes:
            dish.image = None
            dish.save()
    
    if broken_thumbnails:
        print(f"Clearing {len(broken_thumbnails)} broken thumbnails...")
        for restaurant in broken_thumbnails:
            restaurant.thumbnail = None
            restaurant.save()
    
    print("\nCleanup complete! All broken image references removed.")
    print("New uploads will be stored properly in Cloudinary.")

if __name__ == '__main__':
    cleanup_broken_images()