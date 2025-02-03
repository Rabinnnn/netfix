from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('dashboard/', views.dashboard, name='customer_dashboard'),
    path('profile/', views.customer_profile, name='profile'),
    path('history/', views.service_history, name='service_history'),
]