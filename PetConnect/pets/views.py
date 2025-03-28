from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
import json
from .forms import SignUpForm, UserProfileForm, PetForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# NEW IMPORT for the decorator
from django.contrib.auth.decorators import login_required


def general_feed(request):
    posts = Post.objects.all().order_by('-date_created')[:10]
    categories = Category.objects.all()
    comments = Comment.objects.filter(post__in=posts)

    liked_post_ids = set()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        liked_posts = Like.objects.filter(user=user_profile, post__in=posts)\
                                  .values_list('post_id', flat=True)
        liked_post_ids = set(liked_posts)

    context_dict = {
        "posts": posts,
        "comments": comments,
        "categories": categories,
        "liked_post_ids": liked_post_ids,
    }
    return render(request, 'home.html', context_dict)

@login_required
def following_feed(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    followed_profiles = Follow.objects.filter(follower=user_profile).values_list('followed', flat=True)
    posts = Post.objects.filter(user__id__in=followed_profiles).order_by('-date_created')[:10]
    categories = Category.objects.all()
    comments = Comment.objects.filter(post__in=posts)
    liked_posts = Like.objects.filter(user=user_profile, post__in=posts).values_list('post_id', flat=True)

    context_dict = {
        "posts": posts,
        "comments": comments,
        "categories": categories,
        "liked_post_ids": set(liked_posts),
    }
    return render(request, 'home.html', context_dict)

@login_required
def add_likes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_id = data.get("post-id")
            post = Post.objects.get(id=post_id)
            user_profile = UserProfile.objects.get(user=request.user.id)

            existing_like = Like.objects.filter(user=user_profile, post=post).first()
            if not existing_like:
                Like.objects.create(user=user_profile, post=post)
            
            new_like_count = post.likes.count()
            return JsonResponse({"success": True, "new_like_count": new_like_count})

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def remove_likes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_id = data.get("post-id")
            post = Post.objects.get(id=post_id)
            user_profile = UserProfile.objects.get(user_id=request.user.id)

            existing_like = Like.objects.filter(user=user_profile, post=post).first()
            if existing_like:
                existing_like.delete()
            
            new_like_count = post.likes.count()
            return JsonResponse({"success": True, "new_like_count": new_like_count})

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get("comment-content")
            post_id = data.get("post-id")
            post = Post.objects.get(id=post_id)

            if not request.user.is_authenticated:
                return JsonResponse({"error": "User is not authenticated"}, status=401)

            user_profile = UserProfile.objects.get(user=request.user)
            Comment.objects.create(user=user_profile, post=post, comment_text=comment_text)
            
            return JsonResponse({
                "success": True,
                "username": request.user.username,
                "comment_text": comment_text
            })

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories/categories.html', {"categories": categories})


def main_categories(request, category_slug):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=selected_category).order_by('-date_created')

    # If user is logged in, allow them to see liked posts; else skip
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        liked_posts = Like.objects.filter(user=user_profile).values_list('post_id', flat=True)
    else:
        liked_posts = []

    return render(request, 'categories/category_detail.html', {
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
        'liked_post_ids': liked_posts,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            caption = request.POST.get('caption')
            category_id = request.POST.get('category')
            if not caption or not category_id:
                return JsonResponse({'error': 'Caption and category are required'}, status=400)
            
            user_profile = UserProfile.objects.get(user=request.user)
            
            post = Post.objects.create(
                caption=caption,
                image=request.FILES.get('image'),
                category_id=category_id,
                user=user_profile
            )
            return JsonResponse({'success': True, 'post_id': post.id})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user.user != request.user:
        return redirect('pets:profile', username=request.user.username)
    
    post.delete()

    return redirect('pets:profile', username=request.user.username)

@login_required
def chat_index(request):
    chat_rooms = ChatRoom.objects.filter(users=request.user)
    categories = Category.objects.all()
    return render(request, "chat/chatIndex.html", {"ChatRoom": chat_rooms,'categories':categories})


@login_required
def chat_room(request, room_name):
    chatroom = get_object_or_404(ChatRoom, chat_name=room_name)
    categories = Category.objects.all()
    chatroom_data = {
        "id": chatroom.id,
        "chat_name": chatroom.chat_name,
        "users": list(chatroom.users.values("id", "username")),
    }
    messages = Message.objects.filter(chat_room_id=chatroom.id)
    chat_rooms = ChatRoom.objects.filter(users=request.user)
    return render(
        request,
        "chat/chatRoom.html",
        {
            "chatroom_json": chatroom_data,
            "messages": messages,
            "ChatRoom": chat_rooms,
            "categories":categories,
        }
    )


@login_required
def create_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        room_name = data.get("chat_name")
        chat, created = ChatRoom.objects.get_or_create(chat_name=room_name)
        chat.users.add(request.user)  # Add user every time

        return JsonResponse({
            "success": True,
            "chat_name": room_name,
            "newly_created": created,
        })
    return JsonResponse({"success": False}, status=405)


@login_required
def add_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_name = data.get("chat_name")
        username = data.get("username")

        try:
            chat = ChatRoom.objects.get(chat_name=chat_name)
        except ChatRoom.DoesNotExist:
            return JsonResponse({"success": False, "error": "Chat room does not exist"}, status=400)

        try:
            user_obj = User.objects.get(username=username.strip())
            chat.users.add(user_obj)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": f"User {username} does not exist"}, status=400)

        return JsonResponse({"success": True, "message": f"User {username} added to {chat_name}"})
    
    return JsonResponse({"success": False}, status=405)


@login_required
def leave_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_name = data.get("chat_name")
        
        try:
            chat_room = ChatRoom.objects.get(chat_name=chat_name)
        except ChatRoom.DoesNotExist:
            return JsonResponse({"error": "Chat room not found"}, status=404)

        chat_room.users.remove(request.user)
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user=user)
    own_user_profile = UserProfile.objects.get(user=request.user)
    
    is_own_profile = (user == request.user)
    
    # Follow relationships
    is_following = Follow.objects.filter(
        follower=own_user_profile,
        followed=user_profile
    ).exists()
    
    following = user_profile.following.all() 
    followers = user_profile.followers.all()  
    
    context = {
        'user_profile': user_profile,
        'posts': Post.objects.filter(user=user_profile).order_by('-date_created'),
        'followers_count': followers.count(),
        'following_count': following.count(),
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        # Add other context variables...
    }
    return render(request, 'profile/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user_id=user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('pets:profile', username=request.user.username)  # Pass the username here
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile/edit_profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('pets:home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pets:profile', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_pet(request):
    user = request.user
    user_profile = UserProfile.objects.get(user_id=user.id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = user_profile
            pet.save()
            return redirect('pets:profile', username=request.user.username)
    else:
        form = PetForm()

    return render(request, 'pet/add_pet.html', {'form': form,"username":request.user.username})


@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if pet.owner.user.username != request.user.username:
        return redirect('pets:profile', username=request.user.username)  

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets:profile', username=request.user.username) 
    else:
        form = PetForm(instance=pet)

    return render(request, 'pet/edit_pet.html', {'form': form, "username": request.user.username})



@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.owner.user_id == request.user.id:
        pet.delete()
    return redirect('pets:profile',username=request.user.username)


@login_required
def add_follower(request):
    if request.method == "POST":
        data = json.loads(request.body)
        target_username = data.get("username")

        try:
            target_user = User.objects.get(username=target_username)
            target_profile = UserProfile.objects.get(user_id=target_user.id)
            current_profile = UserProfile.objects.get(user_id=request.user.id)

            if Follow.objects.filter(follower=current_profile, followed=target_profile).exists():
                Follow.objects.filter(follower=current_profile, followed=target_profile).delete()
                following = False
            else:
                Follow.objects.create(follower=current_profile, followed=target_profile)
                following = True

            follower_count = Follow.objects.filter(followed=target_profile).count()

            return JsonResponse({
                "success": True,
                "following": following,
                "followers": follower_count,
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


def view_pet(request,pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    context = {
        "pet": pet,
    }
    return render(request, "pet/view_pet.html", context)