import re
from cloudinary.uploader import add_tag
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls.base import reverse
from .forms import ProfileForm, RegistrationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Followers, Image, Comment, Profile
from .forms import ImageForm, CommentForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from itertools import chain


# Create your views here.
def register(request):
    rgf = RegistrationForm()
    if request.method == 'POST':
        rgf = RegistrationForm(request.POST)
        if rgf.is_valid():
            rgf.save()
            user = rgf.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    return render(request, 'authentication/register.html', {'rgf': rgf})


def loginuser(request):
 
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'authentication/login.html')

class ProfileListView(ListView):
    model = Profile
    template_name = 'others/ptf.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user = self.request.user)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'others/profile.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk = pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user = self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False

        form = ImageForm()
        form2 = ProfileForm()
        
        context['follow'] = follow
        context['form'] = form
        context['form2'] = form2
        return context


def my_profile(request, pk):

    form = ImageForm()
    form2 = ProfileForm()

    view_profile = Profile.objects.get(pk = pk)
    my_profile = Profile.objects.get(user = request.user)

    if view_profile.user in my_profile.following.all():
        follow = True
    else:
        follow = False

    pictures = Image.objects.filter(posted_by = pk).all()
    profile = Profile.objects.get(id = pk)

    current_user = request.user

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.posted_by = my_profile
            post.save()
            return redirect('home')
    else:
        form = ImageForm()
    
    if request.method == 'POST':
        form2 = ProfileForm(request.POST, request.FILES)
        if form2.is_valid():
            form2.save()
            return HttpResponseRedirect('profile')
        else:
            form2 = ProfileForm()

    return render(request, 'others/profile.html', {'form': form, 'form2':form2, 'posts': pictures, 'profile': profile, 'follow': follow, 'user': current_user})

def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user = request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk = pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile_list')

def HomeView(request):

    # Get logged in user

    profile = Profile.objects.get(user = request.user)

    # Check who we are following
    users = [user for user in profile.following.all()]

    # Initial values for variables
    posts = []
    qs = None

    # Get the posts of people who we are following
    for u in users:
        p = Image.objects.filter(posted_by = u.id).all()
        # p_posts = p.post_set.all()
        posts.append(p)

    # My posts
    my_posts = Image.objects.filter(posted_by = request.user.id).all()
    posts.append(my_posts)

    # Sort and chain querysets and unpack the posts list
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse = True, key = lambda obj:obj.date_published)

    object_list = Image.objects.all()

    form = CommentForm()

    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    #     else:
    #         form = CommentForm()

    profiles = Profile.objects.all().exclude(user = request.user)

    return render(request, 'others/home.html', {'form': form, 'object_list': qs, 'profiles': profiles})

def PostDetailView(request, pk):
    post = Image.objects.get(id = pk)
    total = post.all_likes()

    form = CommentForm()
    # current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))
        else:
            form = CommentForm()

    return render(request, 'others/post_details.html', {'form': form, 'object': post, 'all_likes': total})

def comment(request, pk):
    form = CommentForm()
    # current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = pk
            new_comment.posted_by = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))
        else:
            form = CommentForm()

    return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))


def LikeView(request, pk):
    post = get_object_or_404(Image, id = request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))

def follow_user(request, username):

    other_user = User.objects.get(username = username)
    session_user = request.user
    # session_user = request.session['user']
    get_user = User.objects.get(username = session_user)
    check_follower = Followers.objects.get(user = get_user.id)
    is_followed = False

    if other_user.username != session_user.username:
        if check_follower.another_user.filter(username = other_user).exists():
            add_user = Followers.objects.get(user = get_user)
            add_user.another_user.remove(other_user)
            is_followed = False
            return HttpResponseRedirect(reverse('profile'))
        else:
            add_user = Followers.objects.get(user = get_user)
            add_user.another_user.add(other_user)
            is_followed = True
            return HttpResponseRedirect(reverse('profile'))
    
    return HttpResponseRedirect(reverse('profile'))

def search_results(request):  

    if 'search_user' in request.GET and request.GET["search_user"]:
        search_term = request.GET.get("search_user")
        searched_users = Profile.search_by_username(search_term)
        message = f"{search_term}"
        title = search_term
        return render(request, 'others/search_results.html',{"message": message, "users": searched_users, 'title': title})
    else:
        message = "You haven't searched for any term"
        return render(request, 'others/search_results.html',{"message": message})

def logout_view(request):
    logout(request)
    return redirect('login')

# def post_of_following(request):

#     # Get logged in user

#     profile = Profile.objects.get(user = request.user)

#     # Check who we are following
#     users = [user for user in profile.following.all()]

#     # Initial values for variables
#     posts = []
#     qs = None

#     # Get the posts of people who we are following
#     for u in users:
#         p = Profile.objects.get(users = u)
#         p_posts = p.post_set.all()
#         posts.append(p_posts)

#     # My posts
#     my_posts = profile.profiles_posts()
#     posts.append(my_posts)

#     return render(request, 'others/home.html', {'posts': posts})
 