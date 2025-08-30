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
from ss_app import views as ss
from ss_app import chat_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ss.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('disease/<str:disease_name>/', ss.disease_detail, name='disease_detail'),
    path('predict/<str:disease_name>/', ss.predict_disease, name='predict_disease'),
    path('user-predictions/', ss.user_predictions, name='user_predictions'),
    path('prediction/<int:prediction_id>/result/', ss.view_prediction_result, name='view_prediction_result'),
    path('add-review/<int:prediction_id>/', ss.add_review, name='add_review'),
    path('edit-review/<int:review_id>/', ss.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', ss.delete_review, name='delete_review'),
    path('api/disease/<str:disease_name>/stats/', ss.api_disease_stats, name='api_disease_stats'),
    path('api/disease/<str:disease_name>/region/<str:region>/', ss.api_regional_data, name='api_regional_data'),
    path('risk-check/', ss.risk_check, name='risk_check'),
    path('wordcloud/', ss.wordcloud_view, name='wordcloud'),
    
    # AI Chat URLs
    path('chat/<int:prediction_id>/', chat_views.chat_with_ai, name='chat_with_ai'),
    path('chat/<int:prediction_id>/start/', chat_views.start_new_conversation, name='start_new_conversation'),
    path('chat/send-message/', chat_views.send_message, name='send_message'),
    path('chat/history/', chat_views.chat_history, name='chat_history'),
    path('chat/conversation/<str:conversation_id>/', chat_views.view_conversation, name='view_conversation'),
    path('chat/conversation/<str:conversation_id>/delete/', chat_views.delete_conversation, name='delete_conversation'),
    
    # Custom Admin Dashboard URLs
    path('custom-admin/', ss.admin_dashboard, name='admin_dashboard'),
    path('admin-test/', ss.admin_test, name='admin_test'),
    path('custom-admin/users/', ss.admin_users, name='admin_users'),
    path('custom-admin/users/<int:user_id>/', ss.admin_user_detail, name='admin_user_detail'),
    path('custom-admin/users/<int:user_id>/delete/', ss.admin_delete_user, name='admin_delete_user'),
    path('custom-admin/diseases/', ss.admin_diseases, name='admin_diseases'),
    path('custom-admin/diseases/<int:disease_id>/', ss.admin_disease_detail, name='admin_disease_detail'),
    path('custom-admin/diseases/<int:disease_id>/edit/', ss.admin_disease_edit, name='admin_disease_edit'),
    path('custom-admin/diseases/<int:disease_id>/delete/', ss.admin_disease_delete, name='admin_disease_delete'),
    path('custom-admin/diseases/<int:disease_id>/form-fields/', ss.admin_form_fields, name='admin_form_fields'),
    path('custom-admin/reviews/', ss.admin_reviews, name='admin_reviews'),
    path('custom-admin/reviews/<int:review_id>/moderate/', ss.admin_review_moderate, name='admin_review_moderate'),
    path('custom-admin/chat-logs/', ss.admin_chat_logs, name='admin_chat_logs'),
    path('custom-admin/chat-logs/<int:chat_log_id>/delete/', ss.admin_delete_chat_log, name='admin_delete_chat_log'),
    path('admin_logout/', ss.admin_logout, name='admin_logout'),
]

