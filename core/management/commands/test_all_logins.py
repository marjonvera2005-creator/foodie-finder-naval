from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Test all account logins'

    def handle(self, *args, **options):
        accounts = [
            ('carlmarco19@gmail.com', 'carlTzy1902', 'Admin'),
            ('elpomar@restaurant.com', 'test123', 'Restaurant'),
            ('enjestkitchen@restaurant.com', 'test123', 'Restaurant'),
            ('manginasal@restaurant.com', 'test123', 'Restaurant'),
            ('big_cup\'s@gmail.com', 'test123', 'Restaurant'),
            ('testuser@example.com', 'test123', 'User'),
            ('jollibee@test.com', 'test123', 'User'),
        ]
        
        self.stdout.write(self.style.SUCCESS('=== LOGIN TEST RESULTS ==='))
        
        for email, password, role in accounts:
            user = authenticate(username=email, password=password)
            if user:
                status = "ACTIVE" if user.is_active else "INACTIVE"
                self.stdout.write(f'[OK] {email} / {password} ({role}) - {status}')
            else:
                self.stdout.write(f'[FAIL] {email} / {password} ({role}) - FAILED')
        
        self.stdout.write(self.style.SUCCESS('\n=== READY TO TEST ON WEBSITE ==='))