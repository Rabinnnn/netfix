from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Count
from .models import Company
from services.models import Service, ServiceRequest
from services.forms import CreateNewService, RequestServiceForm  # Reusing forms from services app

#
# List all services for the company
def service_list(request):
    company = request.user.company  # Directly accessing the company from the user model
    services = Service.objects.filter(company=company).order_by("-date")
    return render(request, 'company/service_list.html', {'services': services})

# View a single service for the company
def service_detail(request, id):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h1>Service not found</h1>")
    return render(request, 'company/single_service.html', {'service': service})

# Create a new service (for company)
@login_required
def create_service(request):
    if not request.user.is_company:
        messages.error(request, 'Only companies can create services')
        return redirect('services:service_list')

    company = request.user.company
    field_choices = [(choice[0], choice[1]) for choice in Service.choices]

    # If company.field_of_work is not 'All in One', filter the choices and set initial value
    initial_data = {}
    if company.field_of_work != 'All in One':
        field_choices = [(f, n) for f, n in field_choices if f == company.field_of_work]
        initial_data['field'] = company.field_of_work  # Set default value

    # Initialize form with field choices and default value (if applicable)
    form = CreateNewService(choices=field_choices, initial=initial_data)

    if request.method == "POST":
        form = CreateNewService(request.POST, choices=field_choices)
        if form.is_valid():
            service = Service(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_per_hour=form.cleaned_data['price_per_hour'],
                field=form.cleaned_data['field'],
                company=company
            )
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('company:service_list')  # Ensure correct redirect

    return render(request, 'company/create_service.html', {'form': form, 'company': company})

# Logout view
def logout(request):
    django_logout(request)
    return redirect('main:logout')  # Redirect to home page after logout

# Filter services by field for the company
def service_field(request, field):
    company = request.user.company
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(company=company, field=field)
    return render(request, 'company/service_field.html', {'services': services, 'field': field})

# Request a service (for company)
def request_service(request, id):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h1>Service not found</h1>")
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Process the request (save, notify, etc.)
            pass
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'service': service, 'form': form})

@login_required
def company_dashboard(request):
    # Fetch any necessary data for the dashboard
    company = request.user.company
    services = Service.objects.filter(company=company).order_by('-date')
    services_requested = ServiceRequest.objects.values('service_name', 'service__name').annotate(
        request_count=Count('id')
    ).order_by('-request_count')[:3]
    pending_requests = ServiceRequest.objects.filter(
        service__company=company,
        status='PENDING'
    ).order_by('-request_date')
    
    context = {
        'company': company,
        'services': services,
        'services_requested': services_requested,
        'pending_requests': pending_requests,
        'total_services': services.count(),
       # 'avg_rating': services.aggregate(Avg('rating'))['rating__avg'] or 0
    }
    return render(request, 'company/company_dashboard.html', context)

@login_required
def company_profile(request):
    # Logic to retrieve and display company profile information
    company = request.user.company
    services = Service.objects.filter(company=company).order_by('-date')
    completed_requests = ServiceRequest.objects.filter(
        service__company=company,
        status='COMPLETED'
    ).count()
    
    context = {
        'company': company,
        'services': services,
        'completed_requests': completed_requests,
        # 'avg_rating': services.aggregate(Avg('rating'))['rating__avg'] or 0
    }
    return render(request, 'company/company_profile.html', context)

@login_required
def service_requests(request):
    if not request.user.is_company:
        messages.error(request, "Access denied. Company account required.")
        return redirect('main:home')
    
    company = request.user.company
    requests = ServiceRequest.objects.filter(
        service__company=company
    ).order_by('-request_date')
    
    context = {
        'requests': requests,
        'pending_count': requests.filter(status='PENDING').count(),
        'completed_count': requests.filter(status='COMPLETED').count()
    }
    return render(request, 'company/service_requests.html', context)

#   render single service for viewing 
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'company/service_detail.html', {'service': service})