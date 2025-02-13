from django.urls import path
from . import views as v

app_name = "main"

urlpatterns = [
    path('', v.home, name='home'),
    path('logout/', v.logout, name='logout'),
   path('login/', v.login_view, name='login'),  # Add the login URL pattern
 ]
from django.urls import path, include
from . import views as v
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = "main"
# 
urlpatterns = [
    path('', v.home, name='home'),
    path('login/', v.login_view, name='login'),
    path('logout/', v.logout, name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('customer/', include('customer.urls')),  # Include customer URLs
    path('company/', include('company.urls')),  # Include company URLs
    path('services/check-new-requests/', v.check_new_requests, name='check_new_requests'),
]