from django import forms
from .models import Building, Room

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'description', 'supervisor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['building', 'number', 'capacity', 'status']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
