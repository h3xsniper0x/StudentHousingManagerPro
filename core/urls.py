from django.urls import path
from .views import home, admin_dashboard, supervisor_dashboard, student_dashboard, reports_view, rejected_view

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/supervisor/', supervisor_dashboard, name='supervisor_dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('rejected/', rejected_view, name='application_rejected'),
    path('reports/', reports_view, name='reports'),
]
