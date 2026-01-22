from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from housing.models import Room

class CustomUserManager(BaseUserManager):
    """Custom manager to set role=ADMIN for superusers."""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN') 
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        STUDENT = "STUDENT", "Student"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class Governorate(models.TextChoices):
        SANAA = "Sana'a", "صنعاء"
        AL_JAWF = "Al Jawf", "الجوف"
        MARIB = "Ma'rib", "مارب"
        SAADA = "Sa'ada", "صعدة"
        AMRAN = "Amran", "عمران"
        IBB = "Ibb", "اب"
        DHAMAR = "Dhamar", "ذمار"
        AL_BAYDA = "Al Bayda", "البيضاء"
        SHABWAH = "Shabwah", "شبوة"
        AL_HUDAYDAH = "Al Hudaydah", "الحديدة"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    governorate = models.CharField(max_length=100, choices=Governorate.choices, blank=False, null=False)
    age = models.IntegerField(null=False, blank=False ,default=20)
    
    # Photos
    profile_photo = models.ImageField(upload_to='users/profiles/', blank=True, null=True)
    university_id_photo = models.ImageField(upload_to='users/ids/', blank=True, null=True)
    
    is_approved = models.BooleanField(default=False)  
    
    objects = CustomUserManager()  

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # def __str__(self):
        # return f"Profile: {self.user.username}"
