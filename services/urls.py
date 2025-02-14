from django.urls import path
from . import views as v
from company import views as company_views

app_name = 'services'

urlpatterns = [
    path('', v.service_list, name='service_list'),
    path('most-requested/', v.most_requested_services, name='most_requested'),
    path('create/', v.create_service, name='create_service'),
    path('<int:id>/', v.service_detail, name='service_detail'),
    path('field/<str:field>/', v.service_field, name='service_field'),
    path('air-conditioner/', v.air_conditioner_view, name='air_conditioner'),
    path('carpentry/', v.carpentry_view, name='carpentry'),
    path('electricity/', v.electricity_view, name='electricity'),
    path('gardening/', v.gardening_view, name='gardening'),
    path('home-machines/', v.home_machines_view, name='home_machines'),
    path('house-keeping/', v.house_keeping_view, name='house_keeping'),
    path('interior-design/', v.interior_design_view, name='interior_design'),
    path('locks/', v.locks_view, name='locks'),
    path('painting/', v.painting_view, name='painting'),
    path('plumbing/', v.plumbing_view, name='plumbing'),
    path('water-heaters/', v.water_heaters_view, name='water_heaters'),
    path('<int:id>/request_service/', v.request_service, name='request_service'),
    path('check-new-requests/', v.check_new_requests, name='check_new_requests'),
]
# 