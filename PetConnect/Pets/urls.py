from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'), 
    path('login/', views.login_view, name='login'), 
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'), 
    path('pet/<int:pet_id>/like/', views.like_pet, name='like_pet'), 
]