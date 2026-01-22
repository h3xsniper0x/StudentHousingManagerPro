from django.urls import path
from .views import complaint_list, complaint_update, complaint_detail, complaint_create

urlpatterns = [
    # Template Views
    path('complaints/list/', complaint_list, name='complaint_list'),
    path('complaints/add/', complaint_create, name='complaint_create'),
    path('complaints/<int:pk>/update/', complaint_update, name='complaint_update'),
    path('complaints/<int:pk>/', complaint_detail, name='complaint_detail'),
]
