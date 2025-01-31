from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as django_logout

# Home view
def home(request):
    return render(request, "main/home.html", {})

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
                    return redirect('main:company_dashboard')
                elif hasattr(user, 'customer'):  # Check if the user has a customer profile
                    return redirect('main:customer_dashboard')
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
    return redirect('main:home')  # Redirect to home page after logout

# Company Dashboard view
def company_dashboard(request):
    return render(request, 'company/dashboard.html')  # Make sure this template exists

# Customer Dashboard view
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')  # Make sure this template exists
