from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Disease, Prediction, Review
from .forms import DiabetesPredictionForm, HeartDiseasePredictionForm,HypertensionPredictionForm,AsthmaPredictionForm,StrokePredictionForm,ReviewForm
from .ml_models import diabetes_predictor,heart_disease_predictor,hypertension_predictor,asthma_predictor,stroke_predictor
from .api_utils import api_client
import json
from django.shortcuts import render
from .forms import RiskForm

def risk_check(request):
    prediction = None
    if request.method == "POST":
        form = RiskForm(request.POST)
        if form.is_valid():
            input_data = {
                'bp': form.cleaned_data['bp'],
                'age': form.cleaned_data['age'],
                'chol': form.cleaned_data['chol'],
            }
            prediction = predictor(input_data)
    else:
        form = RiskForm()

    return render(request, 'risk_check.html', {
        'form': form,
        'prediction': prediction
    })

def home(request):
    # Get disease statistics
    diseases_stats = api_client.get_all_disease_stats()
    
    # Get recent reviews
    recent_reviews = Review.objects.select_related('user', 'disease').order_by('-created_at')[:6]
    
    # Get trending diseases
    trending_diseases = api_client.get_trending_diseases()
    
    context = {
        'diseases_stats': diseases_stats,
        'recent_reviews': recent_reviews,
        'trending_diseases': trending_diseases,
        "star_range": range(5),
    }
    return render(request, 'home.html', context)

def disease_detail(request, disease_name):
    # Normalize disease name for lookup
    disease_name = disease_name.lower().strip()
    print(f"🔍 disease_name = '{disease_name}'")

    # ✅ CORRECT disease_info: dictionary only, no accidental set
    disease_info = {
        'diabetes': {
            'name': 'Diabetes',
            'description': (
                'Diabetes is a group of metabolic disorders characterized by '
                'a high blood sugar level over a prolonged period. It occurs '
                'when the pancreas does not produce enough insulin or when '
                'the body cannot effectively use the insulin it produces. '
                'There are three main types: Type 1, Type 2, and gestational diabetes.'
            ),
            'symptoms': (
                'Frequent urination, Excessive thirst, Unexplained weight loss, '
                'Extreme hunger, Sudden vision changes, Tingling or numbness in hands or feet, '
                'Feeling very tired much of the time, Very dry skin, Sores that are slow to heal, '
                'More infections than usual'
            ),
            'prevention': (
                'Maintain a healthy weight, Stay physically active, Eat a healthy diet, '
                'Limit refined carbohydrates and sugar, Quit smoking, Watch portion sizes, '
                'Make healthy food choices, Get regular health screenings'
            ),
            'form_class': DiabetesPredictionForm,
        },
        'heart_disease': {
            'name': 'Heart Disease',
            'description': (
                'Heart disease refers to several types of heart conditions. The most common '
                'type is coronary artery disease, which affects blood flow to the heart. '
                'It is one of the leading causes of death worldwide and includes conditions '
                'like heart attacks, heart failure, and arrhythmias.'
            ),
            'symptoms': (
                'Chest pain or discomfort, Upper back or neck pain, Heartburn, '
                'Nausea or vomiting, Extreme fatigue, Upper body discomfort, Dizziness, '
                'Shortness of breath, Irregular heartbeat, Swelling in legs or feet'
            ),
            'prevention': (
                'Eat a healthy diet, Maintain a healthy weight, Get regular physical activity, '
                'Don\'t smoke, Limit alcohol use, Get enough sleep, Manage stress, '
                'Get regular health screenings, Control blood pressure and cholesterol'
            ),
            'form_class': HeartDiseasePredictionForm,
        },
        'hypertension': {
            'name': 'Hypertension',
            'description': (
                'Hypertension, also known as high blood pressure, is a long-term medical '
                'condition in which the blood pressure in the arteries is persistently elevated. '
                'It is a major risk factor for cardiovascular disease, stroke, and kidney disease. '
                'Often called the "silent killer" because it usually has no symptoms.'
            ),
            'symptoms': (
                'Most people with high blood pressure have no symptoms, Very high blood pressure may cause: '
                'Severe headaches, Chest pain, Dizziness, Difficulty breathing, Nausea, Vomiting, '
                'Blurred vision, Anxiety, Confusion, Buzzing in ears, Nosebleeds, Abnormal heart rhythm'
            ),
            'prevention': (
                'Maintain a healthy weight, Exercise regularly, Eat a healthy diet, '
                'Reduce sodium intake, Limit alcohol consumption, Don\'t smoke, Get enough sleep, '
                'Manage stress, Monitor blood pressure regularly, Take prescribed medications'
            ),
            'form_class': HypertensionPredictionForm,
        },
        'asthma': {
            'name': 'Asthma',
            'description': (
               'Asthma is a chronic condition that affects the airways in the lungs, causing them to become inflamed and narrow. '
               'This makes it difficult to breathe and can lead to coughing, wheezing, chest tightness, and shortness of breath. '
               'Asthma can be triggered by allergens, exercise, cold air, or stress, and it can range from mild to life-threatening.'
            ),
            'symptoms': (
               'Common asthma symptoms include: Shortness of breath, Chest tightness or pain, Wheezing when exhaling, '
               'Trouble sleeping caused by breathing issues, Coughing or wheezing attacks worsened by respiratory viruses (e.g., cold or flu). '
               'Symptoms can vary from person to person and may worsen with physical activity or at night.'
            ),
            'prevention': (
                'Identify and avoid asthma triggers (such as pollen, dust mites, mold, pet dander), '
                'Follow your asthma action plan, Take medications as prescribed (inhalers, steroids), '
                'Monitor breathing and use a peak flow meter, Get regular medical checkups, '
                'Stay up to date with vaccines (flu, pneumonia), Manage stress and anxiety, '
                'Maintain good indoor air quality, Exercise with caution under doctor’s advice.'
            ),
            'form_class': AsthmaPredictionForm,
        },
        'stroke': {
            'name': 'Stroke',
            'description': (
                'A stroke occurs when the blood supply to part of the brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients. '
                'Brain cells begin to die within minutes, making it a medical emergency. Immediate treatment is crucial to minimize brain damage and complications.'
            ),
            'symptoms': (
                'Common stroke symptoms include: Sudden numbness or weakness in the face, arm, or leg (especially on one side of the body), '
                'Confusion, trouble speaking, or understanding speech, Sudden trouble seeing in one or both eyes, '
                'Sudden trouble walking, dizziness, loss of balance or coordination, and Severe headache with no known cause. '
                'Recognize stroke with the acronym FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency services.'
            ),
            'prevention': (
                'Control high blood pressure (hypertension), Manage diabetes, Avoid smoking and limit alcohol, '
                'Eat a healthy diet rich in fruits, vegetables, and whole grains, Exercise regularly and maintain a healthy weight, '
                'Take medications as prescribed (especially blood thinners or cholesterol-lowering drugs), '
                'Monitor heart conditions such as atrial fibrillation, and Get regular health screenings to detect risk factors early.'
            ),
            'form_class': StrokePredictionForm,
        },


        # Add others like asthma, cancer, stroke if needed...
    }

    # ✅ Validate
    if disease_name not in disease_info:
        messages.error(request, 'Disease not found.')
        return redirect('home')

    disease_data = disease_info[disease_name]
    stats = api_client.get_disease_stats(disease_name)
    regional_data = api_client.get_regional_data(disease_name)
    symptoms = disease_data['symptoms'].split(',')
    prevention_list=disease_data['prevention'].split(',')

    # Get or create Disease in DB
    disease_obj, created = Disease.objects.get_or_create(
        name=disease_data['name'],
        defaults={
            'description': disease_data['description'],
            'symptoms': disease_data['symptoms'],
            'prevention': disease_data['prevention'],
            'global_cases': stats['global_cases'],
        },
    )

    # Recent reviews
    reviews = Review.objects.filter(disease=disease_obj).select_related('user').order_by('-created_at')[:10]
    avg_rating = 0
    if reviews:
        total_rating = sum([r.rating for r in reviews])
        avg_rating = round(total_rating / len(reviews), 1)

    context = {
        'disease': disease_data,
        'symptoms': symptoms,
        'disease_obj': disease_obj,
        'stats': stats,
        'regional_data': regional_data,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'disease_name': disease_name,
        'prevention_list': prevention_list,
        'form': disease_data['form_class']() if disease_data['form_class'] else None,
    }

    return render(request, 'disease_detail.html', context)

@login_required
def predict_disease(request, disease_name):
    """Handle disease prediction"""
    disease_obj = get_object_or_404(Disease, name__icontains=disease_name.replace('_', ' '))

    if request.method != 'POST':
        return redirect('disease_detail', disease_name=disease_name)

    if disease_name == 'diabetes':
        form = DiabetesPredictionForm(request.POST)
        if form.is_valid():
            # ✅ Use correct predictor instance
            risk_level, confidence = diabetes_predictor.predict(
                glucose=form.cleaned_data['glucose'],
                blood_pressure=form.cleaned_data['blood_pressure'],
                bmi=form.cleaned_data['bmi'],
                age=form.cleaned_data['age'],
                pregnancies=form.cleaned_data['pregnancies'],
                insulin=form.cleaned_data['insulin']
            )

            prediction = Prediction.objects.create(
                user=request.user,
                disease=disease_obj,
                symptoms_data=form.cleaned_data,
                risk_level=risk_level.lower(),
                confidence_score=confidence
            )

            return render(request, 'prediction_result.html', {
                'prediction': prediction,
                'risk_level': risk_level,
                'confidence': confidence,
                'disease_name': disease_name
            })

    elif disease_name == 'heart_disease':
        form = HeartDiseasePredictionForm(request.POST)
        if form.is_valid():
            risk_level, confidence = heart_disease_predictor.predict(
                age=form.cleaned_data['age'],
                sex=form.cleaned_data['sex'],
                chest_pain=form.cleaned_data['chest_pain'],
                blood_pressure=form.cleaned_data['blood_pressure'],
                cholesterol=form.cleaned_data['cholesterol'],
                max_heart_rate=form.cleaned_data['max_heart_rate']
            )

            prediction = Prediction.objects.create(
                user=request.user,
                disease=disease_obj,
                symptoms_data=form.cleaned_data,
                risk_level=risk_level.lower(),
                confidence_score=confidence
            )

            return render(request, 'prediction_result.html', {
                'prediction': prediction,
                'risk_level': risk_level,
                'confidence': confidence,
                'disease_name': disease_name
            })

    elif disease_name == 'hypertension':
        form = HypertensionPredictionForm(request.POST)
        if form.is_valid():
            risk_level, confidence = hypertension_predictor.predict(
                age=form.cleaned_data['age'],
                bmi=form.cleaned_data['bmi'],
                current_smoker=form.cleaned_data['currentSmoker'],
                sys_bp=form.cleaned_data['sysBP'],
                dia_bp=form.cleaned_data['diaBP'],
                heart_rate=form.cleaned_data['heartRate']
            )
            # current_smoker, sys_bp, dia_bp, heart_rate
            prediction = Prediction.objects.create(
                user=request.user,
                disease=disease_obj,
                symptoms_data=form.cleaned_data,
                risk_level=risk_level,
                confidence_score=confidence
            )

            return render(request, 'prediction_result.html', {
                'prediction': prediction,
                'risk_level': risk_level,
                'confidence': confidence,
                'disease_name': disease_name
            })

    elif disease_name == 'asthma':
        form = AsthmaPredictionForm(request.POST)
        if form.is_valid():
            risk_level, confidence = asthma_predictor.predict(
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                shortness_of_breath=form.cleaned_data['shortness_of_breath'],
                coughing=form.cleaned_data['coughing'],
                chest_tightness=form.cleaned_data['chest_tightness'],
                wheezing=form.cleaned_data['wheezing'],
                allergy_history=form.cleaned_data['allergy_history']
        )

            prediction = Prediction.objects.create(
                user=request.user,
                disease=disease_obj,
                symptoms_data=form.cleaned_data,
                risk_level=risk_level.lower(),
                confidence_score=confidence
        )

        return render(request, 'prediction_result.html', {
            'prediction': prediction,
            'risk_level': risk_level,
            'confidence': confidence,
            'disease_name': disease_name
        })
    elif disease_name == 'stroke':
        form = StrokePredictionForm(request.POST)
        if form.is_valid():
            risk_level, confidence = stroke_predictor.predict(
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                hypertension=form.cleaned_data['hypertension'],
                heart_disease=form.cleaned_data['heart_disease'],
                avg_glucose_level=form.cleaned_data['avg_glucose_level'],
                bmi=form.cleaned_data['bmi'],
                smoking_status=form.cleaned_data['smoking_status']
        )

            prediction = Prediction.objects.create(
                user=request.user,
                disease=disease_obj,
                symptoms_data=form.cleaned_data,
                risk_level=risk_level.lower(),
                confidence_score=confidence
        )

        return render(request, 'prediction_result.html', {
            'prediction': prediction,
            'risk_level': risk_level,
            'confidence': confidence,
            'disease_name': disease_name
        })


    messages.error(request, 'Invalid form data.')
    return redirect('disease_detail', disease_name=disease_name)

@login_required
def add_review(request, prediction_id):
    """Add a review for a prediction"""
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Check if user already reviewed this prediction
    existing_review = Review.objects.filter(prediction=prediction, user=request.user).first()
    if existing_review:
        messages.info(request, 'You have already reviewed this prediction. You can edit your existing review.')
        return redirect('edit_review', review_id=existing_review.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.disease = prediction.disease
            review.prediction = prediction
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('disease_detail', disease_name=prediction.disease.name.lower().replace(' ', '_'))
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {
        'form': form,
        'prediction': prediction
    })

@login_required
def edit_review(request, review_id):
    """Edit a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('disease_detail', disease_name=review.disease.name.lower().replace(' ', '_'))
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    disease_name = review.disease.name.lower().replace(' ', '_')
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('disease_detail', disease_name=disease_name)

@login_required
def user_predictions(request):
    """Display user's prediction history"""
    predictions = Prediction.objects.filter(user=request.user).select_related('disease').order_by('-created_at')
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_predictions = predictions.count()
    risk_distribution = {
        'low': predictions.filter(risk_level='low').count(),
        'medium': predictions.filter(risk_level='medium').count(),
        'high': predictions.filter(risk_level='high').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'total_predictions': total_predictions,
        'risk_distribution': risk_distribution,
    }
    
    return render(request, 'user_predictions.html', context)

def api_disease_stats(request, disease_name):
    """API endpoint for disease statistics"""
    stats = api_client.get_disease_stats(disease_name)
    return JsonResponse(stats)

def api_regional_data(request, disease_name, region):
    """API endpoint for regional disease data"""
    regional_data = api_client.get_regional_data(disease_name, region)
    return JsonResponse(regional_data)
