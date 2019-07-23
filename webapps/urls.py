"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import grumblr.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('register', grumblr.views.register, name="register"),
    path('logout', auth_views.logout_then_login, name='logout'),
    path('profile', grumblr.views.profile, name='profile'),
    path('', grumblr.views.post_new, name='home'),
    path('edit_profile', grumblr.views.edit_profile, name='edit_profile'),
    path('reset_pwd/<str:username>/<slug:token>/', grumblr.views.reset_pwd, name='reset_pwd'),
    path('send_email', grumblr.views.send_email, name='send_email'),
    path('confirm_register/<str:username>/<slug:token>/', grumblr.views.confirm_register, name="confirm_register"),
    path('get_photo/<str:username>', grumblr.views.get_photo, name="get_photo"),
    path('follow_stream', grumblr.views.follow_stream, name="follow_stream"),
    path('follow/<str:username>', grumblr.views.follow, name="follow"),
    path('unfollow/<str:username>', grumblr.views.unfollow, name="unfollow"),
    path('comment/<int:post_id>', grumblr.views.comment, name="comment"),
    path('get_new_posts/<int:post_id>', grumblr.views.get_new_posts, name="get_new_posts"),
]
