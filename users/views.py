from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserLoginForm  # Assuming you are using a custom form
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomerSignUpForm
from .models import Customer
from django.contrib.auth.models import User
import logging

# Configure logging
logger = logging.getLogger(__name__)

# 
# Register view (landing page for registration)
def register(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # Redirect to the appropriate dashboard based on user type
        if hasattr(request.user, 'customer'):
            return redirect('customer:customer_dashboard')
        elif hasattr(request.user, 'company'):
            return redirect('company:company_dashboard')
        else:
            return redirect('main:home')  # Fallback page for other users
    
    return render(request, 'users/register.html')

# Customer Profile view
@login_required
def customer_profile(request):
    # Ensure the user is a customer
    if not request.user.is_customer:
        messages.error(request, "Access denied. Customer account required.")
        return redirect('main:home')
    
    # Get the customer instance
    customer = request.user.customer  # Assuming 'customer' is a related model for User

    # You can add any additional logic or context data here
    return render(request, 'customer/customer_profile.html', {'customer': customer})

# Customer sign-up view
def customer_signup(request):
    # Check if the user is authenticated and a customer
    if request.user.is_authenticated:
        if hasattr(request.user, 'customer'):
            # If the user is already a customer, redirect them to the homepage
            return redirect('main:home')  # Redirect to the homepage
        else:
            # If the user is authenticated but not a customer, redirect to the homepage
            return redirect('main:home')

    # If the user is not authenticated, proceed with the signup process
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_customer = True  # Set is_customer to True
            user.save()  # Now save the user

            # Create Customer instance
            customer = Customer.objects.create(
                user=user,
                birth=form.cleaned_data['date_of_birth'],  # Pass date_of_birth to the Customer model
                name=user.get_full_name()  # Assuming you want to save the full name
            )

            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful! Welcome to NetFix.')
            return redirect('customer:customer_dashboard')  # Redirect to the customer dashboard
    else:
        form = CustomerSignUpForm()

    return render(request, 'users/register_customer.html', {
        'form': form,
        'user_type': 'customer'
    })

# Company sign-up view
"""
def company_signup(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to NetFix.')
            return redirect('company:dashboard')  # Redirect to the company dashboard
    else:
        form = CompanySignUpForm()
    
    return render(request, 'users/register_company.html', {
        'form': form,
        'user_type': 'company'
    })"""


def register_company(request):
    # Check if the user is authenticated and is a company
    if request.user.is_authenticated:
        if hasattr(request.user, 'company'):
            # If the user is already a company, redirect them to the homepage
            return redirect('main:home')  # Redirect to the homepage
        else:
            # If the user is authenticated but not a company (e.g., a customer), redirect to the homepage
            return redirect('main:home')

    # If the user is not authenticated, proceed with the sign-up process
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            # Create and save the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_company=True  # Mark as company
            )

            # Create and save the related Company instance
            company = Company.objects.create(
                user=user,
                email=form.cleaned_data['email'],
                description=form.cleaned_data['description'],
                location=form.cleaned_data['location'],
                field_of_work=form.cleaned_data['field_of_work']
            )

            login(request, user)
            return redirect('company:company_dashboard')  # Redirect after successful registration

    else:
        form = CompanySignUpForm()

    return render(request, 'users/register_company.html', {'form': form})

User = get_user_model()

# Login view (for both customers and companies)
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Get user by email
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    # messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect based on user type
                    if hasattr(user, 'customer'):
                        return redirect('customer:customer_dashboard')  
                    elif hasattr(user, 'company'):
                        return redirect('company:company_dashboard')  
                    else:
                        return redirect('main:home')
                else:
                    messages.error(request, 'Invalid email or password')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email')
    else:
        form = UserLoginForm()

    return render(request, 'main/login.html', {'form': form})

def custom_404_view(request, exception):
    try:
        return render(request, '404.html', status=404)
    except Exception as e:
        logger.error(f'Error rendering 404 page: {e}')
        return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def test_error_view(request):
    raise Exception("Testing 500 error")