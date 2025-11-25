from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Setup the complete approval system with working credentials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up approval system...'))
        
        # 1. Ensure admin is active
        admin_user = User.objects.filter(email='carlmarco19@gmail.com').first()
        if admin_user:
            admin_user.set_password('carlTzy1902')
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(f'[OK] Admin ready: {admin_user.email} / carlTzy1902')
        
        # 2. Set all non-admin users as inactive (pending approval)
        non_admin_users = User.objects.filter(is_superuser=False, is_staff=False)
        for user in non_admin_users:
            user.set_password('test123')
            user.is_active = False  # Needs approval
            user.save()
            
            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'role': 'user', 'contact_number': '09123456789'}
            )
            
            self.stdout.write(f'[PENDING] User: {user.email} / test123 ({profile.get_role_display()})')
        
        # 3. Create test users for approval testing
        test_users = [
            ('newuser@test.com', 'New', 'User', 'user'),
            ('newrestaurant@test.com', 'New', 'Restaurant', 'restaurant'),
        ]
        
        for email, first_name, last_name, role in test_users:
            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password='test123',
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False  # Needs approval
                )
                
                Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': role,
                        'contact_number': '09123456789'
                    }
                )
                
                self.stdout.write(f'[CREATED] Test {role}: {email} / test123')
        
        self.stdout.write(self.style.SUCCESS('\n=== APPROVAL SYSTEM READY ==='))
        self.stdout.write('1. Admin login: carlmarco19@gmail.com / carlTzy1902')
        self.stdout.write('2. Go to admin dashboard to approve users')
        self.stdout.write('3. After approval, users can login with test123')
        self.stdout.write('4. Users redirect to correct dashboard based on role')