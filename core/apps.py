from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        # Auto-create accounts when app starts
        try:
            from django.contrib.auth.models import User
            from .models import Profile, Restaurant, Dish, DishServing
            
            # Only run if no admin exists
            if not User.objects.filter(is_superuser=True).exists():
                # Create admin
                admin = User.objects.create_user(
                    username='carlmarco19@gmail.com',
                    email='carlmarco19@gmail.com',
                    password='carlTzy1902',
                    first_name='Carl',
                    last_name='Marco',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                
                # Create restaurant accounts
                restaurants = [
                    ('elpomar@restaurant.com', 'El Pomar', 'Restaurant', 'El Pomar'),
                    ('enjestkitchen@restaurant.com', 'Enjest Kitchen', 'Restaurant', 'Enjest Kitchen'),
                    ('manginasal@restaurant.com', 'Mang Inasal', 'Restaurant', 'Mang Inasal'),
                    ('bigcup@restaurant.com', 'Big Daddy Cup', 'Restaurant', 'Big Daddy Cup'),
                ]
                
                for email, name, last_name, resto_name in restaurants:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password='test123',
                        first_name=name,
                        last_name=last_name,
                        is_active=True
                    )
                    
                    restaurant = Restaurant.objects.create(
                        name=resto_name,
                        location='Naval Proper',
                        category='Filipino',
                        open_time='08:00',
                        close_time='22:00',
                        description=f'Welcome to {resto_name}!',
                        is_approved=True,
                        featured=True
                    )
                    
                    Profile.objects.create(
                        user=user,
                        role='restaurant',
                        contact_number='09123456789',
                        restaurant=restaurant
                    )
                    
                    # Create sample dishes
                    dishes = ['Adobo', 'Sinigang', 'Lechon Kawali', 'Pancit']
                    for dish_name in dishes:
                        dish = Dish.objects.create(
                            name=dish_name,
                            restaurant=restaurant,
                            description=f'Delicious {dish_name}'
                        )
                        DishServing.objects.create(
                            dish=dish,
                            serving_size='solo',
                            price=120
                        )
                
                # Create regular users
                users = [
                    ('testuser@example.com', 'Test', 'User'),
                    ('jollibee@test.com', 'Jollibee', 'Manager'),
                ]
                
                for email, first_name, last_name in users:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password='test123',
                        first_name=first_name,
                        last_name=last_name,
                        is_active=True
                    )
                    
                    Profile.objects.create(
                        user=user,
                        role='user',
                        contact_number='09123456789'
                    )
        except Exception:
            pass  # Ignore errors during startup