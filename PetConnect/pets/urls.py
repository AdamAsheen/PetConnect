# pets/urls.py

from django.urls import path
from . import views

app_name = "pets"

urlpatterns = [
    # Feeds
    path("home/", views.general_feed, name="home"),       
    path("following/", views.following_feed, name="following_feed"), 
    
    # Authentication/User Profile
    path('profile/<str:username>/', views.profile, name='profile'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # Pet Management
    path("add-pet/", views.add_pet, name="add_pet"),
    path("edit-pet/<int:pet_id>/", views.edit_pet, name="edit_pet"),
    path("delete-pet/<int:pet_id>/", views.delete_pet, name="delete_pet"),
    path("view-pet/<int:pet_id>/",views.view_pet,name="view-pet"),

    # Posts
    path("create-post", views.create_post, name="create-post"),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete-post'), 
    
    # Comments & Likes & followers
    path("add-comments", views.add_comment, name="add-comments"),
    path("add-likes", views.add_likes, name="add-likes"),
    path("remove-likes", views.remove_likes, name="remove-likes"),
    path("follower",views.add_follower, name="follower"),

    # Categories
    path("categories", views.show_categories, name="categories"),
    path("categories/<slug:category_slug>/", views.main_categories, name="category-detail"),

    # Chat
    path("chat", views.chat_index, name="chat"),
    path("create-chat", views.create_chat, name="create-chat"),
    path("add-user", views.add_user, name="add-user"),
    path("leave-chat", views.leave_chat, name="leave-chat"),
    path("<str:room_name>/", views.chat_room, name="room"),

]
