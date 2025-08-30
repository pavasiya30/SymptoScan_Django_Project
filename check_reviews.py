#!/usr/bin/env python
"""
Script to check existing reviews and debug word cloud functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')
django.setup()

from ss_app.models import Review, User, Disease, Prediction
from ss_app.views import generate_wordcloud_data

def check_reviews():
    """Check existing reviews and debug word cloud"""
    print("🔍 Checking reviews in database...")
    
    # Check total reviews
    total_reviews = Review.objects.count()
    print(f"📊 Total reviews in database: {total_reviews}")
    
    if total_reviews == 0:
        print("❌ No reviews found in database")
        return
    
    # Show all reviews
    print("\n📝 All reviews:")
    reviews = Review.objects.select_related('user', 'disease').all()
    for i, review in enumerate(reviews, 1):
        print(f"  {i}. User: {review.user.username} | Disease: {review.disease.name} | Rating: {review.rating} | Comment: {review.comment[:50]}...")
    
    # Test word cloud generation
    print("\n🌤️ Testing word cloud generation...")
    word_freq = generate_wordcloud_data()
    
    if word_freq:
        print(f"✅ Word cloud data generated successfully!")
        print(f"📊 Total words: {sum(word_freq.values())}")
        print(f"📊 Unique words: {len(word_freq)}")
        print(f"🔝 Top 10 words: {dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10])}")
    else:
        print("❌ Word cloud data generation failed")
        
        # Debug the issue
        print("\n🔍 Debugging word cloud generation...")
        reviews = Review.objects.all()
        print(f"Reviews found: {reviews.count()}")
        
        if reviews.exists():
            # Check if comments are empty
            empty_comments = reviews.filter(comment__isnull=True).count()
            print(f"Reviews with null comments: {empty_comments}")
            
            # Check comments length
            for review in reviews[:5]:  # Check first 5 reviews
                print(f"Review {review.id}: Comment length = {len(review.comment) if review.comment else 0}")
                print(f"  Comment: '{review.comment}'")
        
        # Test with sample text
        print("\n🧪 Testing with sample text...")
        sample_text = "This is a test review for diabetes assessment. The system works great and provides accurate results."
        print(f"Sample text: {sample_text}")
        
        # Import the function and test manually
        import re
        from collections import Counter
        
        # Clean the text
        cleaned_text = re.sub(r'[^\w\s]', '', sample_text.lower())
        print(f"Cleaned text: {cleaned_text}")
        
        # Split into words
        words = cleaned_text.split()
        print(f"Words: {words}")
        
        # Count frequencies
        word_freq = Counter(words)
        print(f"Word frequencies: {word_freq}")

if __name__ == '__main__':
    check_reviews()
