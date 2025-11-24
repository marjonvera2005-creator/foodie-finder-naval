from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant


class Command(BaseCommand):
    help = 'Setup user roles and sample data'

    def handle(self, *args, **options):
        # Create admin user if not exists
        admin_email = 'admin@foodiefinder.com'
        if not User.objects.filter(username=admin_email).exists():
            admin = User.objects.create_user(
                username=admin_email,
                email=admin_email,
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            profile, created = Profile.objects.get_or_create(user=admin)
            profile.role = 'admin'
            profile.contact_number = '09123456789'
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_email}'))

        # Create restaurant user if not exists
        resto_email = 'jollibee@foodiefinder.com'
        if not User.objects.filter(username=resto_email).exists():
            resto_user = User.objects.create_user(
                username=resto_email,
                email=resto_email,
                password='resto123',
                first_name='Jollibee',
                last_name='Manager',
                is_active=True
            )
            profile, created = Profile.objects.get_or_create(user=resto_user)
            profile.role = 'restaurant'
            profile.contact_number = '09987654321'
            
            # Create restaurant
            restaurant = Restaurant.objects.create(
                name='Jollibee Naval',
                location='Naval Proper, Biliran',
                open_time='06:00',
                close_time='22:00',
                category='Fast Food',
                description='The home of the world-famous Chickenjoy and other Filipino favorites.',
                featured=True
            )
            profile.restaurant = restaurant
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created restaurant user: {resto_email}'))

        # Create regular user if not exists
        user_email = 'user@foodiefinder.com'
        if not User.objects.filter(username=user_email).exists():
            regular_user = User.objects.create_user(
                username=user_email,
                email=user_email,
                password='user123',
                first_name='John',
                last_name='Doe',
                is_active=True
            )
            profile, created = Profile.objects.get_or_create(user=regular_user)
            profile.role = 'user'
            profile.contact_number = '09111222333'
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created regular user: {user_email}'))

        self.stdout.write(self.style.SUCCESS('Setup completed successfully!'))
        self.stdout.write('Test accounts:')
        self.stdout.write(f'  Admin: {admin_email} / admin123')
        self.stdout.write(f'  Restaurant: {resto_email} / resto123')
        self.stdout.write(f'  User: {user_email} / user123')