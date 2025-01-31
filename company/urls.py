from django.urls import path
from . import views as company_views

urlpatterns = [
    # Reusing service URLs for the company
    path('your-services/', company_views.service_list, name='company_service_list'),
    path('create-service/', company_views.create, name='company_create_service'),
    path('service/<int:id>/', company_views.index, name='company_service_detail'),
    path('service/<int:id>/request/', company_views.request_service, name='company_request_service'),
    path('service/field/<slug:field>/', company_views.service_field, name='company_service_field'),
]
