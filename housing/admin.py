from django.contrib import admin
from .models import Building, Room

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'supervisor']
    search_fields = ['name', 'address']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'building', 'capacity', 'current_occupants', 'status']
    list_filter = ['status', 'building']
    search_fields = ['number', 'building__name']


