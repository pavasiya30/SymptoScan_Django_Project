from django import forms
from .models import Review


class RiskForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=0)
    bp = forms.IntegerField(label="Blood Pressure")
    chol = forms.IntegerField(label="Cholesterol")

class DiabetesPredictionForm(forms.Form):
    glucose = forms.FloatField(
        label='Glucose Level (mg/dL)',
        min_value=0,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120'})
    )
    blood_pressure = forms.FloatField(
        label='Blood Pressure (mmHg)',
        min_value=0,
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 80'})
    )
    bmi = forms.FloatField(
        label='BMI (Body Mass Index)',
        min_value=10,
        max_value=50,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 25.5'})
    )
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 35'})
    )
    pregnancies = forms.IntegerField(
        label='Number of Pregnancies',
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2'})
    )
    insulin = forms.FloatField(
        label='Insulin Level',
        min_value=0,
        max_value=1000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 85'})
    )


class HeartDiseasePredictionForm(forms.Form):
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Sex',
        choices=[(1, 'Male'), (0, 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    chest_pain = forms.ChoiceField(
        label='Chest Pain Type',
        choices=[
            (0, 'Typical Angina'),
            (1, 'Atypical Angina'),
            (2, 'Non-anginal Pain'),
            (3, 'Asymptomatic')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    blood_pressure = forms.FloatField(
        label='Resting Blood Pressure',
        min_value=0,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    cholesterol = forms.FloatField(
        label='Cholesterol Level',
        min_value=0,
        max_value=600,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_heart_rate = forms.FloatField(
        label='Maximum Heart Rate',
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class HypertensionPredictionForm(forms.Form):
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bmi = forms.FloatField(
        label='BMI',
        min_value=10,
        max_value=50,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    currentSmoker = forms.ChoiceField(
        label='Smoking Status',
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sysBP = forms.FloatField(
        label='sysBP',
        # choices=[(1, 'Yes'), (0, 'No')],
        min_value=10,
        max_value=250,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    diaBP = forms.FloatField(
        label='diaBP',
        # choices=[(1, 'Yes'), (0, 'No')],
        min_value=10,
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    heartRate = forms.FloatField(
        label='heartRate',
        # choices=[(1, 'Yes'), (0, 'No')],
        min_value=10,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
from django import forms

class AsthmaPredictionForm(forms.Form):
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30'})
    )

    gender = forms.ChoiceField(
        label='Gender',
        choices=[('0', 'Female'), ('1', 'Male')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    shortness_of_breath = forms.ChoiceField(
        label='Shortness of Breath',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    coughing = forms.ChoiceField(
        label='Frequent Coughing',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    chest_tightness = forms.ChoiceField(
        label='Chest Tightness',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    wheezing = forms.ChoiceField(
        label='Wheezing',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    allergy_history = forms.ChoiceField(
        label='History of Allergies',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    
# forms.py

from django import forms

class StrokePredictionForm(forms.Form):
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 45'})
    )

    gender = forms.ChoiceField(
        label='Gender',
        choices=[('0', 'Female'), ('1', 'Male')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    hypertension = forms.ChoiceField(
        label='Hypertension (High BP)',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    heart_disease = forms.ChoiceField(
        label='Heart Disease',
        choices=[('0', 'No'), ('1', 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    avg_glucose_level = forms.FloatField(
        label='Average Glucose Level (mg/dL)',
        min_value=50,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 125.5'})
    )

    bmi = forms.FloatField(
        label='BMI (Body Mass Index)',
        min_value=10,
        max_value=60,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 27.3'})
    )

    smoking_status = forms.ChoiceField(
        label='Smoking Status',
        choices=[
            ('0', 'Never Smoked'),
            ('1', 'Formerly Smoked'),
            ('2', 'Currently Smokes'),
            ('3', 'Unknown')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
