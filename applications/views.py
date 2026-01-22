from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import HousingApplication
from housing.models import Building, Room

def is_admin_or_supervisor(user):
    return user.role in ['ADMIN', 'SUPERVISOR']

def is_admin(user):
    return user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin_or_supervisor)
def application_list(request):
    applications = HousingApplication.objects.select_related('student', 'assigned_building', 'assigned_room').order_by('-created_at')
    buildings = Building.objects.prefetch_related('rooms').all()
    return render(request, 'housing/application_list.html', {'applications': applications, 'buildings': buildings})

@login_required
@user_passes_test(is_admin)
def application_accept(request, pk):
    """Accept an application and assign a room"""
    application = get_object_or_404(HousingApplication, pk=pk)
    
    if request.method == 'POST':
        building_id = request.POST.get('building')
        room_id = request.POST.get('room')
        
        if not building_id or not room_id:
            messages.error(request, 'Please select both building and room.')
            return redirect('application_list')
        
        building = get_object_or_404(Building, pk=building_id)
        room = get_object_or_404(Room, pk=room_id)
        
        # Check if room has capacity
        if room.current_occupants >= room.capacity:
            messages.error(request, 'Selected room is full.')
            return redirect('application_list')
        
 
        application.status = HousingApplication.Status.ACCEPTED
        application.assigned_building = building
        application.assigned_room = room
        application.save()
        
        # Update room occupancy
        room.current_occupants += 1
        if room.current_occupants >= room.capacity:
            room.status = Room.Status.OCCUPIED
        room.save()
        
        # Approve the user account
        if application.student:
            application.student.is_approved = True
            application.student.save()
        
        messages.success(request, f'Application #{application.id} accepted. Student assigned to {room}.')
        return redirect('application_list')
    
    return redirect('application_list')

@login_required
@user_passes_test(is_admin)
def application_reject(request, pk):
    """Reject an application"""
    application = get_object_or_404(HousingApplication, pk=pk)
    
    if request.method == 'POST':
        application.status = HousingApplication.Status.REJECTED
        application.save()
        
        messages.success(request, f'Application #{application.id} rejected.')
        return redirect('application_list')
    
    return redirect('application_list')

@login_required
@user_passes_test(is_admin)
def application_detail(request, pk):
    """View application details including student info and photos"""
    application = get_object_or_404(HousingApplication, pk=pk)
    return render(request, 'housing/application_detail.html', {'application': application})
