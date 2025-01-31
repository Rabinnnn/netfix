from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),  # List all services
    path('service/<int:id>/', views.service_detail, name='service_detail'),  # View service details
    path('service/<int:id>/request/', views.request_service, name='request_service'),  # Request a service
    path('field/<str:field>/', views.service_field, name='service_field'),  # Filter by service field
]
