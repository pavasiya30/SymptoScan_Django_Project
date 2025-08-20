import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/SymptoScan')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SymptoScan.settings')

# Setup Django
django.setup()

from Bio_app.models import Disease
from django.contrib.auth.models import User

def setup_diseases():
    """Create initial disease records"""
    diseases_data = [
        {
            'name': 'Diabetes',
            'description': 'Diabetes is a group of metabolic disorders characterized by a high blood sugar level over a prolonged period.',
            'symptoms': 'Frequent urination, Excessive thirst, Unexplained weight loss, Extreme hunger, Sudden vision changes, Tingling or numbness in hands or feet',
            'prevention': 'Maintain a healthy weight, Stay physically active, Eat a healthy diet, Limit refined carbohydrates and sugar',
            'global_cases': 537000000
        },
        {
            'name': 'Heart Disease',
            'description': 'Heart disease refers to several types of heart conditions. The most common type is coronary artery disease.',
            'symptoms': 'Chest pain or discomfort, Upper back or neck pain, Heartburn, Nausea or vomiting, Extreme fatigue',
            'prevention': 'Eat a healthy diet, Maintain a healthy weight, Get regular physical activity, Don\'t smoke, Limit alcohol use',
            'global_cases': 523000000
        },
        {
            'name': 'Hypertension',
            'description': 'Hypertension, also known as high blood pressure, is a long-term medical condition in which the blood pressure in the arteries is persistently elevated.',
            'symptoms': 'Most people with high blood pressure have no symptoms, Severe headaches, Chest pain, Dizziness, Difficulty breathing',
            'prevention': 'Maintain a healthy weight, Exercise regularly, Eat a healthy diet, Reduce sodium intake, Limit alcohol consumption',
            'global_cases': 1280000000
        },
        {
            'name': 'Asthma',
            'description': 'Asthma is a respiratory condition marked by attacks of spasm in the bronchi of the lungs, causing difficulty in breathing.',
            'symptoms': 'Shortness of breath, Chest tightness or pain, Wheezing when exhaling, Trouble sleeping caused by shortness of breath',
            'prevention': 'Identify and avoid asthma triggers, Get vaccinated for influenza and pneumonia, Monitor your breathing',
            'global_cases': 262000000
        },
        {
            'name': 'Cancer',
            'description': 'Cancer is a group of diseases involving abnormal cell growth with the potential to invade or spread to other parts of the body.',
            'symptoms': 'Unexplained weight loss, Fever, Fatigue, Pain, Skin changes, Change in bowel or bladder habits',
            'prevention': 'Don\'t use tobacco, Eat a healthy diet, Maintain a healthy weight, Be physically active, Protect yourself from the sun',
            'global_cases': 19300000
        },
        {
            'name': 'Stroke',
            'description': 'A stroke occurs when the blood supply to part of your brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients.',
            'symptoms': 'Sudden numbness or weakness in face, arm, or leg, Sudden confusion, trouble speaking, Sudden trouble seeing',
            'prevention': 'Control high blood pressure, Lower cholesterol, Don\'t smoke, Manage diabetes, Maintain a healthy weight',
            'global_cases': 101000000
        }
    ]
    
    for disease_data in diseases_data:
        disease, created = Disease.objects.get_or_create(
            name=disease_data['name'],
            defaults=disease_data
        )
        if created:
            print(f"Created disease: {disease.name}")
        else:
            print(f"Disease already exists: {disease.name}")

def create_admin_user():
    """Create admin user if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created admin user: admin/admin123")
    else:
        print("Admin user already exists")

if __name__ == '__main__':
    print("Setting up database...")
    setup_diseases()
    create_admin_user()
    print("Database setup complete!")
