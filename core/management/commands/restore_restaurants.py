from django.core.management.base import BaseCommand
from core.models import Restaurant, Dish, DishServing, Category


class Command(BaseCommand):
    help = 'Restore and ensure all restaurants are visible'

    def handle(self, *args, **options):
        # Make all restaurants approved and visible
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            restaurant.is_approved = True
            restaurant.featured = True  # Make them featured so they show up
            restaurant.save()
            self.stdout.write(f'✓ Restored: {restaurant.name}')
        
        # Create some sample categories if they don't exist
        categories = ['Fast Food', 'Filipino', 'Chinese', 'Italian', 'Seafood', 'Dessert', 'Drinks']
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(f'✓ Created category: {cat_name}')
        
        # Ensure all dishes have at least one serving
        dishes_without_servings = Dish.objects.filter(servings__isnull=True)
        for dish in dishes_without_servings:
            DishServing.objects.create(
                dish=dish,
                serving_size='solo',
                price=100.00
            )
            self.stdout.write(f'✓ Added serving to: {dish.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Restored {restaurants.count()} restaurants'))
        self.stdout.write(self.style.SUCCESS('All restaurants are now visible and approved!'))