from django.contrib import admin
from .models import HousingApplication

@admin.register(HousingApplication)
class HousingApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'assigned_building', 'assigned_room', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at']
