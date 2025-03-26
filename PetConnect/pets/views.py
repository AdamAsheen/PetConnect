from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import *
import json

def general_feed(request):
    posts = Post.objects.all().order_by('-date_created')[:10] 
    return render(request, 'home.html', {'posts': posts})

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
            user_profile = UserProfile.objects.get(user_id = user.id)
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
                return JsonResponse({"error": "Post not found"}, status=404)
            except json.JSONDecodeError:
              return JsonResponse({"error": "Invalid JSON"}, status=400)

        return JsonResponse({"error": "Invalid request method"}, status=405)
