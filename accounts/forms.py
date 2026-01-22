from django import forms
from .models import CustomUser

from housing.models import Building, Room
from .models import CustomUser, StudentProfile

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    student_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2XXXXXXX', 'maxlength': '8'})
    )
    
    # Extra fields for Student role
    supervisor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role=CustomUser.Role.SUPERVISOR),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Supervisor'
    )
    building = forms.ModelChoiceField(
        queryset=Building.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Building'
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(status=Room.Status.AVAILABLE),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Room'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'phone', 'first_name', 'last_name', 'student_id']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        role = self.cleaned_data.get('role')
        if (role == CustomUser.Role.STUDENT.value or role == 'STUDENT') and not student_id:
             raise forms.ValidationError('Student ID is required for students.')
             
        if student_id:
            student_id = student_id.strip()
            if len(student_id) != 8:
                raise forms.ValidationError('Student ID must be exactly 8 digits.')
            if not student_id.isdigit():
                raise forms.ValidationError('Student ID must contain only numbers.')
            if not student_id.startswith('2'):
                raise forms.ValidationError('Student ID must start with 2.')
        return student_id

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == CustomUser.Role.STUDENT.value or role == 'STUDENT':
            supervisor = cleaned_data.get('supervisor')
            building = cleaned_data.get('building')
            room = cleaned_data.get('room')
            
            if not supervisor:
                self.add_error('supervisor', 'Supervisor is required for students.')
            if not building:
                self.add_error('building', 'Building is required for students.')
            if not room:
                 self.add_error('room', 'Room is required for students.')
            
            if room and room.is_full():
                 self.add_error('room', 'Selected room is full.')
        
        return cleaned_data

    def save(self, commit=True):
        from applications.models import HousingApplication
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            
            # Handle Student Housing Assignment
            if user.role == CustomUser.Role.STUDENT.value or user.role == 'STUDENT':
                room = self.cleaned_data.get('room')
                building = self.cleaned_data.get('building')
                
                if room and building:
                    # Create/Update StudentProfile
                    profile, created = StudentProfile.objects.get_or_create(user=user)
                    profile.room = room
                    profile.save()
                    
                    # Create HousingApplication with ACCEPTED status
                    HousingApplication.objects.create(
                        student=user,
                        name=f"{user.first_name} {user.last_name}",
                        phone=user.phone or '',
                        age=user.age if user.age else 20,
                        governorate=user.governorate if user.governorate else "Sana'a",
                        status=HousingApplication.Status.ACCEPTED,
                        assigned_building=building,
                        assigned_room=room
                    )
                    
                    # Update Room Occupancy
                    room.current_occupants += 1
                    if room.is_full():
                        room.status = Room.Status.OCCUPIED
                    room.save()
                    
        return user

class UserEditForm(forms.ModelForm):
    """Form for editing existing users - no password field, allows role change"""
    student_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2XXXXXXX', 'maxlength': '8'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'phone', 'first_name', 'last_name', 'student_id', 'is_approved']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            student_id = student_id.strip()
            if len(student_id) != 8:
                raise forms.ValidationError('Student ID must be exactly 8 digits.')
            if not student_id.isdigit():
                raise forms.ValidationError('Student ID must contain only numbers.')
            if not student_id.startswith('2'):
                raise forms.ValidationError('Student ID must start with 2.')
        return student_id


class RegistrationForm(forms.ModelForm):
    """Form for student registration """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text='Password must be at least 8 characters.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'student_id', 'governorate', 'age']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2XXXXXXX',
                'maxlength': '8',
                'pattern': '2[0-9]{7}'
            }),
            'governorate': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    profile_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    university_card_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    def clean_student_id(self):
        """Validate student ID: must be 8 digits and start with 2"""
        student_id = self.cleaned_data.get('student_id')
        
        if student_id:
            student_id = student_id.strip()
            if len(student_id) != 8:
                raise forms.ValidationError('Student ID must be exactly 8 digits.')
            if not student_id.isdigit():
                raise forms.ValidationError('Student ID must contain only numbers.')
            if not student_id.startswith('2'):
                raise forms.ValidationError('Student ID must start with 2.')
        
        return student_id
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = CustomUser.Role.STUDENT
        user.is_approved = False
        if commit:
            user.save()
        return user
