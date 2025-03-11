from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'), 
    path('login/', views.login_view, name='login'), 
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/', views.profile, name='profile'),
    path('categories/', views.categories, name='categories'),
    path('chat/', views.chat, name='chat'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]