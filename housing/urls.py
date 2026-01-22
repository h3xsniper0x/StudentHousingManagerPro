from django.urls import path
from .views import (
    building_list, building_create, building_update, building_delete, building_detail,
    room_list, room_create, room_update, room_delete, room_detail,
)

urlpatterns = [
    # Template Views
    path('housing/buildings/list/', building_list, name='building_list'),
    path('housing/buildings/create/', building_create, name='building_create'),
    path('housing/buildings/<int:pk>/update/', building_update, name='building_update'),
    path('housing/buildings/<int:pk>/delete/', building_delete, name='building_delete'),
    path('housing/buildings/<int:pk>/', building_detail, name='building_detail'),
    path('housing/rooms/list/', room_list, name='room_list'),
    path('housing/rooms/create/', room_create, name='room_create'),
    path('housing/rooms/<int:pk>/update/', room_update, name='room_update'),
    path('housing/rooms/<int:pk>/delete/', room_delete, name='room_delete'),
    path('housing/rooms/<int:pk>/', room_detail, name='room_detail'),
]
