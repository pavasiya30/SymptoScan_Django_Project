from django.contrib import admin
from .models import Disease, Prediction, Review

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'global_cases', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'disease', 'risk_level', 'confidence_score', 'created_at']
    list_filter = ['risk_level', 'disease', 'created_at']
    search_fields = ['user__username', 'disease__name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'disease', 'rating', 'created_at']
    list_filter = ['rating', 'disease', 'created_at']
    search_fields = ['user__username', 'disease__name']