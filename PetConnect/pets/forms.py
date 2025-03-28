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
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove help texts
        for field in self.fields.values():
            field.help_text = None

        # Uniform styling for all fields
        self.fields['username'].widget.attrs.update({
            'placeholder': 'e.g., petlover123',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'At least 8 characters',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat your password',
            'class': 'form-control'
        })
        
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
