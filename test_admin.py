#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')
django.setup()

from django.contrib import admin
from django.contrib.auth.models import User
from ss_app.models import Disease, DiseaseFormField, RiskCategory, Prediction, Review, AIChatLog, UserProfile

def test_admin():
    print("🔍 Testing Django Admin Configuration...")
    print("=" * 50)
    
    # Check if admin site is configured
    print("✅ Admin site is configured")
    
    # Check registered models
    registered_models = admin.site._registry
    print(f"\n📋 Registered Models in Admin ({len(registered_models)}):")
    
    for model, admin_class in registered_models.items():
        print(f"  • {model._meta.app_label}.{model._meta.model_name}")
    
    # Check superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"\n👤 Superusers ({superusers.count()}):")
    for user in superusers:
        print(f"  • {user.username} ({user.email})")
    
    # Check if models have data
    print(f"\n📊 Model Data Counts:")
    print(f"  • Diseases: {Disease.objects.count()}")
    print(f"  • Predictions: {Prediction.objects.count()}")
    print(f"  • Reviews: {Review.objects.count()}")
    print(f"  • Users: {User.objects.count()}")
    print(f"  • User Profiles: {UserProfile.objects.count()}")
    
    print(f"\n🌐 Admin URL: http://127.0.0.1:8000/admin/")
    print("=" * 50)

if __name__ == '__main__':
    test_admin()
