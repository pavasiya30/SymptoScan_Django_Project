#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        return
    
    # Create superuser with default credentials
    username = 'admin'
    email = 'admin@symptoscan.com'
    password = 'admin123'
    
    try:
        user = User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("\n🔗 You can now access the admin panel at: http://127.0.0.1:8000/admin/")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()

