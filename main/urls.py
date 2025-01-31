from django.urls import path
from . import views as v

app_name = "main"

urlpatterns = [
    path('', v.home, name='home'),
    path('logout/', v.logout, name='logout'),
   path('login/', v.login_view, name='login'),  # Add the login URL pattern
 ]
