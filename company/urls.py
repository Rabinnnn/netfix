from django.urls import path
from . import views  # Import views
from .views import company_dashboard

app_name = 'company'

urlpatterns = [
    path('dashboard/', company_dashboard, name='dashboard'),  # Company dashboard URL
    path('profile/', views.company_profile, name='company_profile'),
    path('requests/', views.service_requests, name='service_requests'),
    path('services/', views.service_list, name='service_list'),
]