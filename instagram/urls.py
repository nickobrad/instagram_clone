"""insta_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from . import views
from .views import ProfileDetailView, ProfileListView, comment, follow_unfollow_profile, logout_view, search_results, loginuser, my_profile, register, LikeView, follow_user, HomeView, PostDetailView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout


urlpatterns = [
    path('register/', register, name = 'register'), 
    path('', loginuser, name = 'login' ),
    path('home', HomeView, name = 'home'),
    path('post/<int:pk>', PostDetailView, name = 'postdetails'), 
    path('comment/post/<int:pk>', comment, name = 'comment'), 
    # path('profile/<int:pk>', ProfileDetailView.as_view(), name = 'my_profile'),
    path('profile/<int:pk>', my_profile, name = 'myprofile'),
    path('like/<int:pk>', LikeView, name = 'like_post'),
    path('ptf', ProfileListView.as_view(), name = 'profile_list'),
    path('follow/<str:username>', follow_user, name = 'follow'),
    path('follow', follow_unfollow_profile, name = 'ffview'),
    url(r'^search/', search_results, name = 'search_users'),
    path('logout', logout_view, name='logout'),

    # path('home', home, name = 'home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 