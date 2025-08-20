from django.test import TestCase
from django.contrib.auth.models import User
from .models import Disease, Prediction, Review
from ....princy.SymptoScan.Bio_app.ml_models import predictor

class DiseaseModelTest(TestCase):
    def setUp(self):
        self.disease = Disease.objects.create(
            name="Test Disease",
            description="Test description",
            symptoms="Test symptoms",
            prevention="Test prevention",
            global_cases=1000000
        )
    
    def test_disease_creation(self):
        self.assertEqual(self.disease.name, "Test Disease")
        self.assertEqual(self.disease.global_cases, 1000000)

class PredictionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.disease = Disease.objects.create(
            name="Diabetes",
            description="Test description",
            symptoms="Test symptoms",
            prevention="Test prevention"
        )
    
    def test_prediction_creation(self):
        prediction = Prediction.objects.create(
            user=self.user,
            disease=self.disease,
            symptoms_data={'age': 45, 'glucose': 120},
            risk_level='medium',
            confidence_score=85.5
        )
        self.assertEqual(prediction.risk_level, 'medium')
        self.assertEqual(prediction.confidence_score, 85.5)

class MLModelTest(TestCase):
    def test_diabetes_prediction(self):
        risk_level, confidence = predictor.predict_diabetes(
            age=45,
            glucose=140,
            blood_pressure=90,
            bmi=28,
            insulin=120,
            family_history=True
        )
        self.assertIn(risk_level, ['Low', 'Medium', 'High'])
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
    
    def test_heart_disease_prediction(self):
        risk_level, confidence = predictor.predict_heart_disease(
            age=55,
            chest_pain=2,
            blood_pressure=140,
            cholesterol=250,
            heart_rate=150,
            exercise_angina=True
        )
        self.assertIn(risk_level, ['Low', 'Medium', 'High'])
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
