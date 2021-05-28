
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('post/<str:post_id>', views.post, name='post'),
    path('add_post', views.add_post, name='add_post'),
    path('user/<str:user_id>', views.get_user, name='get_user'),
    path('follow/<str:user_id>', views.follow_user, name='follow_user'),
    path('following', views.following, name='following'),
    path('like/<str:post_id>', views.like_post, name='like_post')
]
