from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


# Register view (landing page for registration)
def register(request):
    return render(request, 'users/register.html')


# Customer sign-up view
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user instance without committing to the database
            user.set_password(form.cleaned_data['password'])  # Set the password
            user.save()  # Now save the user

            # Create Customer instance
            customer = Customer.objects.create(
                user=user,
                birth=form.cleaned_data['date_of_birth']  # Pass date_of_birth to the Customer model
            )

            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful! Welcome to NetFix.')
            return redirect('customer:dashboard')
    else:
        form = CustomerSignUpForm()
    
    return render(request, 'users/register_customer.html', {
        'form': form,
        'user_type': 'customer'
    })


# Company sign-up view
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
    })


# Company registration view (if needed, can be removed)
def register_company(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('customer:customer_dashboard')  # Redirect to customer dashboard
    else:
        form = CompanySignUpForm()
    return render(request, 'users/register_company.html', {'form': form})


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
                    messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect based on user type
                    if hasattr(user, 'customer'):
                        return redirect('customer:customer_dashboard')
                    elif hasattr(user, 'company'):
                        return redirect('company:company_dashboard')  # Replace with the correct URL name for company dashboard')
                    else:
                        return redirect('main:home')
                else:
                    messages.error(request, 'Invalid email or password')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email')
    else:
        form = UserLoginForm()

    return render(request, 'main/login.html', {'form': form})