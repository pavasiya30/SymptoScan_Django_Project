from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Make a user a staff member for admin access'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to make staff')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully made "{username}" a staff member!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'User "{username}" can now access the admin dashboard at /admin-dashboard/')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist!')
            )
