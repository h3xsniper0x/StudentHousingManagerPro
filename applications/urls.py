from django.urls import path
from .views import application_list, application_accept, application_reject, application_detail

urlpatterns = [
    path('list/', application_list, name='application_list'),
    path('<int:pk>/accept/', application_accept, name='application_accept'),
    path('<int:pk>/reject/', application_reject, name='application_reject'),
    path('<int:pk>/', application_detail, name='application_detail'),
]
