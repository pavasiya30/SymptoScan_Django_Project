from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    bmi = models.FloatField()

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()
    prevention = models.TextField()
    global_cases = models.IntegerField(default=0)
    deaths_per_year = models.IntegerField(default=0)
    prevalence = models.CharField(max_length=50, default="Unknown")
    csv_file = models.FileField(upload_to='disease_data/', null=True, blank=True)
    model_file = models.FileField(upload_to='ml_models/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_url_name(self):
        """Get the URL-friendly name for the disease"""
        return self.name.lower().replace(' ', '_')
    
    class Admin(admin.ModelAdmin):
        list_display = ['name', 'global_cases', 'is_active', 'created_at']
        search_fields = ['name']
        list_filter = ['is_active', 'created_at']
        readonly_fields = ['created_at', 'updated_at']

class DiseaseFormField(models.Model):
    FIELD_TYPES = [
        ('number', 'Number'),
        ('text', 'Text'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
    ]
    
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='form_fields')
    field_name = models.CharField(max_length=100)
    field_label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    validation_rules = models.JSONField(null=True, blank=True)
    options = models.JSONField(null=True, blank=True)  # For dropdown/radio fields
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.disease.name} - {self.field_label}"
    
    class Admin(admin.ModelAdmin):
        list_display = ['disease', 'field_label', 'field_type', 'required', 'order']
        list_filter = ['field_type', 'required', 'disease']
        search_fields = ['field_label', 'disease__name']
        ordering = ['disease', 'order']

class RiskCategory(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='risk_categories')
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ])
    tips = models.TextField()
    
    def __str__(self):
        return f"{self.disease.name} - {self.risk_level}"
    
    class Admin(admin.ModelAdmin):
        list_display = ['disease', 'risk_level']
        list_filter = ['risk_level', 'disease']
        search_fields = ['disease__name']

class Prediction(models.Model):
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptoms_data = models.JSONField()
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.disease.name} - {self.risk_level}"
    
    class Admin(admin.ModelAdmin):
        list_display = ['user', 'disease', 'risk_level', 'confidence_score', 'created_at']
        list_filter = ['risk_level', 'disease', 'created_at']
        search_fields = ['user__username', 'disease__name']
        readonly_fields = ['created_at']

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.disease.name} - {self.rating} stars"
    
    class Admin(admin.ModelAdmin):
        list_display = ['user', 'disease', 'rating', 'is_approved', 'created_at']
        list_filter = ['rating', 'disease', 'is_approved', 'created_at']
        search_fields = ['user__username', 'disease__name', 'comment']
        readonly_fields = ['created_at', 'updated_at']

class AIChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, null=True, blank=True)
    conversation_id = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    is_user_message = models.BooleanField(default=True)  # True for user, False for AI
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.disease.name if self.disease else 'General'} - {self.timestamp}"
    
    class Meta:
        ordering = ['timestamp']
    
    class Admin(admin.ModelAdmin):
        list_display = ['user', 'disease', 'prediction', 'is_user_message', 'timestamp']
        list_filter = ['disease', 'is_user_message', 'timestamp']
        search_fields = ['user__username', 'message', 'response']
        readonly_fields = ['timestamp']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True)
    suspension_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    class Admin(admin.ModelAdmin):
        list_display = ['user', 'is_suspended', 'suspension_date', 'created_at']
        list_filter = ['is_suspended', 'created_at']
        search_fields = ['user__username', 'user__email']
        readonly_fields = ['created_at']

# Register all models with admin
admin.site.register(Disease, Disease.Admin)
admin.site.register(DiseaseFormField, DiseaseFormField.Admin)
admin.site.register(RiskCategory, RiskCategory.Admin)
admin.site.register(Prediction, Prediction.Admin)
admin.site.register(Review, Review.Admin)
admin.site.register(AIChatLog, AIChatLog.Admin)
admin.site.register(UserProfile, UserProfile.Admin)
