from django.urls import path,include

from .views import SignUpView,chatPage

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("chat/",chatPage, name="chat-page"),

]