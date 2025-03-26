from django.urls import path,include
from . import views

urlpatterns = [
    path("home/",views.general_feed,name="home"),
    path("add-comments",views.add_comment,name="add-comments"),
    path("add-likes",views.add_likes,name="add-likes"),
    path("remove-likes",views.remove_likes,name="remove-likes"),
]