"""
URL configuration for SymptoScan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ss_app import views as ss

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', ss.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('disease/<str:disease_name>/', ss.disease_detail, name='disease_detail'),
    path('predict/<str:disease_name>/', ss.predict_disease, name='predict_disease'),
    path('review/add/<int:prediction_id>/', ss.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', ss.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', ss.delete_review, name='delete_review'),
    path('my-predictions/', ss.user_predictions, name='user_predictions'),
    path('api/disease/<str:disease_name>/stats/', ss.api_disease_stats, name='api_disease_stats'),
    path('api/disease/<str:disease_name>/region/<str:region>/', ss.api_regional_data, name='api_regional_data'),
    path('risk-check/', ss.risk_check, name='risk_check'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

