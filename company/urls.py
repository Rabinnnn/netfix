from django.urls import path
from . import views  # Import views
from .views import company_dashboard

app_name = 'company'
#urls
urlpatterns = [
    path('dashboard/', company_dashboard, name='company_dashboard'),  # Company dashboard URL
    path('profile/', views.company_profile, name='company_profile'),
    path('requests/', views.service_requests, name='service_requests'),
    path('services/', views.service_list, name='service_list'),
    path('create_service/', views.create_service, name='create_service'),
    path('services/<int:service_id>/request_service/', views.service_detail, name='service_detail'),
]