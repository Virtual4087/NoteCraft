from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("register", views.registerUser, name="register"),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path('image2text', views.image2text, name="image2text"),
    path('text2studMat', views.text2studMat, name="text2studMat"),
    path("chapter", views.chapter, name="chapter"),
    path("test", views.test, name="test"),
    path("myChapters", views.myChapters, name="myChapters"),
]
