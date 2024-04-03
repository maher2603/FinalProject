from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Vehicle, VehicleLog, Post

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length = 25)
    email = forms.EmailField(required=True)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Required.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'dob', 'password1', 'password2')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['user_id', 'registration_number', 'make', 'colour', 'year_of_manufacture', 'fuel_type', 'engine_capacity', 'tax_status', 'tax_due_date', 'mot_status', 'mot_expiry_date']

class VehicleLogForm(forms.ModelForm):
    class Meta:
        model = VehicleLog
        fields = ['vehicle_id', 'title', 'date', 'cost', 'description', 'file_upload']
        
    # file_upload = forms.FileField()
    widgets = {'file_upload': forms.FileInput(attrs={'required': False})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user_id', 'title', 'description', 'image_upload']
        
    widgets = {'image_upload': forms.FileInput(attrs={'required': False})}