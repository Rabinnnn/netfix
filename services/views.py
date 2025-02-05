from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from users.models import Company, Customer, User
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


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
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
                company=company
            )
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services:service_list')
    else:
        form = CreateNewService(choices=choices)
    
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field).order_by('-date')
    return render(request, 'services/field.html', {
        'services': services,
        'field': field
    })


def air_conditioner_view(request):
    return render(request, 'services/air_conditioner.html')

def carpentry_view(request):
    return render(request, 'services/carpentry.html')

def electricity_view(request):
    return render(request, 'services/electricity.html')

def gardening_view(request):
    return render(request, 'services/gardening.html')

def home_machines_view(request):
    return render(request, 'services/home_machines.html')

def house_keeping_view(request):
    return render(request, 'services/house_keeping.html')

def interior_design_view(request):
    return render(request, 'services/interior_design.html')

def locks_view(request):
    return render(request, 'services/locks.html')

def painting_view(request):
    return render(request, 'services/painting.html')

def plumbing_view(request):
    return render(request, 'services/plumbing.html')

def water_heaters_view(request):
    return render(request, 'services/water_heaters.html')
