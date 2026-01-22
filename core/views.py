from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .decorators import role_required
from accounts.models import CustomUser
from complaints.models import Complaint
from applications.models import HousingApplication
from housing.models import Building, Room
from datetime import datetime, timedelta

def home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser or user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif user.role == 'SUPERVISOR':
            return redirect('supervisor_dashboard')
        elif user.role == 'STUDENT':
            # Check for rejected application
            application = HousingApplication.objects.filter(student=user).last()
            if application:
                if application.status == HousingApplication.Status.REJECTED:
                    return redirect('application_rejected')
                elif application.status == HousingApplication.Status.PENDING:
                    return redirect('register_success')
            return redirect('student_dashboard')
    return render(request, 'core/home.html')

@login_required
@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    users_count = CustomUser.objects.count()
    complaints_count = Complaint.objects.count()
    approved_count = HousingApplication.objects.filter(status=HousingApplication.Status.ACCEPTED).count()
    pending_count = HousingApplication.objects.filter(status=HousingApplication.Status.PENDING).count()
    rejected_count = HousingApplication.objects.filter(status=HousingApplication.Status.REJECTED).count()
    
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_apps = (
        HousingApplication.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    app_labels = []
    app_data = []
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for entry in monthly_apps:
        app_labels.append(month_names[entry['month'].month - 1])
        app_data.append(entry['count'])
    
    
    if not app_labels:
        app_labels = [month_names[datetime.now().month - 1]]
        app_data = [0]
    
    total_capacity = Room.objects.aggregate(total=Sum('capacity'))['total'] or 0
    total_occupied = Room.objects.aggregate(total=Sum('current_occupants'))['total'] or 0
    total_free = max(0, total_capacity - total_occupied)
    
    context = {
        'users_count': users_count,
        'complaints_count': complaints_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'app_labels': app_labels,
        'app_data': app_data,
        'occupancy_free': total_free,
        'occupancy_occupied': total_occupied,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@role_required(allowed_roles=['SUPERVISOR'])
def supervisor_dashboard(request):
    user = request.user
    my_buildings = Building.objects.filter(supervisor=user)
    
    
    recent_complaints = Complaint.objects.filter(
        room__building__in=my_buildings
    ).select_related('room', 'student').order_by('-created_at')[:10]
    
    context = {
        'my_buildings_count': my_buildings.count(),
        'pending_moveins_count': HousingApplication.objects.filter(assigned_building__in=my_buildings, status=HousingApplication.Status.ACCEPTED).count(),
        'active_complaints_count': Complaint.objects.filter(room__building__in=my_buildings).exclude(status=Complaint.Status.RESOLVED).count(),
        'assigned_buildings': my_buildings,
        'pending_confirmations': HousingApplication.objects.filter(assigned_building__in=my_buildings, status=HousingApplication.Status.ACCEPTED)[:5],
        'recent_complaints': recent_complaints,
    }
    return render(request, 'dashboard/supervisor_dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('home')

    application = HousingApplication.objects.filter(student=request.user).last()

    if application:
        if application.status == HousingApplication.Status.REJECTED:
            return redirect('application_rejected')
        elif application.status == HousingApplication.Status.PENDING:
            return redirect('register_success')

    recent_complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')[:5]
    
    context = {
        'application': application,
        'recent_complaints': recent_complaints
    }
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def rejected_view(request):
    if request.user.role != 'STUDENT':
        return redirect('home')
    
    application = HousingApplication.objects.filter(student=request.user).last()
    
    # If not rejected, redirect back to dashboard
    if not application or application.status != HousingApplication.Status.REJECTED:
        return redirect('student_dashboard')
        
    return render(request, 'dashboard/application_rejected.html', {'application': application})
@login_required
def reports_view(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    return render(request, 'core/reports.html')
