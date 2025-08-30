from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from ss_app.models import Disease, Prediction, Review, AIChatLog
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Add sample data for admin dashboard'

    def handle(self, *args, **options):
        # Create sample diseases if they don't exist
        diseases_data = [
            {
                'name': 'Diabetes',
                'description': 'A metabolic disorder characterized by high blood sugar levels.',
                'symptoms': 'Frequent urination, Excessive thirst, Unexplained weight loss',
                'prevention': 'Maintain healthy weight, Exercise regularly, Eat balanced diet',
                'global_cases': 537000000,
                'deaths_per_year': 6700000,
                'prevalence': '6.7% of global population'
            },
            {
                'name': 'Heart Disease',
                'description': 'Various conditions affecting the heart and blood vessels.',
                'symptoms': 'Chest pain, Shortness of breath, Fatigue',
                'prevention': 'Quit smoking, Exercise regularly, Eat heart-healthy diet',
                'global_cases': 523000000,
                'deaths_per_year': 17900000,
                'prevalence': '6.5% of global population'
            },
            {
                'name': 'Hypertension',
                'description': 'High blood pressure affecting cardiovascular health.',
                'symptoms': 'Headaches, Dizziness, Chest pain',
                'prevention': 'Reduce salt intake, Exercise regularly, Manage stress',
                'global_cases': 1280000000,
                'deaths_per_year': 10400000,
                'prevalence': '16% of global population'
            },
            {
                'name': 'Asthma',
                'description': 'Chronic respiratory condition affecting airways.',
                'symptoms': 'Wheezing, Coughing, Shortness of breath',
                'prevention': 'Avoid triggers, Use inhalers, Regular checkups',
                'global_cases': 262000000,
                'deaths_per_year': 455000,
                'prevalence': '3.3% of global population'
            },
            {
                'name': 'Stroke',
                'description': 'Brain damage caused by interrupted blood supply.',
                'symptoms': 'Numbness, Confusion, Difficulty speaking',
                'prevention': 'Control blood pressure, Quit smoking, Exercise regularly',
                'global_cases': 101000000,
                'deaths_per_year': 6550000,
                'prevalence': '1.3% of global population'
            }
        ]

        for disease_data in diseases_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults=disease_data
            )
            if created:
                self.stdout.write(f'Created disease: {disease.name}')

        # Get existing users
        users = list(User.objects.all())
        diseases = list(Disease.objects.all())
        
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Please create users first.'))
            return

        # Create sample predictions
        predictions = []
        prediction_count = 0
        for i in range(25):  # Create 25 sample predictions
            user = random.choice(users)
            disease = random.choice(diseases)
            
            # Create random symptoms data
            symptoms_data = {
                'age': random.randint(25, 75),
                'blood_pressure': random.randint(90, 180),
                'bmi': round(random.uniform(18.5, 35), 1),
                'glucose': random.randint(70, 200),
                'cholesterol': random.randint(150, 300),
            }
            
            risk_levels = ['low', 'medium', 'high']
            risk_level = random.choice(risk_levels)
            confidence = random.randint(65, 95)
            
            # Create prediction with random date in last 30 days
            created_date = timezone.now() - timedelta(days=random.randint(0, 30))
            
            prediction = Prediction.objects.create(
                user=user,
                disease=disease,
                symptoms_data=symptoms_data,
                risk_level=risk_level,
                confidence_score=confidence,
                created_at=created_date
            )
            predictions.append(prediction)
            prediction_count += 1

        self.stdout.write(f'Created {prediction_count} sample predictions')

        # Create sample reviews (linked to predictions)
        review_count = 0
        for i in range(15):  # Create 15 sample reviews
            prediction = random.choice(predictions)
            
            review_texts = [
                "Great experience with the prediction tool! Very accurate results.",
                "The interface is user-friendly and easy to navigate.",
                "Found the recommendations very helpful for my health.",
                "Would recommend to others looking for health insights.",
                "The tool provided valuable information about my risk factors.",
                "Excellent service with detailed explanations.",
                "Very satisfied with the accuracy of predictions.",
                "The platform is intuitive and informative.",
                "Helpful for understanding my health better.",
                "Professional and reliable health assessment tool."
            ]
            
            rating = random.randint(3, 5)
            comment = random.choice(review_texts)
            
            # Create review with random date in last 30 days
            created_date = timezone.now() - timedelta(days=random.randint(0, 30))
            
            review = Review.objects.create(
                user=prediction.user,
                disease=prediction.disease,
                prediction=prediction,
                rating=rating,
                comment=comment,
                created_at=created_date
            )
            review_count += 1

        self.stdout.write(f'Created {review_count} sample reviews')

        # Create sample AI chat logs
        chat_count = 0
        for i in range(20):  # Create 20 sample chat logs
            user = random.choice(users)
            disease = random.choice(diseases) if random.choice([True, False]) else None
            
            messages = [
                "What are the symptoms of diabetes?",
                "How can I prevent heart disease?",
                "What causes high blood pressure?",
                "Is asthma hereditary?",
                "What are the warning signs of stroke?",
                "How often should I check my blood pressure?",
                "What foods should I avoid with hypertension?",
                "Can exercise help with asthma?",
                "What are the risk factors for diabetes?",
                "How is heart disease diagnosed?"
            ]
            
            responses = [
                "Diabetes symptoms include frequent urination, excessive thirst, and unexplained weight loss. It's important to consult a healthcare provider for proper diagnosis.",
                "To prevent heart disease, maintain a healthy diet, exercise regularly, quit smoking, and manage stress levels.",
                "High blood pressure can be caused by poor diet, lack of exercise, stress, and genetic factors.",
                "Asthma can have genetic components, but environmental factors also play a significant role.",
                "Stroke warning signs include sudden numbness, confusion, difficulty speaking, and severe headache."
            ]
            
            message = random.choice(messages)
            response = random.choice(responses)
            
            # Create chat log with random date in last 30 days
            created_date = timezone.now() - timedelta(days=random.randint(0, 30))
            
            chat_log = AIChatLog.objects.create(
                user=user,
                disease=disease,
                message=message,
                response=response,
                timestamp=created_date
            )
            chat_count += 1

        self.stdout.write(f'Created {chat_count} sample chat logs')

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample data for admin dashboard!')
        )
