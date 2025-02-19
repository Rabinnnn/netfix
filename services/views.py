from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from users.models import Company, Customer, User
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})

def check_new_requests(request):
    new_requests_count = ServiceRequest.objects.filter(status='PENDING').count()
    return JsonResponse({'new_requests_count': new_requests_count})

def most_requested_services(request):
    services = Service.objects.annotate(
        request_count=Count('requests')
    ).order_by('-request_count')[:10]
    return render(request, 'services/most_requested.html', {'services': services})


def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'customer'):
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_request = ServiceRequest(
                service=service,
                customer=request.user.customer,
                address=form.cleaned_data['address'],
                hours_needed=form.cleaned_data['hours_needed']
            )
            service_request.save()
            messages.success(request, 'Service requested successfully!')
            return redirect('services:service_list')
    else:
        form = RequestServiceForm()
    
    return render(request, 'services/single_service.html', {
        'service': service,
        'form': form
    })


@login_required
def create_service(request):
    if not request.user.is_company:
        messages.error(request, 'Only companies can create services')
        return redirect('services:service_list')
        
    company = request.user.company
    choices = [(choice[0], choice[1]) for choice in Service.choices]
    
    if company.field != 'All in One':
        choices = [(f, n) for f, n in choices if f == company.field]
    
    if request.method == "POST":
        form = CreateNewService(request.POST, choices=choices)
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
            return redirect('services:service_list')
    else:
        form = CreateNewService(choices=choices)
    
    return render(request, 'services/create.html', {'form': form})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        print('Request POST data:', request.POST)  # Log the incoming request data
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_request = ServiceRequest(  # Create the instance directly
                service=service,
                customer=request.user.customer,  # ASSIGN THE CUSTOMER HERE
                address=form.cleaned_data['address'],
                hours_needed=form.cleaned_data['hours_needed']
            )
            service_request.save()
            messages.success(request, 'Your service request has been submitted successfully!')
            return redirect('services:request_service', id=id)
        else:
            print('Form errors:', form.errors)  # Log form errors if not valid
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'service': service, 'form': form})
    

def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field).order_by('-date')
    return render(request, 'services/field.html', {
        'services': services,
        'field': field
    })

def air_conditioner_view(request):
    services = Service.objects.filter(field='Air Conditioner')
    return render(request, 'services/air_conditioner.html', {'services': services})


def carpentry_view(request):
    services = Service.objects.filter(field='Carpentry')
    return render(request, 'services/carpentry.html', {'services': services})

def electricity_view(request):
    services = Service.objects.filter(field='Electricity')
    return render(request, 'services/electricity.html', {'services': services})

def gardening_view(request):
    services = Service.objects.filter(field='Gardening')
    return render(request, 'services/gardening.html', {'services': services})

def house_keeping_view(request):
    services = Service.objects.filter(field='Housekeeping')
    return render(request, 'services/house_keeping.html', {'services': services})

def interior_design_view(request):
    services = Service.objects.filter(field='Interior Design')
    return render(request, 'services/interior_design.html', {'services': services})

def locks_view(request):
    services = Service.objects.filter(field='Locks')
    return render(request, 'services/locks.html', {'services': services})

def painting_view(request):
    services = Service.objects.filter(field='Painting')
    return render(request, 'services/painting.html', {'services': services})

def plumbing_view(request):
    services = Service.objects.filter(field='Plumbing')
    return render(request, 'services/plumbing.html', {'services': services})

def home_machines_view(request):
    services = Service.objects.filter(field='Home Machines')
    return render(request, 'services/home_machines.html', {'services': services})

def water_heaters_view(request):
    services = Service.objects.filter(field='Water Heaters')
    return render(request, 'services/water_heaters.html', {'services': services})