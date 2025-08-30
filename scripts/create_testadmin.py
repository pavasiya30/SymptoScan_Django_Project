import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/SymptoScan')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_testadmin():
    """Create testadmin user if it doesn't exist"""
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_superuser('testadmin', 'testadmin@example.com', 'testadmin123')
        print("✅ Created testadmin user: testadmin/testadmin123")
        print("🔑 Username: testadmin")
        print("🔑 Password: testadmin123")
        print("🔑 Email: testadmin@example.com")
    else:
        print("⚠️ testadmin user already exists")
        
        # Update password if needed
        user = User.objects.get(username='testadmin')
        user.set_password('testadmin123')
        user.save()
        print("✅ Updated testadmin password to: testadmin123")

if __name__ == '__main__':
    print("Creating testadmin user...")
    create_testadmin()
    print("✅ Setup complete!")
