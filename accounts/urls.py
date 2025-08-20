from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signupaccount, name='signupaccount'),
    path('login/', views.loginaccount, name='loginaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
]
