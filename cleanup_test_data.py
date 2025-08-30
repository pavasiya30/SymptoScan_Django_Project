#!/usr/bin/env python
"""
Script to clean up test data and keep only real user activity
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')
django.setup()

from django.contrib.auth.models import User
from ss_app.models import Prediction, Review, AIChatLog, Disease, UserProfile
from django.db import connection

def cleanup_test_data():
    """Remove all test/automatically generated data"""
    print("🧹 Starting database cleanup...")
    
    # 1. Remove test users (except admin)
    test_users = User.objects.filter(
        username__in=['testuser', 'demo_user', 'sample_user', 'user1', 'user2', 'user3']
    ).exclude(is_superuser=True)
    
    print(f"🗑️  Removing {test_users.count()} test users...")
    test_users.delete()
    
    # 2. Remove predictions from test users
    test_predictions = Prediction.objects.filter(
        user__username__in=['testuser', 'demo_user', 'sample_user', 'user1', 'user2', 'user3']
    )
    print(f"🗑️  Removing {test_predictions.count()} test predictions...")
    test_predictions.delete()
    
    # 3. Remove reviews from test users
    test_reviews = Review.objects.filter(
        user__username__in=['testuser', 'demo_user', 'sample_user', 'user1', 'user2', 'user3']
    )
    print(f"🗑️  Removing {test_reviews.count()} test reviews...")
    test_reviews.delete()
    
    # 4. Remove AI chat logs from test users
    test_chat_logs = AIChatLog.objects.filter(
        user__username__in=['testuser', 'demo_user', 'sample_user', 'user1', 'user2', 'user3']
    )
    print(f"🗑️  Removing {test_chat_logs.count()} test chat logs...")
    test_chat_logs.delete()
    
    # 5. Remove user profiles for deleted users
    orphaned_profiles = UserProfile.objects.filter(
        user__isnull=True
    )
    print(f"🗑️  Removing {orphaned_profiles.count()} orphaned user profiles...")
    orphaned_profiles.delete()
    
    # 6. Remove diseases that have no predictions or reviews
    diseases_with_activity = Disease.objects.filter(
        prediction__isnull=False
    ).distinct()
    
    diseases_without_activity = Disease.objects.exclude(
        id__in=diseases_with_activity
    )
    
    print(f"🗑️  Removing {diseases_without_activity.count()} diseases without activity...")
    diseases_without_activity.delete()
    
    # 7. Show final statistics
    print("\n📊 Final Database Statistics:")
    print(f"   Users: {User.objects.count()}")
    print(f"   Predictions: {Prediction.objects.count()}")
    print(f"   Reviews: {Review.objects.count()}")
    print(f"   AI Chat Logs: {AIChatLog.objects.count()}")
    print(f"   Diseases: {Disease.objects.count()}")
    
    # 8. Show remaining users
    remaining_users = User.objects.all()
    print(f"\n👥 Remaining Users:")
    for user in remaining_users:
        predictions_count = Prediction.objects.filter(user=user).count()
        reviews_count = Review.objects.filter(user=user).count()
        chat_logs_count = AIChatLog.objects.filter(user=user).count()
        
        print(f"   {user.username} ({user.email})")
        print(f"     - Predictions: {predictions_count}")
        print(f"     - Reviews: {reviews_count}")
        print(f"     - Chat Logs: {chat_logs_count}")
    
    print("\n✅ Database cleanup completed!")

if __name__ == '__main__':
    cleanup_test_data()
