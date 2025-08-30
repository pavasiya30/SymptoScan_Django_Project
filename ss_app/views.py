from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Disease, Prediction, Review, DiseaseFormField, RiskCategory, AIChatLog, UserProfile
from .forms import (DiabetesPredictionForm, HeartDiseasePredictionForm, HypertensionPredictionForm,
                   AsthmaPredictionForm, StrokePredictionForm, KidneyDiseasePredictionForm, ReviewForm, RiskForm,
                   DiseaseForm, DiseaseFormFieldForm, RiskCategoryForm, UserSuspensionForm,
                   ReviewModerationForm, AdminSearchForm, DateRangeForm)
from .ml_models import diabetes_predictor, heart_disease_predictor, hypertension_predictor, asthma_predictor, stroke_predictor, kidney_disease_predictor
from .api_utils import api_client
import json
import re
import io
import base64
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


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
    # Get recent reviews
    recent_reviews = Review.objects.select_related('user', 'disease').order_by('-created_at')[:6]
    # Get trending diseases
    trending_diseases = api_client.get_trending_diseases()
    
    context = {
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
        'kidney_disease': {
            'name': 'Kidney Disease',
            'description': (
                'Kidney disease, also known as chronic kidney disease (CKD), is a condition where the kidneys gradually lose their ability to filter waste and excess fluids from the blood. '
                'It is a serious condition that can lead to kidney failure if not properly managed. Early detection and treatment are crucial for preventing complications.'
            ),
            'symptoms': (
                'Common kidney disease symptoms include: Fatigue and weakness, Swelling in legs, ankles, or feet, '
                'Changes in urination (frequent urination, foamy urine, blood in urine), High blood pressure, '
                'Loss of appetite and nausea, Muscle cramps and twitches, Itching and dry skin, '
                'Shortness of breath, and Sleep problems.'
            ),
            'prevention': (
                'Control blood pressure and diabetes, Maintain a healthy diet low in salt and protein, '
                'Stay hydrated by drinking plenty of water, Exercise regularly and maintain a healthy weight, '
                'Avoid smoking and limit alcohol consumption, Get regular health checkups, '
                'Take medications as prescribed, and Monitor kidney function with regular tests.'
            ),
            'form_class': KidneyDiseasePredictionForm,
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
    elif disease_name == 'kidney_disease':
        form = KidneyDiseasePredictionForm(request.POST)
        if form.is_valid():
            # Convert categorical string values to integers
            hypertension_value = int(form.cleaned_data['hypertension'])
            diabetes_value = int(form.cleaned_data['diabetes'])
            
            risk_level, confidence = kidney_disease_predictor.predict(
                age=form.cleaned_data['age'],
                blood_pressure=form.cleaned_data['blood_pressure'],
                serum_creatinine=form.cleaned_data['serum_creatinine'],
                blood_urea=form.cleaned_data['blood_urea'],
                hemoglobin=form.cleaned_data['hemoglobin'],
                hypertension=hypertension_value,
                diabetes=diabetes_value
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

@login_required
def view_prediction_result(request, prediction_id):
    """View a specific prediction result"""
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Get the disease name for the template
    disease_name = prediction.disease.name.lower().replace(' ', '_')
    
    context = {
        'prediction': prediction,
        'risk_level': prediction.risk_level,
        'confidence': prediction.confidence_score,
        'disease_name': disease_name
    }
    
    return render(request, 'prediction_result.html', context)

def api_disease_stats(request, disease_name):
    """API endpoint for disease statistics"""
    stats = api_client.get_disease_stats(disease_name)
    return JsonResponse(stats)

def api_regional_data(request, disease_name, region):
    """API endpoint for regional disease data"""
    regional_data = api_client.get_regional_data(disease_name, region)
    return JsonResponse(regional_data)

def generate_wordcloud_data():
    """Generate word cloud data from all reviews"""
    # Get all review comments
    reviews = Review.objects.all()
    if not reviews:
        return None
    
    # Combine all comments
    all_text = ' '.join([review.comment for review in reviews if review.comment])
    
    if not all_text.strip():
        return None
    
    # Clean the text
    all_text = re.sub(r'[^\w\s]', '', all_text.lower())
    
    # Remove only basic stop words, keep medical and health-related terms
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs',
        'very', 'really', 'quite', 'just', 'only', 'also', 'too', 'as', 'so', 'than', 'more', 'most',
        'like', 'love', 'hate', 'dislike', 'enjoy', 'appreciate', 'value', 'trust', 'believe', 'think',
        'know', 'understand', 'see', 'look', 'watch', 'hear', 'listen', 'feel', 'touch', 'taste', 'smell',
        'say', 'tell', 'speak', 'talk', 'ask', 'answer', 'reply', 'respond', 'comment', 'mention',
        'get', 'give', 'take', 'put', 'set', 'place', 'move', 'go', 'come', 'arrive', 'leave', 'stay',
        'make', 'create', 'build', 'construct', 'form', 'shape', 'design', 'plan', 'prepare', 'ready',
        'use', 'utilize', 'apply', 'employ', 'practice', 'exercise', 'work', 'play', 'study', 'learn',
        'help', 'assist', 'support', 'aid', 'serve', 'provide', 'offer', 'give', 'present', 'show',
        'want', 'need', 'require', 'desire', 'wish', 'hope', 'expect', 'wait', 'try', 'attempt', 'effort',
        'find', 'discover', 'search', 'seek', 'look', 'find', 'locate', 'identify', 'recognize', 'notice',
        'start', 'begin', 'commence', 'initiate', 'launch', 'open', 'close', 'end', 'finish', 'complete',
        'continue', 'keep', 'maintain', 'preserve', 'save', 'store', 'hold', 'contain', 'include', 'involve',
        'change', 'modify', 'alter', 'adjust', 'adapt', 'transform', 'convert', 'turn', 'become', 'grow',
        'increase', 'decrease', 'rise', 'fall', 'grow', 'shrink', 'expand', 'contract', 'extend', 'reduce',
        'time', 'day', 'week', 'month', 'year', 'hour', 'minute', 'second', 'morning', 'afternoon', 'evening',
        'night', 'today', 'yesterday', 'tomorrow', 'now', 'then', 'before', 'after', 'during', 'while',
        'place', 'location', 'area', 'region', 'country', 'city', 'town', 'village', 'street', 'road',
        'way', 'path', 'direction', 'north', 'south', 'east', 'west', 'up', 'down', 'left', 'right',
        'thing', 'object', 'item', 'piece', 'part', 'section', 'portion', 'amount', 'quantity', 'number',
        'people', 'person', 'man', 'woman', 'boy', 'girl', 'child', 'adult', 'human', 'individual',
        'group', 'team', 'family', 'community', 'society', 'world', 'earth', 'planet', 'universe',
        'life', 'living', 'alive', 'dead', 'death', 'birth', 'born', 'die', 'live', 'survive',
        'food', 'eat', 'drink', 'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'hungry', 'thirsty',
        'water', 'milk', 'juice', 'coffee', 'tea', 'soda', 'alcohol', 'wine', 'beer', 'drink',
        'house', 'home', 'building', 'room', 'kitchen', 'bathroom', 'bedroom', 'living', 'dining',
        'car', 'vehicle', 'transport', 'travel', 'trip', 'journey', 'vacation', 'holiday', 'visit',
        'money', 'cash', 'dollar', 'cent', 'price', 'cost', 'expensive', 'cheap', 'free', 'buy', 'sell',
        'job', 'work', 'employment', 'career', 'profession', 'business', 'company', 'office', 'factory',
        'school', 'education', 'student', 'teacher', 'class', 'course', 'lesson', 'study', 'learn',
        'book', 'read', 'write', 'story', 'article', 'news', 'information', 'data', 'fact', 'truth',
        'music', 'song', 'dance', 'art', 'picture', 'photo', 'image', 'video', 'movie', 'film',
        'game', 'play', 'fun', 'enjoy', 'entertainment', 'hobby', 'interest', 'activity', 'sport',
        'computer', 'internet', 'website', 'app', 'software', 'program', 'code', 'technology',
        'phone', 'mobile', 'call', 'text', 'message', 'email', 'communication', 'contact',
        'weather', 'sunny', 'rainy', 'cloudy', 'hot', 'cold', 'warm', 'cool', 'temperature',
        'color', 'red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'brown', 'pink',
        'size', 'big', 'small', 'large', 'tiny', 'huge', 'enormous', 'giant', 'mini', 'micro',
        'shape', 'round', 'square', 'triangle', 'circle', 'rectangle', 'oval', 'flat', 'curved',
        'texture', 'smooth', 'rough', 'soft', 'hard', 'sharp', 'dull', 'wet', 'dry', 'sticky',
        'taste', 'sweet', 'sour', 'bitter', 'salty', 'spicy', 'delicious', 'tasty', 'yummy',
        'sound', 'loud', 'quiet', 'noisy', 'silent', 'music', 'noise', 'voice', 'speech',
        'light', 'bright', 'dark', 'shiny', 'dull', 'glowing', 'sparkling', 'twinkling',
        'speed', 'fast', 'slow', 'quick', 'rapid', 'gradual', 'sudden', 'immediate', 'instant',
        'strength', 'strong', 'weak', 'powerful', 'mighty', 'fragile', 'delicate', 'tough',
        'quantity', 'many', 'few', 'several', 'some', 'none', 'all', 'every', 'each', 'both',
        'frequency', 'always', 'never', 'sometimes', 'often', 'rarely', 'usually', 'occasionally',
        'probability', 'certain', 'possible', 'likely', 'unlikely', 'definite', 'maybe', 'perhaps',
        'comparison', 'same', 'different', 'similar', 'identical', 'unique', 'special', 'ordinary',
        'relationship', 'friend', 'family', 'love', 'hate', 'like', 'dislike', 'care', 'ignore',
        'emotion', 'happy', 'sad', 'angry', 'excited', 'worried', 'scared', 'surprised', 'confused',
        'thought', 'think', 'believe', 'know', 'understand', 'remember', 'forget', 'imagine', 'dream',
        'action', 'do', 'make', 'create', 'build', 'destroy', 'break', 'fix', 'repair', 'clean',
        'movement', 'walk', 'run', 'jump', 'climb', 'swim', 'fly', 'drive', 'ride', 'carry',
        'communication', 'say', 'tell', 'speak', 'talk', 'ask', 'answer', 'reply', 'respond',
        'sensation', 'see', 'hear', 'feel', 'touch', 'taste', 'smell', 'look', 'watch', 'listen'
    }
    
    # Split into words and filter
    words = [word for word in all_text.split() if word not in stop_words and len(word) > 2]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    return word_freq

def wordcloud_view(request):
    """Generate and display word cloud from reviews"""
    word_freq = generate_wordcloud_data()
    
    if not word_freq:
        messages.info(request, 'No reviews available to generate word cloud.')
        return redirect('home')
    
    # Create word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5
    ).generate_from_frequencies(word_freq)
    
    # Convert to image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)
    
    # Convert to base64
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    # Encode to base64
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    
    # Get some statistics
    total_reviews = Review.objects.count()
    total_words = sum(word_freq.values())
    unique_words = len(word_freq)
    top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10])
    
    context = {
        'wordcloud_image': image_base64,
        'total_reviews': total_reviews,
        'total_words': total_words,
        'unique_words': unique_words,
        'top_words': top_words,
    }
    
    return render(request, 'wordcloud.html', context)

def is_admin(user):
    """Check if user is the specific testadmin"""
    return user.is_authenticated and user.username == 'testadmin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin Dashboard Overview"""
    try:
        # Get statistics
        total_users = User.objects.count()
        total_predictions = Prediction.objects.count()
        total_diseases = Disease.objects.count()
        total_reviews = Review.objects.count()
        total_chat_logs = AIChatLog.objects.count()
        unique_conversations = AIChatLog.objects.values('conversation_id').distinct().count()
        
        # Recent activity
        recent_predictions = Prediction.objects.select_related('user', 'disease').order_by('-created_at')[:5]
        recent_reviews = Review.objects.select_related('user', 'disease').order_by('-created_at')[:5]
        recent_users = User.objects.order_by('-date_joined')[:5]
        recent_chat_logs = AIChatLog.objects.select_related('user', 'disease').order_by('-timestamp')[:5]
        
        # Chart data
        predictions_by_disease = Prediction.objects.values('disease__name').annotate(count=Count('id')).order_by('-count')[:5]
        reviews_by_rating = Review.objects.values('rating').annotate(count=Count('id')).order_by('rating')
        
        # Monthly trends
        current_month = timezone.now().month
        monthly_predictions = Prediction.objects.filter(created_at__month=current_month).count()
        monthly_users = User.objects.filter(date_joined__month=current_month).count()
        monthly_chat_logs = AIChatLog.objects.filter(timestamp__month=current_month).count()
        monthly_reviews = Review.objects.filter(created_at__month=current_month).count()
        
        context = {
            'total_users': total_users,
            'total_predictions': total_predictions,
            'total_diseases': total_diseases,
            'total_reviews': total_reviews,
            'total_chat_logs': total_chat_logs,
            'unique_conversations': unique_conversations,
            'recent_predictions': recent_predictions,
            'recent_reviews': recent_reviews,
            'recent_users': recent_users,
            'recent_chat_logs': recent_chat_logs,
            'predictions_by_disease': predictions_by_disease,
            'reviews_by_rating': reviews_by_rating,
            'monthly_predictions': monthly_predictions,
            'monthly_users': monthly_users,
            'monthly_chat_logs': monthly_chat_logs,
            'monthly_reviews': monthly_reviews,
        }
        
        return render(request, 'admin/dashboard.html', context)
    except Exception as e:
        # If there's an error, return a simple context
        context = {
            'total_users': 0,
            'total_predictions': 0,
            'total_diseases': 0,
            'total_reviews': 0,
            'total_chat_logs': 0,
            'unique_conversations': 0,
            'recent_predictions': [],
            'recent_reviews': [],
            'recent_users': [],
            'recent_chat_logs': [],
            'predictions_by_disease': [],
            'reviews_by_rating': [],
            'monthly_predictions': 0,
            'monthly_users': 0,
            'monthly_chat_logs': 0,
            'monthly_reviews': 0,
        }
        messages.error(request, f'Error loading dashboard data: {str(e)}')
        return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """User Management"""
    search_form = AdminSearchForm(request.GET)
    date_form = DateRangeForm(request.GET)
    
    users = User.objects.all()
    
    # Apply search filter
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
    
    # Apply date filter
    if date_form.is_valid():
        start_date = date_form.cleaned_data.get('start_date')
        end_date = date_form.cleaned_data.get('end_date')
        if start_date:
            users = users.filter(date_joined__gte=start_date)
        if end_date:
            users = users.filter(date_joined__lte=end_date)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    active_users_count = UserProfile.objects.filter(is_suspended=False).count()
    suspended_users_count = UserProfile.objects.filter(is_suspended=True).count()
    new_users_this_month = User.objects.filter(
        date_joined__month=timezone.now().month
    ).count()
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'date_form': date_form,
        'active_users_count': active_users_count,
        'suspended_users_count': suspended_users_count,
        'new_users_this_month': new_users_this_month,
    }
    
    return render(request, 'admin/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_detail(request, user_id):
    """User Detail View"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Get user's predictions
    predictions = Prediction.objects.filter(user=user).select_related('disease').order_by('-created_at')
    
    # Get user's reviews
    reviews = Review.objects.filter(user=user).select_related('disease').order_by('-created_at')
    
    # Get user's AI chat logs
    chat_logs = AIChatLog.objects.filter(user=user).order_by('-timestamp')
    
    # Suspension form
    if request.method == 'POST':
        suspension_form = UserSuspensionForm(request.POST, instance=profile)
        if suspension_form.is_valid():
            profile = suspension_form.save(commit=False)
            if profile.is_suspended:
                profile.suspension_date = timezone.now()
            else:
                profile.suspension_date = None
            profile.save()
            messages.success(request, f'User {user.username} suspension status updated.')
            return redirect('admin_user_detail', user_id=user_id)
    else:
        suspension_form = UserSuspensionForm(instance=profile)
    
    context = {
        'user_obj': user,
        'profile': profile,
        'predictions': predictions,
        'reviews': reviews,
        'chat_logs': chat_logs,
        'suspension_form': suspension_form,
    }
    
    return render(request, 'admin/user_detail.html', context)

@login_required
@user_passes_test(is_admin)
def admin_diseases(request):
    """Disease Management"""
    diseases = Disease.objects.all().order_by('-created_at')
    
    # Calculate statistics
    active_diseases_count = diseases.filter(is_active=True).count()
    diseases_with_models_count = diseases.filter(model_file__isnull=False).exclude(model_file='').count()
    total_predictions_count = Prediction.objects.count()
    
    context = {
        'diseases': diseases,
        'active_diseases_count': active_diseases_count,
        'diseases_with_models_count': diseases_with_models_count,
        'total_predictions_count': total_predictions_count,
    }
    
    return render(request, 'admin/diseases.html', context)

@login_required
@user_passes_test(is_admin)
def admin_disease_detail(request, disease_id):
    """Disease Detail Management"""
    disease = get_object_or_404(Disease, id=disease_id)
    
    # Get form fields
    form_fields = DiseaseFormField.objects.filter(disease=disease)
    
    # Get risk categories
    risk_categories = RiskCategory.objects.filter(disease=disease)
    
    # Get predictions for this disease
    predictions = Prediction.objects.filter(disease=disease).select_related('user').order_by('-created_at')
    
    # Get reviews for this disease
    reviews = Review.objects.filter(disease=disease).select_related('user').order_by('-created_at')
    
    context = {
        'disease': disease,
        'form_fields': form_fields,
        'risk_categories': risk_categories,
        'predictions': predictions,
        'reviews': reviews,
    }
    
    return render(request, 'admin/disease_detail.html', context)

@login_required
@user_passes_test(is_admin)
def admin_disease_edit(request, disease_id):
    """Edit Disease"""
    disease = get_object_or_404(Disease, id=disease_id)
    
    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES, instance=disease)
        if form.is_valid():
            form.save()
            messages.success(request, f'Disease "{disease.name}" updated successfully.')
            return redirect('admin_disease_detail', disease_id=disease_id)
    else:
        form = DiseaseForm(instance=disease)
    
    context = {
        'form': form,
        'disease': disease,
    }
    
    return render(request, 'admin/disease_edit.html', context)

@login_required
@user_passes_test(is_admin)
def admin_disease_delete(request, disease_id):
    """Delete Disease"""
    disease = get_object_or_404(Disease, id=disease_id)
    
    if request.method == 'POST':
        disease_name = disease.name
        disease.delete()
        messages.success(request, f'Disease "{disease_name}" deleted successfully.')
        return redirect('admin_diseases')
    
    context = {
        'disease': disease,
    }
    
    return render(request, 'admin/disease_delete.html', context)

@login_required
@user_passes_test(is_admin)
def admin_form_fields(request, disease_id):
    """Manage Disease Form Fields"""
    disease = get_object_or_404(Disease, id=disease_id)
    
    if request.method == 'POST':
        form = DiseaseFormFieldForm(request.POST)
        if form.is_valid():
            form_field = form.save(commit=False)
            form_field.disease = disease
            form_field.save()
            messages.success(request, 'Form field added successfully.')
            return redirect('admin_form_fields', disease_id=disease_id)
    else:
        form = DiseaseFormFieldForm()
    
    form_fields = DiseaseFormField.objects.filter(disease=disease).order_by('order')
    
    context = {
        'disease': disease,
        'form_fields': form_fields,
        'form': form,
    }
    
    return render(request, 'admin/form_fields.html', context)

@login_required
@user_passes_test(is_admin)
def admin_reviews(request):
    """Review Moderation"""
    search_form = AdminSearchForm(request.GET)
    date_form = DateRangeForm(request.GET)
    
    reviews = Review.objects.select_related('user', 'disease').all()
    
    # Apply filters
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        if search:
            reviews = reviews.filter(
                Q(user__username__icontains=search) |
                Q(disease__name__icontains=search) |
                Q(comment__icontains=search)
            )
    
    if date_form.is_valid():
        start_date = date_form.cleaned_data.get('start_date')
        end_date = date_form.cleaned_data.get('end_date')
        if start_date:
            reviews = reviews.filter(created_at__gte=start_date)
        if end_date:
            reviews = reviews.filter(created_at__lte=end_date)
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate average rating from all reviews
    if reviews.exists():
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / reviews.count()
    else:
        average_rating = 0
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'date_form': date_form,
        'average_rating': average_rating,
    }
    
    return render(request, 'admin/reviews.html', context)

@login_required
@user_passes_test(is_admin)
def admin_review_moderate(request, review_id):
    """Moderate Review"""
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        form = ReviewModerationForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review moderation status updated.')
            return redirect('admin_reviews')
    else:
        form = ReviewModerationForm(instance=review)
    
    context = {
        'review': review,
        'form': form,
    }
    
    return render(request, 'admin/review_moderate.html', context)

@login_required
@user_passes_test(is_admin)
def admin_chat_logs(request):
    """AI Chat Logs"""
    search_form = AdminSearchForm(request.GET)
    date_form = DateRangeForm(request.GET)
    
    chat_logs = AIChatLog.objects.select_related('user', 'disease').all()
    
    # Apply filters
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        if search:
            chat_logs = chat_logs.filter(
                Q(user__username__icontains=search) |
                Q(disease__name__icontains=search) |
                Q(message__icontains=search) |
                Q(response__icontains=search)
            )
    
    if date_form.is_valid():
        start_date = date_form.cleaned_data.get('start_date')
        end_date = date_form.cleaned_data.get('end_date')
        if start_date:
            chat_logs = chat_logs.filter(timestamp__gte=start_date)
        if end_date:
            chat_logs = chat_logs.filter(timestamp__lte=end_date)
    
    # Get statistics
    total_chat_logs = AIChatLog.objects.count()
    unique_users_count = AIChatLog.objects.values('user').distinct().count()
    disease_specific_count = AIChatLog.objects.filter(disease__isnull=False).count()
    today_conversations_count = AIChatLog.objects.filter(
        timestamp__date=timezone.now().date()
    ).values('conversation_id').distinct().count()
    
    # Calculate average response time (mock calculation for now)
    avg_response_time = "2.5"  # This would be calculated from actual data
    
    # User satisfaction (mock calculation)
    user_satisfaction = "85"  # This would be calculated from follow-up actions
    
    # Most common topic
    most_common_topic = "Symptoms & Prevention"
    
    # Pagination
    paginator = Paginator(chat_logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'date_form': date_form,
        'unique_users_count': unique_users_count,
        'disease_specific_count': disease_specific_count,
        'today_conversations_count': today_conversations_count,
        'avg_response_time': avg_response_time,
        'user_satisfaction': user_satisfaction,
        'most_common_topic': most_common_topic,
    }
    
    return render(request, 'admin/chat_logs.html', context)

@login_required
@user_passes_test(is_admin)
def admin_delete_chat_log(request, chat_log_id):
    """Delete a chat log"""
    if request.method == 'POST':
        try:
            chat_log = get_object_or_404(AIChatLog, id=chat_log_id)
            chat_log.delete()
            messages.success(request, 'Chat log has been deleted.')
        except Exception as e:
            messages.error(request, f'Error deleting chat log: {str(e)}')
    return redirect('admin_chat_logs')

def admin_test(request):
    """Simple test view to verify admin styling"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('loginaccount')
    
    context = {
        'total_users': User.objects.count(),
        'total_predictions': Prediction.objects.count(),
        'total_diseases': Disease.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    
    return render(request, 'admin/dashboard.html', context)



@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    """Delete a user"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            username = user.username
            user.delete()
            messages.success(request, f'User {username} has been deleted.')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
    return redirect('admin_users')

def admin_logout(request):
    """Admin logout - redirects to home page"""
    logout(request)
    messages.success(request, 'You have been logged out from admin panel.')
    return redirect('home')
