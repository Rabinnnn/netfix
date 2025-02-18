import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from django.http import JsonResponse
from services.models import Service, ServiceRequest# Adjust the import based on your project structure


# Home view
def home(request):
    return render(request, "main/home.html", {})
# 
# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                django_login(request, user)

                # Check if the user is a company or customer
                if hasattr(user, 'company'):  # Check if the user has a company profile
                    return redirect('company:company_dashboard')
                elif hasattr(user, 'customer'):  # Check if the user has a customer profile
                    return redirect('customer:customer_dashboard')
                else:
                    # Handle case if the user does not have a company or customer profile
                    return redirect('main:home')  # Or some other fallback page
            else:
                form.add_error(None, 'Invalid username or password')  # Display error if authentication fails
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

# Logout view
def logout(request):
    django_logout(request)
    return render(request, 'main/logout.html')  # Redirect to logout page after logout

# Password Reset Request View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/password_reset_email.html'
    success_url = reverse_lazy('main:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

# Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'

# Password Reset Confirm View
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')

# Password Reset Complete View
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'

# Company Dashboard view
def company_dashboard(request):
    return render(request, 'company/templates/company/company_dashboard.html')  # Make sure this template exists

# Customer Dashboard view
def customer_dashboard(request):
    return render(request, 'customer/templates/customer/customer_dashboard.html')  # Make sure this template exists


# def check_new_requests(request):
#     if request.user.is_authenticated and request.user.is_company:
#         new_requests = ServiceRequest.objects.filter(status='PENDING').values(
#             'id', 'address', 'hours_needed', 'total_cost', 'request_date', 'customer_id', 'service_id','status',
#         )
#         new_requests_count = new_requests.count()
#         return JsonResponse({
#             'new_requests_count': new_requests_count,
#             'requests': list(new_requests)
#         })
#     return JsonResponse({'new_requests_count': 0, 'requests': []})
def check_new_requests(request):
    if request.user.is_authenticated and request.user.is_company:
        # Get all service IDs owned by the logged-in company
        service_ids = Service.objects.filter(company_id=request.user.id).values_list('id', flat=True)

        # Filter service requests where service_id matches the logged-in company's services
        new_requests = ServiceRequest.objects.filter(
            status__in=['PENDING', 'ACCEPTED', 'CANCELLED', 'COMPLETED'],
            service_id__in=service_ids  # Corrected query
        ).values(
            'id', 'address', 'hours_needed', 'total_cost', 'request_date', 'customer_id', 'service_id', 'status', 'service_name'
        )

        new_requests_count = new_requests.count()
        
        return JsonResponse({
            'new_requests_count': new_requests_count,
            'requests': list(new_requests)
        })

    return JsonResponse({'new_requests_count': 0, 'requests': []})


def update_request_status(request, request_id):
    if request.method == "POST":
        try:
            service_request = ServiceRequest.objects.get(id=request_id)
            
            # Parse the request body as JSON
            data = json.loads(request.body.decode("utf-8"))
            new_status = data.get("status")
            
            if new_status in ['ACCEPTED', 'CANCELLED', 'COMPLETED']:
                service_request.status = new_status
                service_request.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Invalid status"})
        except ServiceRequest.DoesNotExist:
            return JsonResponse({"success": False, "error": "Request not found"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"})
    return JsonResponse({"success": False, "error": "Invalid method"})