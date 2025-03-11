from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Pet
from .models import Category
from .models import Post


def home(request):
    pets = Pet.objects.all().order_by('-id')[:10] 
    posts = Post.objects.all().order_by('-date_created')[:10] 
    return render(request, 'pets/home.html', {'pets': pets})

def about(request):
    return render(request, 'pets/about.html')


def contact(request):
    return render(request, 'pets/contact.html')

def profile(request):
    return render(request, 'pets/profile.html')

def categories(request):
    categories = Category.objects.all()  
    return render(request, 'pets/categories.html', {'categories': categories})

def chat(request):
    return render(request, 'pets/chat.html')


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



def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'pets/post_detail.html', {'post': post})


@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.add(request.user)  
    return JsonResponse({'likes': post.likes.count()})