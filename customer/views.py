from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import logout as django_logout
from users.models import Customer
from services.models import Service, ServiceRequest

# Create your views here.
# 
@login_required
@login_required
def dashboard(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. Customer account required.")
        return redirect('main:home')
    
    customer = request.user.customer
    service_requests = ServiceRequest.objects.filter(
        customer=customer
    ).order_by('-request_date')
    
    # Get recent service requests
    recent_requests = service_requests[:5]
    
    # Calculate total spent
    total_spent = service_requests.filter(
        status='COMPLETED'
    ).aggregate(
        total=Sum('total_cost')
    )['total'] or 0
    
    context = {
        'customer': customer,
        'recent_requests': recent_requests,
        'total_requests': service_requests.count(),
        'pending_requests': service_requests.filter(status='PENDING').count(),
        'completed_requests': service_requests.filter(status='COMPLETED').count(),
        'total_spent': total_spent
    }
    return render(request, 'customer/customer_dashboard.html', context)  # Updated template name   return render(request, 'customer/dashboard.html', context)
# Logout view
def logout(request):
    django_logout(request)
    return render(request, 'main/logout.html')  # Redirect to logout page after logout
@login_required
def customer_profile(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. Customer account required.")
        return redirect('main:home')
    
    customer = request.user.customer
    service_requests = ServiceRequest.objects.filter(
        customer=customer
    ).order_by('-request_date')
    
    context = {
        'customer': customer,
        'service_requests': service_requests,
        'total_spent': service_requests.filter(
            status='COMPLETED'
        ).aggregate(
            total=Sum('total_cost')
        )['total'] or 0
    }
    return render(request, 'customer/customer_profile.html', context)

@login_required
def service_history(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. Customer account required.")
        return redirect('main:home')
    
    customer = request.user.customer
    service_requests = ServiceRequest.objects.filter(
        customer=customer
    ).order_by('-request_date')
    
    context = {
        'service_requests': service_requests,
        'total_requests': service_requests.count(),
        'pending_requests': service_requests.filter(status='PENDING').count(),
        'completed_requests': service_requests.filter(status='COMPLETED').count()
    }
    return render(request, 'customer/service_history.html', context)
