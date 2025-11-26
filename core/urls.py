from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('create-accounts/', views.force_create_accounts, name='force-create-accounts'),
    path('create-restaurants/', views.create_restaurants_only, name='create-restaurants'),
    path('check-accounts/', views.check_accounts, name='check-accounts'),
    path('test-registration/', views.test_registration, name='test-registration'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main_view, name='main'),
    path('about/', views.about_view, name='about'),
    path('logo/', views.logo_view, name='logo-page'),
    path('poster/', views.poster_view, name='poster-page'),
    path('advertisement/', views.advertisement_view, name='advertisement-page'),
    path('suggest/', views.suggest_foods, name='suggest-foods'),
    path('search/', views.search_results, name='search-results'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant-detail'),
    # Admin dashboard (custom) - use 'console' prefix to avoid collision with Django admin
    path('console/', views.admin_dashboard, name='admin-dashboard'),
    path('console/logout/', views.admin_logout_view, name='admin-logout'),
    # Restaurant management
    path('console/restaurants/', views.admin_restaurant_list, name='admin-restaurant-list'),
    path('console/restaurants/new/', views.admin_restaurant_create, name='admin-restaurant-create'),
    path('console/restaurants/<int:pk>/edit/', views.admin_restaurant_edit, name='admin-restaurant-edit'),
    path('console/restaurants/<int:pk>/delete/', views.admin_restaurant_delete, name='admin-restaurant-delete'),
    path('console/restaurants/<int:resto_id>/images/', views.admin_restaurant_images, name='admin-restaurant-images'),
    path('console/restaurants/<int:resto_id>/images/add/', views.admin_restaurant_images_add, name='admin-restaurant-images-add'),
    path('console/images/<int:img_id>/delete/', views.admin_image_delete, name='admin-image-delete'),
    # Dish management
    path('console/dishes/', views.admin_dish_list, name='admin-dish-list'),
    path('console/dishes/new/', views.admin_dish_create, name='admin-dish-create'),
    path('console/dishes/<int:pk>/edit/', views.admin_dish_edit, name='admin-dish-edit'),
    path('console/dishes/<int:pk>/delete/', views.admin_dish_delete, name='admin-dish-delete'),
    
    # Restaurant Dashboard
    path('restaurant/', views.restaurant_dashboard, name='restaurant-dashboard'),
    path('restaurant/edit/', views.restaurant_edit, name='restaurant-edit'),
    path('restaurant/dishes/', views.restaurant_dishes, name='restaurant-dishes'),
    path('restaurant/dishes/new/', views.restaurant_dish_create, name='restaurant-dish-create'),
    path('restaurant/dishes/<int:pk>/edit/', views.restaurant_dish_edit, name='restaurant-dish-edit'),
    path('restaurant/dishes/<int:pk>/delete/', views.restaurant_dish_delete, name='restaurant-dish-delete'),
    path('restaurant/images/', views.restaurant_images, name='restaurant-images'),
    path('restaurant/images/add/', views.restaurant_images_add, name='restaurant-images-add'),
    path('restaurant/images/<int:img_id>/delete/', views.restaurant_image_delete, name='restaurant-image-delete'),
    path('restaurant/menu-categories/', views.restaurant_menu_categories, name='restaurant-menu-categories'),
    path('restaurant/update-location/', views.restaurant_update_location, name='restaurant-update-location'),
    
    # Restaurant approval
    path('console/restaurants/<int:pk>/approve/', views.admin_restaurant_approve, name='admin-restaurant-approve'),
    path('console/restaurants/<int:pk>/reject/', views.admin_restaurant_reject, name='admin-restaurant-reject'),
    
    # User approval
    path('console/users/<int:pk>/approve/', views.admin_user_approve, name='admin-user-approve'),
    path('console/users/<int:pk>/reject/', views.admin_user_reject, name='admin-user-reject'),
    path('console/users/<int:pk>/delete/', views.admin_user_delete, name='admin-user-delete'),
    
    # About content management
    path('console/about/update/', views.admin_about_update, name='admin-about-update'),
    
    # Restaurant full menu view
    path('restaurant/full-menu/', views.restaurant_full_menu, name='restaurant-full-menu'),
    
    # Debug view for testing images
    path('debug/images/', views.debug_images, name='debug-images'),
    
    # Test view to force cache refresh
    path('test/refresh/', views.test_refresh, name='test-refresh'),
    
    # All restaurant images view
    path('all-images/', views.all_restaurant_images, name='all-restaurant-images'),
]

