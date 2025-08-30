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

def check_superusers():
    superusers = User.objects.filter(is_superuser=True)
    
    if superusers.exists():
        print("🔍 Existing Superusers:")
        for user in superusers:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Active: {user.is_active}")
            print("---")
    else:
        print("❌ No superusers found!")

if __name__ == '__main__':
    check_superusers()

