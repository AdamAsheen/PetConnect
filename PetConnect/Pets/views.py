from django.shortcuts import render
from .models import Pet  

def home(request):
    pets = Pet.objects.all() 
    return render(request, 'pets/home.html', {'pets': pets})

def about(request):
    return render(request, 'pets/about.html')

def contact(request):
    return render(request, 'pets/contact.html')

def login(request):
    return render(request, 'pets/login.html')