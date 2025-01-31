from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import Company
from services.models import Service
from services.forms import CreateNewService, RequestServiceForm  # Reusing forms from services app

# List all services for the company
def service_list(request):
    company = request.user.company  # Directly accessing the company from the user model
    services = Service.objects.filter(company=company).order_by("-date_created")
    return render(request, 'company/service_list.html', {'services': services})

# View a single service for the company
def service_detail(request, id):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h1>Service not found</h1>")
    return render(request, 'company/single_service.html', {'service': service})

# Create a new service (for company)
def create_service(request):
    company = request.user.company
    choices = [(choice[0], choice[1]) for choice in Service.FIELD_CHOICES]  # Assuming this comes from the service model
    form = CreateNewService(choices=choices)
    
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
            return redirect('company:service_list')  # Corrected redirect URL name to 'company:service_list'

    return render(request, 'company/create_service.html', {'form': form})

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

    return render(request, 'company/request_service.html', {'service': service, 'form': form})
