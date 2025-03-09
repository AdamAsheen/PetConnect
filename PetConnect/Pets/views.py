from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Pet


def home(request):
    pets = Pet.objects.all() 
    return render(request, 'pets/home.html', {'pets': pets})

def about(request):
    return render(request, 'pets/about.html')


def contact(request):
    return render(request, 'pets/contact.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pets:home')
    else:
        form = AuthenticationForm()
    return render(request, 'pets/login.html', {'form': form})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)  
    return render(request, 'pets/pet_detail.html', {'pet': pet})


@require_POST
def like_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.likes.add(request.user)  
    return JsonResponse({'likes': pet.likes.count()})  