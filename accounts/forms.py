from django import forms
from accounts.models import CustomUser

class SignInForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'rollno', 'branch', 'year', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rollno': forms.NumberInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-password'}),
        }

