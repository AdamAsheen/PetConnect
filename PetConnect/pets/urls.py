from django.urls import path,include
from . import views

urlpatterns = [
    path("home/",views.general_feed,name="home"),
    path("add-comments",views.add_comment,name="add-comments"),
    path("add-likes",views.add_likes,name="add-likes"),
    path("remove-likes",views.remove_likes,name="remove-likes"),
    path("create-post",views.create_post,name="create-post"),
    path("categories",views.show_categories,name="categories"),
    path("categories/<slug:category_slug>/", views.main_categories, name="category-detail"),
    path("chat",views.chat_index,name="chat"),
    path("create-chat",views.create_chat,name="create-chat"),
    path("add-user",views.add_user,name="add-user"),
    path("leave-chat",views.leave_chat,name="leave-chat"),
    path("<str:room_name>/",views.chat_room, name="room"),
]