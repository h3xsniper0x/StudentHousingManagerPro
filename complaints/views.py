from .models import Complaint
from .forms import ComplaintForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

@login_required
def complaint_list(request):
    user = request.user
    if user.role == 'STUDENT':
        complaints = Complaint.objects.filter(student=user)
    else:
        complaints = Complaint.objects.all()
    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})

@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, user=request.user)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            # Auto-assign room if not selected but student has one
            if not complaint.room and hasattr(request.user, 'student_profile') and request.user.student_profile.room:
                complaint.room = request.user.student_profile.room
            complaint.save()
            messages.success(request, 'Complaint submitted successfully.')
            return redirect('complaint_list')
    else:
        form = ComplaintForm(user=request.user)
    
    return render(request, 'complaints/add_complaint.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN')
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            complaint.status = new_status
            complaint.save()
            messages.success(request, 'Complaint status updated.')
            return redirect('complaint_list')
    
    return render(request, 'complaints/complaint_form.html', {'object': complaint})

@login_required
def complaint_detail(request, pk):
    """View complaint details"""
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.user.role == 'STUDENT' and complaint.student != request.user:
         messages.error(request, "Access denied.")
         return redirect('complaint_list')
         
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})





#studentprofile__user=request.user
