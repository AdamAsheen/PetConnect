from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('categories/', views.categories, name='categories'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login_view, name='login'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('signup/', views.signup, name='signup'),
]
