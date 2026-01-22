from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    description = models.TextField(blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_buildings', limit_choices_to={'role': 'SUPERVISOR'})
    
    def __str__(self):
        return self.name

class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        MAINTENANCE = "maintenance", "Maintenance"

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=1)
    current_occupants = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        unique_together = ('building', 'number')

    def __str__(self):
        return f"{self.building.name} - {self.number}"
        
    def is_full(self):
        return self.current_occupants >= self.capacity


