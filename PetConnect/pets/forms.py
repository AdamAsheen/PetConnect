# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Pet


class UserProfileForm(forms.ModelForm):
    """
    For editing the UserProfile model only, which includes:
    user (OneToOneField to User), pet_name, profile_pic, bio
    """
    class Meta:
        model = UserProfile
        fields = ['pet_name', 'profile_pic', 'bio']  
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'maxlength': 280,
                    'placeholder': 'Write a short bio about yourself...'
                }
            ),
        }


class SignUpForm(UserCreationForm):
    """
    For creating a new User (the Django auth User model).
    This form includes email, username, password1, and password2.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PetForm(forms.ModelForm):
    """
    For creating or editing Pet objects, which belong to a UserProfile.
    """
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
