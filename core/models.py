from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default="Naval Proper")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=11.5564)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=124.2595)
    open_time = models.TimeField()
    close_time = models.TimeField()
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    category = models.CharField(max_length=40, default="Fast Food")
    is_approved = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def is_open_now(self) -> bool:
        from django.utils import timezone
        now = timezone.localtime().time()
        # Simple same-day open/close window
        return self.open_time <= now <= self.close_time


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurants/gallery/')

    def __str__(self) -> str:
        return f"{self.restaurant.name} image"


class Dish(models.Model):
    name = models.CharField(max_length=120)
    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True, help_text="Select multiple categories for this dish")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.restaurant.name}"

    def get_min_price(self):
        serving = self.servings.first()
        return serving.price if serving else 0
    
    @property
    def price(self):
        return self.get_min_price()

    def is_affordable(self) -> bool:
        return self.get_min_price() <= 199

    def price_tier(self) -> str:
        p = float(self.get_min_price())
        if p <= 149:
            return '₱'
        if p <= 249:
            return '₱₱'
        return '₱₱₱'


class DishServing(models.Model):
    SERVING_CHOICES = [
        ('solo', 'Solo'),
        ('sharing', 'Sharing (2-3 pax)'),
        ('family', 'Family (4-6 pax)'),
        ('party', 'Party (8+ pax)'),
    ]
    
    dish = models.ForeignKey(Dish, related_name='servings', on_delete=models.CASCADE)
    serving_size = models.CharField(max_length=20, choices=SERVING_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        unique_together = ['dish', 'serving_size']
    
    def __str__(self):
        return f"{self.dish.name} - {self.get_serving_size_display()}: ₱{self.price}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('restaurant', 'Restaurant'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()}"


class AboutContent(models.Model):
    logo = models.ImageField(upload_to='about/', blank=True, null=True)
    poster = models.ImageField(upload_to='about/', blank=True, null=True)
    video = models.FileField(upload_to='about/', blank=True, null=True)
    
    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"
    
    def __str__(self):
        return "About Page Content"

# Create your models here.
