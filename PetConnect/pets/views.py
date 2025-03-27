from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import *
import json

def general_feed(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all().order_by('-date_created')[:10]
    categories = Category.objects.all()

    liked_posts = Like.objects.filter(user=user_profile, post__in=posts).values_list('post_id', flat=True)
    context_dict["liked_post_ids"] = set(liked_posts)  # Convert to a set for efficient lookups

    context_dict["posts"] = posts
    context_dict["comments"] = Comment.objects.filter(post__in=posts)
    context_dict["categories"] = categories
    
    return render(request, 'home.html', context_dict)


def following_feed(request):
    user = request.user
    following = Follower.objects.filter(follower=user).values_list('followed', flat=True)
    posts = Post.objects.filter(user__id__in=following).order_by('-date_created')[:10]
    return render(request, 'home.html', {'posts': posts})

def add_likes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_id = data.get("post-id")
            
            post = Post.objects.get(id=post_id)

            user = request.user
            user_profile = UserProfile.objects.get(user = user.id)
            existing_like = Like.objects.filter(user=user_profile,post=post).first()

            if not existing_like:
                Like.objects.create(user=user_profile,post=post)
            
            new_like_count = post.likes.count()
            

            return JsonResponse({"success": True, "new_like_count": new_like_count})

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def remove_likes(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                post_id = data.get("post-id")
            
                post = Post.objects.get(id=post_id)

                user = request.user
                user_profile = UserProfile.objects.get(user_id = user.id)
                existing_like = Like.objects.filter(user=user_profile,post=post).first()

                if existing_like:
                    liked = Like.objects.get(user=user_profile,post=post)
                    liked.delete()
            
                new_like_count = post.likes.count()
            

                return JsonResponse({"success": True, "new_like_count": new_like_count})

            except Post.DoesNotExist:
                return JsonResponse({"error": "Post not found"}, status=405)
            except json.JSONDecodeError:
              return JsonResponse({"error": "Invalid JSON"}, status=400)

        return JsonResponse({"error": "Invalid request method"}, status=405)


def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            comment_text = data.get("comment-content")
            post_id = data.get("post-id")

            post = Post.objects.get(id=post_id)
            
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "User is not authenticated"}, status=401)
            
            user_profile = UserProfile.objects.get(user=user)

            comment = Comment.objects.create(user=user_profile, post=post, comment_text=comment_text)
            
            username = user_profile.user.username
            return JsonResponse({
                "success": True,
                "username": username,
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
    return render(request,'categories.html',{"categories":categories})
    
def main_categories(request,category_slug):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=selected_category).order_by('-date_created')
    user = request.user
    user_profile = UserProfile(user_id = user.id)
    liked_posts = Like.objects.filter(user =user_profile)
    liked_post_ids = liked_posts.values_list('post_id', flat=True)
    
    return render(request, 'category_detail.html', {
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
        'liked_post_ids':liked_post_ids
    })


def create_post(request):
    if request.method == 'POST':
        try:
            # Validate required fields
            caption = request.POST.get('caption')
            category_id = request.POST.get('category')
            
            if not caption or not category_id:
                return JsonResponse({'error': 'Caption and category are required'}, status=400)
            
            # Get user profile
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Create post
            post = Post.objects.create(
                caption=caption,
                image=request.FILES.get('image'),  # Optional image
                category_id=category_id,
                user=user_profile
            )
            
            return JsonResponse({'success': True, 'post_id': post.id})
            
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def chat_index(request):
    chat_rooms = ChatRoom.objects.filter(users=request.user)
    return render(request, "chat/chatIndex.html", {"ChatRoom": chat_rooms})

def chat_room(request, room_name):
    chatroom = get_object_or_404(ChatRoom, chat_name=room_name)

    chatroom_data = {
        "id":chatroom.id,
        "chat_name":chatroom.chat_name,
        "users":list(chatroom.users.values("id","username")),
    }

    messages = Message.objects.filter(chat_room_id=chatroom.id)
    chat_rooms = ChatRoom.objects.filter(users=request.user)

    return render(request, "chat/chatRoom.html", {"chatroom_json": chatroom_data, "messages": messages,"ChatRoom":chat_rooms})



def create_chat(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success":False,"error":"Not authenticated"},status = 403)

    if request.method == "POST":
        data = json.loads(request.body)
        room_name = data.get("chat_name")

        chat, created = ChatRoom.objects.get_or_create(chat_name=room_name)
        chat.users.add(request.user)  # Add user every time

        print("test")

        return JsonResponse({
            "success": True,
            "chat_name": room_name,
            "newly_created": created,
        })
    return JsonResponse({"success": False}, status=405)

def add_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        chat_name = data.get("chat_name")
        username = data.get("username")  # Single username

        try:
            chat = ChatRoom.objects.get(chat_name=chat_name)
        except ChatRoom.DoesNotExist:
            return JsonResponse({"success": False, "error": "Chat room does not exist"}, status=400)

        try:
            user = User.objects.get(username=username.strip())
            chat.users.add(user)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": f"User {username} does not exist"}, status=400)

        return JsonResponse({"success": True, "message": f"User {username} added to {chat_name}"})
    
    return JsonResponse({"success": False}, status=405)


def leave_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_name = data.get("chat_name")
        
        user_object = request.user

        try:
            chat_room = ChatRoom.objects.get(chat_name=chat_name)
        except ChatRoom.DoesNotExist:
            return JsonResponse({"error": "Chat room not found"}, status=404)


        chat_room.users.remove(user_object)
        

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
