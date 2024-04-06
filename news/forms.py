from django import forms
from .models import newsCategory
from django import forms
from django.contrib.auth.forms import UserCreationForm

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = register
#         fields = '__all__'

class NewsCatrgoryForm(forms.ModelForm):
    PreferencedNews=forms.ModelChoiceField(queryset=newsCategory.objects.all())


# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

 


# from django import forms

# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput())

