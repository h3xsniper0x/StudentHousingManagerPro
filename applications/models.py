from django.db import models
from django.conf import settings
from housing.models import Building, Room

class HousingApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    name = models.CharField(max_length=200) 
    phone = models.CharField(max_length=20)
    age = models.IntegerField()

    governorate = models.CharField(max_length=100, choices=[
        ("Sana'a", "صنعاء"),
        ("Al Jawf", "الجوف"),
        ("Ma'rib", "مارب"),
        ("Sa'ada", "صعدة"),
        ("Amran", "عمران"),
        ("Ibb", "اب"),
        ("Dhamar", "ذمار"),
        ("Al Bayda", "البيضاء"),
        ("Shabwah", "شبوة"),
        ("Al Hudaydah", "الحديدة"),
    ])
    
    
    profile_image = models.ImageField(upload_to='applications/profiles/', null=True, blank=True) 
    university_card_image = models.ImageField(upload_to='applications/ids/', null=True, blank=True) 
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    assigned_building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Application for {self.name}"


# from django.contrib.auth import get_user_model
# User = get_user_model()