from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a test user for the admin dashboard'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='testuser', help='Username for the test user')
        parser.add_argument('--email', type=str, default='test@example.com', help='Email for the test user')
        parser.add_argument('--password', type=str, default='testpass123', help='Password for the test user')
        parser.add_argument('--staff', action='store_true', help='Make user staff member')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        is_staff = options['staff']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Use a different username.')
            )
            return

        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_staff=is_staff,
            first_name='Test',
            last_name='User'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user "{username}" with password "{password}"')
        )
        
        if is_staff:
            self.stdout.write(
                self.style.SUCCESS(f'User "{username}" has staff privileges and can access admin dashboard')
            )
