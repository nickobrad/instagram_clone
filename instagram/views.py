import re
from cloudinary.uploader import add_tag
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls.base import reverse
from .forms import ProfileForm, RegistrationForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  Image, Comment, Profile
from .forms import ImageForm, CommentForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from itertools import chain
from .email import send_welcome_email

def register(request):
    rgf = RegistrationForm()
    if request.method == 'POST':
        rgf = RegistrationForm(request.POST)
        if rgf.is_valid():
            rgf.save()
            user = rgf.cleaned_data.get('username')
            email = rgf.cleaned_data.get('email')
            send_welcome_email(user, email)
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

def my_profile(request, pk):

    form = ImageForm()
    form2 = ProfileForm() 

    view_profile = Profile.objects.get(pk = pk)
    my_profile = Profile.objects.get(user = request.user)

    if view_profile.user in my_profile.following.all():
        follow = True
    else:
        follow = False

    if my_profile.user in view_profile.followers.all():
        follower = True
    else:
        follower = False

    pictures = Image.objects.filter(posted_by = pk).all()
    profile = Profile.objects.get(id = pk)
    title = f'{profile.user}\'s Profile'


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
    
    return render(request, 'others/profile.html', {'form': form, 'form2':form2, 'posts': pictures, 'profile': profile, 'follow': follow, 'follower': follower,'user': current_user, 'title': title})

def edit_profile(request, pk):
    form2 = ProfileForm()
    if request.method == 'POST':
        form2 = ProfileForm(request.POST, request.FILES)
        if form2.is_valid():
            user = request.user
            profile_photo = request.FILES.get('photo')
            bio = request.POST.get('bio')
            profile = Profile(user = user, bio = bio, profile_photo = profile_photo)
            profile.save()
            return HttpResponseRedirect(reverse('myprofile', args=[int(pk)]))
        else:
            form2 = ProfileForm()
            return HttpResponseRedirect(reverse('myprofile', args=[int(pk)]))


def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user = request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk = pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)

        if my_profile.user in obj.followers.all():
            obj.followers.remove(my_profile.user)
        else:
            obj.followers.add(my_profile.user)

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

    profiles = Profile.objects.all().exclude(user = request.user)

    return render(request, 'others/home.html', {'form': form, 'object_list': qs, 'profiles': profiles})

def PostDetailView(request, pk):
    post = Image.objects.get(id = pk)
    total = post.all_likes()
    current_user = Profile.objects.get(user = request.user)
    title = post.image_name
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid(): 
            new_comment = form.save(commit = False)
            new_comment.post = Image.objects.get(pk = pk)
            new_comment.posted_by = Profile.objects.get(user = request.user)
            print(new_comment.posted_by)

            new_comment.save()
            return HttpResponseRedirect(reverse('postdetails', args = [int(pk)])) 
        else:
            form = CommentForm()

    return render(request, 'others/post_details.html', {'form': form, 'object': post, 'all_likes': total, 'user2': current_user, 'title': title})

def comment(request, pk):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = Image.objects.get(pk = pk)
            new_comment.posted_by = Profile.objects.get(user = request.user)
            print(new_comment.posted_by)
            new_comment.save()
            return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))
        else:
            form = CommentForm()

    return HttpResponseRedirect(reverse('postdetails', args = [int(pk)]))

def LikeView(request, pk):
    post = get_object_or_404(Image, id = request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

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

class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'others/update_profile.html' 

def logout_view(request):
    logout(request)
    return redirect('login')

# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'others/profile.html'

#     def get_object(self, **kwargs):
#         pk = self.kwargs.get('pk')
#         view_profile = Profile.objects.get(pk = pk)
#         return view_profile

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         view_profile = self.get_object()
#         my_profile = Profile.objects.get(user = self.request.user)
#         if view_profile.user in my_profile.following.all():
#             follow = True
#         else:
#             follow = False

#         form = ImageForm()
#         form2 = ProfileForm()
        
#         context['follow'] = follow
#         context['form'] = form
#         context['form2'] = form2
#         return context