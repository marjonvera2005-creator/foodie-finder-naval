from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Restaurant, Dish, RestaurantImage, Profile


# Food vocabulary by category and letter
FOOD_BY_CATEGORY = {
    'breakfast': ["Tapsilog", "Hotsilog", "Longsilog", "Bangsilog", "Cornsilog", "Pancakes", "Champorado", "Arroz Caldo", "Lugaw", "Pandesal"],
    'lunch': ["Adobo", "Sinigang", "Kare-Kare", "Menudo", "Caldereta", "Pancit", "Fried Rice", "Grilled Fish", "Pork Chop", "Chicken Curry"],
    'dinner': ["Lechon", "Bistek", "Fish Tinola", "Beef Steak", "Grilled Chicken", "Seafood Platter", "Pork Adobo", "Chicken Inasal", "Grilled Pork", "Fish Fillet"],
    'snack': ["Lumpia", "Siomai", "Fishball", "Empanada", "Puto", "Kutsinta", "Bibingka", "Okoy", "Isaw", "Turon"],
    'drinks': ["Iced Coffee", "Fresh Juice", "Soda", "Water", "Iced Tea", "Lemonade", "Fruit Shake", "Coconut Water"],
    'milktea': ["Taro Milk Tea", "Matcha Milk Tea", "Thai Milk Tea", "Chocolate Milk Tea", "Strawberry Milk Tea", "Wintermelon Milk Tea", "Brown Sugar Milk Tea", "Okinawa Milk Tea"]
}

FOOD_BY_LETTER = {
    'A': ["Adobo", "Arroz Caldo", "Afritada", "Aligue Pasta", "Atchara"],
    'B': ["Bistek", "Bicol Express", "Batchoy", "Bibingka", "Bopis", "Bubble Tea"],
    'C': ["Caldereta", "Champorado", "Chicken Inasal", "Camaron", "Crispy Pata"],
    'D': ["Dinuguan", "Daing na Bangus", "Dilis", "Dynamite", "Dapang"],
    'E': ["Eggplant Adobo", "Ensaymada", "Empanada", "Escabeche", "Eggdrop"],
    'F': ["Fish Tinola", "Fried Chicken", "Fishball", "Fettuccine", "Fried Rice"],
    'G': ["Ginisang Munggo", "Ginataan", "Goto", "Gising-Gising", "Giniling"],
    'H': ["Halo-Halo", "Hamonado", "Humba", "Hotdog", "Hotsilog"],
    'I': ["Inihaw na Baboy", "Inasal", "Igado", "Inihaw na Manok", "Isaw", "Iced Coffee", "Ice Cream"],
    'J': ["Jelly Dessert", "Japchae", "Jambalaya", "Jalapeño Poppers", "Jicama Salad"],
    'K': ["Kare-Kare", "Kaldereta", "Kansi", "Kutsinta", "Kangkong"],
    'L': ["Lechon", "Laing", "Lomi", "Lumpia", "Lugaw"],
    'M': ["Menudo", "Mechado", "Mongo", "Maja Blanca", "Mais con Yelo", "Milk Tea", "Matcha Milk Tea"],
    'N': ["Nilaga", "Naval Noodles", "Nachos", "Nasi Goreng", "Nutri-sarap"],
    'O': ["Okoy", "Omelette", "Ox Tongue", "Oyster Sisig", "Oden"],
    'P': ["Pancit", "Pinakbet", "Pares", "Pares Mami", "Puto"],
    'Q': ["Quinoa Salad", "Quezo Ice Cream", "Quiche", "Quickmelt Burger", "Quesadilla"],
    'R': ["Relyenong Bangus", "Roast Beef", "Ramen", "Rice Bowl", "Rebosado"],
    'S': ["Sinigang", "Sisig", "Spaghetti", "Steak", "Siomai", "Strawberry Milk Tea"],
    'T': ["Tapsilog", "Tinola", "Tortang Talong", "Tokwa't Baboy", "Tuna Pasta", "Taro Milk Tea", "Thai Milk Tea"],
    'U': ["Ube Halaya", "Ukoy", "Utan Bisaya", "Udon", "Upside-down Cake"],
    'V': ["Vegetable Curry", "Vigan Longganisa", "Vanilla Pudding", "Vichysoisse", "Veggie Lumpia"],
    'W': ["Wagyu", "Waffles", "Wanton", "Waldorf Salad", "Wing Platter", "Wintermelon Milk Tea"],
    'X': ["Xiaolongbao", "XO Noodles", "Xavier Steak", "Xo Fried Rice", "X-web Sushi"],
    'Y': ["Yema Cake", "Yakitori", "Yakisoba", "Yogurt Parfait", "Yabby"],
    'Z': ["Ziti", "Zaru Soba", "Zucchini Salad", "Zinger Burger", "Zesty Wings"],
}


# Category suggestions (extendable). "All Food" is a special catch-all.
CATEGORY_SUGGESTIONS = [
    "All Food",
    "Breakfast",
    "Lunch", 
    "Dinner",
    "Snack",
    "Drinks",
    "Milktea",
    "Fast Food",
    "Seafood",
    "Dessert",
]




def landing_view(request):
    return render(request, 'landing.html')


def register_view(request):
    # Check if admin already exists
    admin_exists = User.objects.filter(is_superuser=True).exists()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'user')

        if password != confirm or not email:
            messages.error(request, "Please check your inputs.")
            return render(request, 'register.html', {'admin_exists': admin_exists})

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html', {'admin_exists': admin_exists})

        # Prevent admin registration if admin already exists
        if role == 'admin' and admin_exists:
            messages.error(request, "Admin account already exists.")
            return render(request, 'register.html', {'admin_exists': admin_exists})
        
        # Create user
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name
        )
        
        # Create profile safely
        try:
            profile = Profile.objects.create(
                user=user,
                contact_number=contact_number or 'Not provided',
                role=role
            )
        except Exception:
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'contact_number': contact_number or 'Not provided',
                    'role': role
                }
            )
        
        # Set admin privileges if admin role
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            messages.success(request, "Admin account created successfully! You can now log in.")
        else:
            # All non-admin users need approval
            user.is_active = False
            user.save()
            messages.success(request, "Registration successful! Your account is pending admin approval. You will be notified once approved.")
        
        return redirect('login')

    return render(request, 'register.html', {'admin_exists': admin_exists})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.warning(request, "Your account is pending admin approval. Please wait for approval before you can log in.")
                return render(request, 'login.html')
            
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}!")
            
            # Check if user is admin first
            if user.is_superuser or user.is_staff:
                return redirect('admin-dashboard')
            
            # Create profile if missing
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user, role='user')
            
            # Role-based redirection for approved users
            if profile.role == 'restaurant':
                return redirect('restaurant-dashboard')
            elif profile.role == 'user':
                return redirect('main')
            
            # Default fallback
            return redirect('main')
        messages.error(request, "Invalid email or password.")
        return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def main_view(request):
    featured_restos = Restaurant.objects.filter(featured=True).prefetch_related('dishes')[:6]
    categories = list(Restaurant.objects.values_list('category', flat=True).distinct())
    return render(request, 'main.html', {"featured": featured_restos, "categories": categories})


@login_required
def suggest_foods(request):
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        q_lower = q.lower()
        
        # Budget suggestions
        budget_suggestions = []
        if 'budget' in q_lower or 'less than' in q_lower or 'under' in q_lower:
            budget_suggestions = [
                'Budget less than 50',
                'Budget less than 100', 
                'Budget less than 150',
                'Budget less than 200'
            ]
        
        # Meal category suggestions (breakfast, lunch, dinner, etc.) - show first
        meal_categories = []
        for category in FOOD_BY_CATEGORY.keys():
            if category.startswith(q_lower):
                meal_categories.append(category.title())
        
        # Category-based food suggestions
        category_foods = []
        for category, foods in FOOD_BY_CATEGORY.items():
            if category.startswith(q_lower):
                category_foods.extend(foods[:3])
        
        # Restaurant suggestions
        restaurant_hits = list(Restaurant.objects.filter(name__istartswith=q).values_list('name', flat=True)[:3])
        
        # Category suggestions (from static list + DB distinct)
        db_categories = list(Restaurant.objects.values_list('category', flat=True).distinct())
        combined_categories = CATEGORY_SUGGESTIONS + [c for c in db_categories if c not in CATEGORY_SUGGESTIONS]
        category_hits = [c for c in combined_categories if c.lower().startswith(q_lower)][:3]

        # Dish name suggestions from curated vocabulary (first letter)
        first = q[0].upper() if q else ''
        letter_dishes = FOOD_BY_LETTER.get(first, [])[:3]

        # Dish name suggestions from database
        db_dishes = list(Dish.objects.filter(name__istartswith=q).values_list('name', flat=True).distinct()[:3])

        # Merge all suggestions with priority order: budget first, then meal categories
        merged = []
        for item in budget_suggestions + meal_categories + category_foods + restaurant_hits + category_hits + db_dishes + letter_dishes:
            if item not in merged:
                merged.append(item)
        suggestions = merged[:10]
    return JsonResponse({"suggestions": suggestions})


@login_required
def search_results(request):
    term = request.GET.get('q', '').strip()
    restaurants_with_dishes = []
    
    if term:
        term_lower = term.lower()
        
        # Check for budget search (e.g., "budget less than 100")
        import re
        budget_match = re.search(r'budget\s+less\s+than\s+(\d+)', term_lower)
        if budget_match:
            max_price = float(budget_match.group(1))
            from .models import DishServing
            serving_ids = DishServing.objects.filter(price__lt=max_price).values_list('dish_id', flat=True)
            dishes = Dish.objects.filter(id__in=serving_ids).select_related('restaurant')
            
            # Group dishes by restaurant
            restaurant_dict = {}
            for dish in dishes:
                restaurant = dish.restaurant
                if restaurant.id not in restaurant_dict:
                    restaurant_dict[restaurant.id] = {
                        'restaurant': restaurant,
                        'dishes': []
                    }
                restaurant_dict[restaurant.id]['dishes'].append(dish)
            
            restaurants_with_dishes = list(restaurant_dict.values())
        
        # Check if searching for meal categories
        elif term_lower in FOOD_BY_CATEGORY:
            # Get foods from the category
            category_foods = FOOD_BY_CATEGORY[term_lower]
            
            # Use Q objects to find dishes
            from django.db.models import Q
            query = Q()
            for food in category_foods:
                query |= Q(name__icontains=food)
            
            dishes = Dish.objects.filter(query).select_related('restaurant')
            
            # Group dishes by restaurant
            restaurant_dict = {}
            for dish in dishes:
                restaurant = dish.restaurant
                if restaurant.id not in restaurant_dict:
                    restaurant_dict[restaurant.id] = {
                        'restaurant': restaurant,
                        'dishes': []
                    }
                restaurant_dict[restaurant.id]['dishes'].append(dish)
            
            restaurants_with_dishes = list(restaurant_dict.values())
        
        # If searching by restaurant category or dish name
        else:
            if term_lower == 'all food':
                dishes = Dish.objects.all().select_related('restaurant')
            elif Restaurant.objects.filter(category__iexact=term).exists():
                dishes = Dish.objects.filter(restaurant__category__iexact=term).select_related('restaurant')
            else:
                dishes = Dish.objects.filter(name__icontains=term).select_related('restaurant')
            
            # Group by restaurant for consistent display
            restaurant_dict = {}
            for dish in dishes:
                restaurant = dish.restaurant
                if restaurant.id not in restaurant_dict:
                    restaurant_dict[restaurant.id] = {
                        'restaurant': restaurant,
                        'dishes': []
                    }
                restaurant_dict[restaurant.id]['dishes'].append(dish)
            
            restaurants_with_dishes = list(restaurant_dict.values())

    return render(request, 'category_results.html', {
        "restaurants_with_dishes": restaurants_with_dishes, 
        "term": term,
        "is_category": term.lower() in FOOD_BY_CATEGORY if term else False
    })


@login_required
def restaurant_detail(request, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    images = RestaurantImage.objects.filter(restaurant=restaurant)
    return render(request, 'restaurant_detail.html', {"restaurant": restaurant, "images": images})


def about_view(request):
    from .models import AboutContent
    about_content = AboutContent.objects.first()
    return render(request, 'about.html', {'about_content': about_content})


def logo_view(request):
    return render(request, 'logo.html')


def poster_view(request):
    return render(request, 'poster.html')


def advertisement_view(request):
    return render(request, 'advertisement.html')

# Create your views here.


# ------------------------
# Admin Dashboard (custom)
# ------------------------

def _ensure_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def _admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not _ensure_superuser(request.user):
            messages.error(request, "Admin access required.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapped


@require_http_methods(["GET", "POST"])
def admin_login_view(request):
    from django.contrib.auth.models import User
    # Ensure default admin exists if none
    if not User.objects.filter(is_superuser=True).exists():
        email = 'carlmarco19@gmail.com'
        password = 'carlTzy1902'
        user, _ = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': 'Admin'})
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
    # Allow register if fewer than 2 admins exist
    allow_register = User.objects.filter(is_superuser=True).count() < 2
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user and user.is_superuser:
            login(request, user)
            messages.success(request, "Welcome, Admin!")
            return redirect('admin-dashboard')
        messages.error(request, "Invalid admin credentials.")
    return render(request, 'admin/login.html', {"allow_register": allow_register})


def admin_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('landing')


@require_http_methods(["GET", "POST"])
def admin_register_view(request):
    # Only allow admin registration if no superuser exists yet
    from django.contrib.auth.models import User
    # Cap at 2 superusers
    if User.objects.filter(is_superuser=True).count() >= 2:
        messages.error(request, "Admin capacity reached. Please log in.")
        return redirect('admin-login')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if not email or password != confirm:
            messages.error(request, "Please check your inputs.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email already in use.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, "Admin account created. You can now log in.")
            return redirect('admin-login')
    return render(request, 'admin/register.html')


@_admin_required
def admin_dashboard(request):
    try:
        stats = {
            'restaurants': Restaurant.objects.count(),
            'dishes': Dish.objects.count(),
            'users': User.objects.count(),
            'pending_restaurants': Restaurant.objects.filter(is_approved=False).count(),
            'pending_users': User.objects.filter(is_active=False).count(),
        }
        recent_restos = Restaurant.objects.order_by('-id')[:6]
        recent_dishes = Dish.objects.select_related('restaurant').order_by('-id')[:6]
        users = User.objects.all().order_by('-date_joined')
        all_restaurants = Restaurant.objects.all().order_by('-id')
        pending_users = User.objects.filter(is_active=False).order_by('-date_joined')
        
        return render(request, 'admin/dashboard.html', {
            "stats": stats, 
            "recent_restos": recent_restos, 
            "recent_dishes": recent_dishes,
            "users": users,
            "all_restaurants": all_restaurants,
            "pending_users": pending_users,
        })
    except Exception as e:
        messages.error(request, f"Dashboard error: {str(e)}")
        return render(request, 'admin/dashboard.html', {
            "stats": {'restaurants': 0, 'dishes': 0, 'users': 0, 'pending_restaurants': 0, 'pending_users': 0},
            "recent_restos": [],
            "recent_dishes": [],
            "users": [],
            "all_restaurants": [],
            "pending_users": [],
        })


# --- Restaurant management ---
from django.forms import ModelForm


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'location', 'latitude', 'longitude', 'open_time', 'close_time', 'description', 'featured', 'thumbnail', 'category'
        ]


@_admin_required
def admin_restaurant_list(request):
    restos = Restaurant.objects.all().order_by('name')
    return render(request, 'admin/restaurants_list.html', {"restos": restos})


@_admin_required
@require_http_methods(["GET", "POST"])
def admin_restaurant_create(request):
    form = RestaurantForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Restaurant created.")
        return redirect('admin-restaurant-list')
    return render(request, 'admin/restaurant_form.html', {"form": form, "mode": "Create"})


@_admin_required
@require_http_methods(["GET", "POST"])
def admin_restaurant_edit(request, pk: int):
    resto = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantForm(request.POST or None, request.FILES or None, instance=resto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Restaurant updated.")
        return redirect('admin-restaurant-list')
    return render(request, 'admin/restaurant_form.html', {"form": form, "mode": "Edit", "resto": resto})


@_admin_required
@require_http_methods(["POST"])
def admin_restaurant_delete(request, pk: int):
    resto = get_object_or_404(Restaurant, pk=pk)
    resto.delete()
    messages.success(request, "Restaurant deleted.")
    return redirect('admin-restaurant-list')


# --- Dish management ---

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'restaurant', 'categories', 'description', 'image']


@_admin_required
def admin_dish_list(request):
    dishes = Dish.objects.select_related('restaurant').all().order_by('name')
    return render(request, 'admin/dishes_list.html', {"dishes": dishes})


@_admin_required
@require_http_methods(["GET", "POST"])
def admin_dish_create(request):
    form = DishForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        dish = form.save()
        # Create default solo serving
        from .models import DishServing
        DishServing.objects.create(
            dish=dish,
            serving_size='solo',
            price=100.00
        )
        messages.success(request, "Dish created with default serving size.")
        return redirect('admin-dish-list')
    return render(request, 'admin/dish_form.html', {"form": form, "mode": "Create"})


@_admin_required
@require_http_methods(["GET", "POST"])
def admin_dish_edit(request, pk: int):
    dish = get_object_or_404(Dish, pk=pk)
    form = DishForm(request.POST or None, request.FILES or None, instance=dish)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Dish updated.")
        return redirect('admin-dish-list')
    return render(request, 'admin/dish_form.html', {"form": form, "mode": "Edit", "dish": dish})


@_admin_required
@require_http_methods(["POST"])
def admin_dish_delete(request, pk: int):
    dish = get_object_or_404(Dish, pk=pk)
    dish.delete()
    messages.success(request, "Dish deleted.")
    return redirect('admin-dish-list')


# --- Restaurant images management ---

@_admin_required
def admin_restaurant_images(request, resto_id: int):
    resto = get_object_or_404(Restaurant, pk=resto_id)
    imgs = RestaurantImage.objects.filter(restaurant=resto).order_by('-id')
    return render(request, 'admin/images_list.html', {"resto": resto, "images": imgs})


@_admin_required
@require_http_methods(["GET", "POST"])
def admin_restaurant_images_add(request, resto_id: int):
    resto = get_object_or_404(Restaurant, pk=resto_id)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        created = 0
        for f in files:
            RestaurantImage.objects.create(restaurant=resto, image=f)
            created += 1
        if created:
            messages.success(request, f"Uploaded {created} image(s).")
        else:
            messages.error(request, "Please choose image files to upload.")
        return redirect('admin-restaurant-images', resto_id=resto.id)
    return render(request, 'admin/image_upload.html', {"resto": resto})


@_admin_required
@require_http_methods(["POST"])
def admin_image_delete(request, img_id: int):
    img = get_object_or_404(RestaurantImage, pk=img_id)
    resto_id = img.restaurant_id
    img.delete()
    messages.success(request, "Image deleted.")
    return redirect('admin-restaurant-images', resto_id=resto_id)


# ------------------------
# Restaurant Dashboard
# ------------------------

def _restaurant_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'restaurant':
            messages.error(request, "Restaurant access required.")
            return redirect('main')
        return view_func(request, *args, **kwargs)
    return wrapped


@_restaurant_required
def restaurant_dashboard(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    
    # If no restaurant assigned, create one or show error
    if not restaurant:
        # Auto-create restaurant for restaurant role users
        restaurant = Restaurant.objects.create(
            name=f"{request.user.get_full_name() or request.user.username}'s Restaurant",
            location="Naval Proper",
            open_time="08:00",
            close_time="22:00",
            category="Fast Food",
            description="Welcome to our restaurant!"
        )
        profile.restaurant = restaurant
        profile.save()
    
    featured_restos = Restaurant.objects.filter(featured=True).prefetch_related('dishes')[:6]
    categories = list(Restaurant.objects.values_list('category', flat=True).distinct())
    
    return render(request, 'restaurant/dashboard.html', {
        "featured": featured_restos, 
        "categories": categories,
        "restaurant": restaurant
    })


@_restaurant_required
@require_http_methods(["GET", "POST"])
def restaurant_edit(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    form = RestaurantForm(request.POST or None, request.FILES or None, instance=restaurant)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Restaurant updated successfully.")
        return redirect('restaurant-dashboard')
    
    return render(request, 'restaurant/edit.html', {"form": form, "restaurant": restaurant})


@_restaurant_required
def restaurant_dishes(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    dishes = Dish.objects.filter(restaurant=restaurant).order_by('name')
    return render(request, 'restaurant/dishes.html', {"dishes": dishes, "restaurant": restaurant})


@_restaurant_required
@require_http_methods(["GET", "POST"])
def restaurant_dish_create(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        
        if name:
            dish = Dish.objects.create(
                name=name, 
                restaurant=restaurant, 
                description=description,
                image=image
            )
            # Handle categories
            category_ids = request.POST.getlist('categories')
            if category_ids:
                dish.categories.set(category_ids)
            
            # Handle serving sizes and prices
            from .models import DishServing
            serving_sizes = ['solo', 'sharing', 'family', 'party']
            created_servings = 0
            
            for size in serving_sizes:
                price = request.POST.get(f'price_{size}', '').strip()
                if price:
                    try:
                        DishServing.objects.create(
                            dish=dish,
                            serving_size=size,
                            price=float(price)
                        )
                        created_servings += 1
                    except ValueError:
                        pass
            
            if created_servings > 0:
                messages.success(request, f"Dish created with {created_servings} serving options.")
            else:
                messages.warning(request, "Dish created but no serving sizes added. Please add at least one serving size.")
            return redirect('restaurant-dishes')
        else:
            messages.error(request, "Please provide a dish name.")
    
    from .models import Category
    categories = Category.objects.all().order_by('name')
    return render(request, 'restaurant/dish_form.html', {
        "restaurant": restaurant, 
        "mode": "Create",
        "categories": categories
    })


@_restaurant_required
@require_http_methods(["GET", "POST"])
def restaurant_dish_edit(request, pk: int):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    dish = get_object_or_404(Dish, pk=pk, restaurant=restaurant)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        
        if name:
            dish.name = name
            dish.description = description
            if image:
                dish.image = image
            dish.save()
            
            # Handle categories
            category_ids = request.POST.getlist('categories')
            dish.categories.set(category_ids)
            
            # Update serving sizes and prices
            from .models import DishServing
            serving_sizes = ['solo', 'sharing', 'family', 'party']
            
            for size in serving_sizes:
                price = request.POST.get(f'price_{size}', '').strip()
                serving = DishServing.objects.filter(dish=dish, serving_size=size).first()
                
                if price:
                    try:
                        price_val = float(price)
                        if serving:
                            serving.price = price_val
                            serving.save()
                        else:
                            DishServing.objects.create(
                                dish=dish,
                                serving_size=size,
                                price=price_val
                            )
                    except ValueError:
                        pass
                elif serving:
                    serving.delete()
            
            messages.success(request, "Dish updated successfully.")
            return redirect('restaurant-dishes')
        else:
            messages.error(request, "Please provide a dish name.")
    
    from .models import Category
    categories = Category.objects.all().order_by('name')
    return render(request, 'restaurant/dish_form.html', {
        "restaurant": restaurant, 
        "dish": dish, 
        "mode": "Edit",
        "categories": categories
    })


@_restaurant_required
@require_http_methods(["POST"])
def restaurant_dish_delete(request, pk: int):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    dish = get_object_or_404(Dish, pk=pk, restaurant=restaurant)
    dish.delete()
    messages.success(request, "Dish deleted successfully.")
    return redirect('restaurant-dishes')


@_restaurant_required
def restaurant_images(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    images = RestaurantImage.objects.filter(restaurant=restaurant).order_by('-id')
    return render(request, 'restaurant/images.html', {"restaurant": restaurant, "images": images})


@_restaurant_required
@require_http_methods(["GET", "POST"])
def restaurant_images_add(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        created = 0
        for f in files:
            RestaurantImage.objects.create(restaurant=restaurant, image=f)
            created += 1
        if created:
            messages.success(request, f"Uploaded {created} image(s) successfully.")
        else:
            messages.error(request, "Please choose image files to upload.")
        return redirect('restaurant-images')
    
    return render(request, 'restaurant/image_upload.html', {"restaurant": restaurant})


@_restaurant_required
@require_http_methods(["POST"])
def restaurant_image_delete(request, img_id: int):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    img = get_object_or_404(RestaurantImage, pk=img_id, restaurant=restaurant)
    img.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('restaurant-images')


# Restaurant approval views
@_admin_required
@require_http_methods(["POST"])
def admin_restaurant_approve(request, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    restaurant.is_approved = True
    restaurant.save()
    messages.success(request, f"{restaurant.name} has been approved.")
    return redirect('admin-dashboard')


@_admin_required
@require_http_methods(["POST"])
def admin_restaurant_reject(request, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    restaurant.is_approved = False
    restaurant.save()
    messages.warning(request, f"{restaurant.name} has been rejected.")
    return redirect('admin-dashboard')


@_admin_required
@require_http_methods(["POST"])
def admin_user_approve(request, pk: int):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.get_full_name() or user.username} has been approved.")
    return redirect('admin-dashboard')


@_admin_required
@require_http_methods(["POST"])
def admin_user_reject(request, pk: int):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.warning(request, "User account has been rejected and deleted.")
    return redirect('admin-dashboard')


@_admin_required
@require_http_methods(["POST"])
def admin_user_delete(request, pk: int):
    user = get_object_or_404(User, pk=pk)
    if user.pk == request.user.pk:
        messages.error(request, "Cannot delete your own account.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('admin-dashboard')


@_restaurant_required
def restaurant_menu_categories(request):
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        messages.error(request, "No restaurant associated with this account.")
        return redirect('main')
    
    dishes_by_category = {}
    dishes = Dish.objects.filter(restaurant=restaurant).prefetch_related('categories').order_by('name')
    
    for dish in dishes:
        categories = dish.categories.all()
        if categories:
            for category in categories:
                cat_name = category.name
                if cat_name not in dishes_by_category:
                    dishes_by_category[cat_name] = []
                dishes_by_category[cat_name].append(dish)
        else:
            if 'Uncategorized' not in dishes_by_category:
                dishes_by_category['Uncategorized'] = []
            dishes_by_category['Uncategorized'].append(dish)
    
    return render(request, 'restaurant/menu_categories.html', {
        "restaurant": restaurant,
        "dishes_by_category": dishes_by_category
    })


@_restaurant_required
@require_http_methods(["POST"])
def restaurant_update_location(request):
    import json
    profile = request.user.profile
    restaurant = profile.restaurant
    if not restaurant:
        return JsonResponse({'success': False})
    
    data = json.loads(request.body)
    restaurant.latitude = data['latitude']
    restaurant.longitude = data['longitude']
    restaurant.save()
    
    return JsonResponse({'success': True})


@_admin_required
@require_http_methods(["POST"])
def admin_about_update(request):
    from .models import AboutContent
    
    # Get or create AboutContent instance
    about_content, created = AboutContent.objects.get_or_create(pk=1)
    
    # Handle file uploads
    if 'logo' in request.FILES:
        about_content.logo = request.FILES['logo']
    if 'poster' in request.FILES:
        about_content.poster = request.FILES['poster']
    if 'video' in request.FILES:
        about_content.video = request.FILES['video']
    
    about_content.save()
    messages.success(request, "About content updated successfully.")
    return redirect('admin-dashboard')
