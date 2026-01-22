from .models import Service, StudentService
from .forms import ServiceForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.role == 'ADMIN'

@login_required
def service_list(request):
    services = Service.objects.all()
    user_subscriptions = StudentService.objects.filter(student=request.user) if request.user.role == 'STUDENT' else StudentService.objects.all()
    return render(request, 'services/service_list.html', {'services': services, 'subscriptions': user_subscriptions})

@login_required
@user_passes_test(is_admin)
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})

@login_required
@user_passes_test(is_admin)
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})

@login_required
@user_passes_test(is_admin)
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('service_list')
    return render(request, 'services/confirm_delete.html', {'object': service})
