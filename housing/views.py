from .models import Building, Room
from .forms import BuildingForm, RoomForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


def is_admin(user):
    """Check if the user has ADMIN role."""
    return user.role == 'ADMIN'


# Template Views

@login_required
def building_list(request):
    """
    List all buildings.

    Accessible to logged-in users.
    """
    buildings = Building.objects.all()
    return render(request, 'housing/building_list.html', {'buildings': buildings})


@login_required
@user_passes_test(is_admin)
def building_create(request):
    """
    Create a new building (Admin only).
    """
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building created successfully.')
            return redirect('building_list')
    else:
        form = BuildingForm()
    return render(request, 'housing/building_form.html', {'form': form, 'title': 'Add Building'})


@login_required
@user_passes_test(is_admin)
def building_update(request, pk):
    """
    Update an existing building (Admin only).
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building updated successfully.')
            return redirect('building_list')
    else:
        form = BuildingForm(instance=building)
    return render(request, 'housing/building_form.html', {'form': form, 'title': 'Edit Building'})


@login_required
@user_passes_test(is_admin)
def building_delete(request, pk):
    """
    Delete a building (Admin only).
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        building.delete()
        messages.success(request, 'Building deleted successfully.')
        return redirect('building_list')
    return render(request, 'housing/confirm_delete.html', {'object': building})


# Room Views

@login_required
def room_list(request):
    """
    List all rooms.

    Can be filtered by 'building' ID.
    Accessible to all logged-in users.
    """
    rooms = Room.objects.all()
    
    building_id = request.GET.get('building')
    if building_id:
        # Secure ORM usage for filtering
        rooms = rooms.filter(building_id=building_id)
    
    return render(request, 'housing/room_list.html', {'rooms': rooms, 'building_id': building_id})


@login_required
@user_passes_test(is_admin)
def room_create(request):
    """
    Create a new room (Admin only).
    """
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully.')
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'housing/room_form.html', {'form': form, 'title': 'Add Room'})


@login_required
@user_passes_test(is_admin)
def room_update(request, pk):
    """
    Update an existing room (Admin only).
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully.')
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'housing/room_form.html', {'form': form, 'title': 'Edit Room'})


@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    """
    Delete a room (Admin only).
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully.')
        return redirect('room_list')
    return render(request, 'housing/confirm_delete.html', {'object': room})


@login_required
def building_detail(request, pk):
    """View building details."""
    building = get_object_or_404(Building, pk=pk)
    return render(request, 'housing/building_detail.html', {'building': building})


@login_required
def room_detail(request, pk):
    """View room details."""
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'housing/room_detail.html', {'room': room})
