from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['type', 'description', 'room']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of your complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your issue in detail'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'student_profile') and user.student_profile.room:
             # Limit room choice to the student's assigned room logic if complex, 
             # but often students just have one room. 
             # For simpler UX, if we know their room, we might just set it in view.
             # But if they want to complain about a common area or another room? 
             # Usually complaints are about their room.
             # Let's keep it simple: generic form.
             pass
