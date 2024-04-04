from django import forms
from .models import register

class RegisterForm(forms.ModelForm):
    class Meta:
        model = register
        fields = '__all__'
