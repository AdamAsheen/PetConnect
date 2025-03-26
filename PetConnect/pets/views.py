from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import *
import json
import logging

def general_feed(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = Post.objects.all().order_by('-date_created')[:10]

    liked_posts = Like.objects.filter(user=user_profile, post__in=posts).values_list('post_id', flat=True)
    context_dict["liked_post_ids"] = set(liked_posts)  # Convert to a set for efficient lookups

    context_dict["posts"] = posts
    context_dict["comments"] = Comment.objects.filter(post__in=posts)
    
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


logger = logging.getLogger(__name__)
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