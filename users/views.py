from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


# Register view (landing page for registration)
def register(request):
    return render(request, 'users/register.html')


# Customer sign-up view
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


# Company sign-up view
class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


# Login view (for both customers and companies)
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('main:home')  # Redirect to home page after login
            else:
                form.add_error(None, 'Invalid username or password')  # Display error if authentication fails
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

