from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ss_app.models import Disease, Prediction, Review
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Add sample reviews for testing word cloud functionality'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
        
        # Get or create diseases
        diseases_data = [
            {
                'name': 'Diabetes',
                'description': 'Diabetes is a group of metabolic disorders...',
                'symptoms': 'Frequent urination, Excessive thirst...',
                'prevention': 'Maintain a healthy weight, Stay physically active...'
            },
            {
                'name': 'Heart Disease',
                'description': 'Heart disease refers to several types of heart conditions...',
                'symptoms': 'Chest pain or discomfort, Upper back or neck pain...',
                'prevention': 'Eat a healthy diet, Maintain a healthy weight...'
            },
            {
                'name': 'Hypertension',
                'description': 'Hypertension, also known as high blood pressure...',
                'symptoms': 'Most people with high blood pressure have no symptoms...',
                'prevention': 'Maintain a healthy weight, Exercise regularly...'
            }
        ]
        
        diseases = []
        for disease_data in diseases_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults=disease_data
            )
            diseases.append(disease)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created disease: {disease.name}'))
        
        # Sample review comments
        sample_comments = [
            "This prediction system is incredibly accurate and helpful. The results were spot on with my actual diagnosis. Highly recommend for anyone concerned about their health.",
            "Great tool for initial health assessment. The interface is user-friendly and the predictions seem reliable. Will definitely use again.",
            "Excellent accuracy in predicting my risk level. The system provided detailed explanations and helpful recommendations. Very satisfied with the experience.",
            "The prediction was very accurate and the confidence score helped me understand the reliability. Great platform for health monitoring.",
            "Amazing tool! The prediction matched perfectly with my doctor's assessment. The detailed breakdown of risk factors was very informative.",
            "Very helpful system for understanding health risks. The predictions are accurate and the recommendations are practical. Highly recommend.",
            "Outstanding accuracy in risk assessment. The system is easy to use and provides comprehensive health insights. Excellent user experience.",
            "The prediction system is reliable and user-friendly. Results were consistent with my medical history. Great for regular health checks.",
            "Fantastic tool for health monitoring. Predictions are accurate and the interface is intuitive. Very satisfied with the results.",
            "Excellent prediction accuracy. The system provides valuable health insights and helpful recommendations. Highly recommend for everyone.",
            "Very accurate predictions and helpful recommendations. The system is easy to navigate and provides comprehensive health information.",
            "Great accuracy in risk assessment. The predictions are reliable and the platform is user-friendly. Excellent health monitoring tool.",
            "Outstanding prediction system with high accuracy. The results were very helpful and the recommendations were practical. Highly recommend.",
            "Excellent tool for health assessment. Predictions are accurate and the system provides valuable health insights. Great user experience.",
            "Very reliable prediction system. The accuracy is impressive and the recommendations are helpful. Excellent platform for health monitoring."
        ]
        
        # Create sample predictions and reviews
        for i, comment in enumerate(sample_comments):
            # Create a prediction
            prediction = Prediction.objects.create(
                user=user,
                disease=random.choice(diseases),
                symptoms_data={
                    'age': random.randint(25, 65),
                    'bmi': round(random.uniform(18.5, 35.0), 1),
                    'glucose': random.randint(80, 200),
                    'blood_pressure': random.randint(70, 140)
                },
                risk_level=random.choice(['low', 'medium', 'high']),
                confidence_score=round(random.uniform(75.0, 95.0), 1),
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
            )
            
            # Create a review
            review = Review.objects.create(
                user=user,
                disease=prediction.disease,
                prediction=prediction,
                rating=random.randint(4, 5),
                comment=comment,
                created_at=prediction.created_at
            )
            
            self.stdout.write(f'Created review {i+1}: {review.rating} stars for {review.disease.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(sample_comments)} sample reviews'))
        self.stdout.write(self.style.SUCCESS('You can now test the word cloud functionality at /wordcloud/'))
