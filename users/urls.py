from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from customer import views as customer_views

app_name = 'users'

urlpatterns = [
    path('', user_views.register, name='register'),
    path('company/', user_views.company_signup, name='register_company'),
    path('customer/', user_views.customer_signup, name='register_customer'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', customer_views.dashboard, name='dashboard'),  
]
