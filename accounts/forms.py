from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", )

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( "profile_pic", "bio",)