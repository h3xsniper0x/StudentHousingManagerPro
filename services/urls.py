from django.urls import path
from .views import service_list, service_create, service_update, service_delete

urlpatterns = [
    # Template Views
    path('services/list/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('services/<int:pk>/update/', service_update, name='service_update'),
    path('services/<int:pk>/delete/', service_delete, name='service_delete'),
]
