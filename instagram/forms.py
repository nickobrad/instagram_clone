from django import forms
from django.core import validators
from django.db.models import fields
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Comment, Profile


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password1','password2' ]

        widgets = {
            'first_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"First Name", 'label': 'First Name'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Second Name", 'label': 'Second Name'}),
            'email':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Email Address", 'label': 'Email Address'}),
            'username':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Username", 'label': 'Username'}),
            'password1':forms.PasswordInput(attrs = {'class':'form-control names','type':'password', 'placeholder':"Password", 'label': 'Password'}),
            'password2':forms.PasswordInput(attrs = {'class':'form-control names', 'placeholder':"Confirm Password", 'label': 'Confirm Password'}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image_name', 'image_caption', 'image')

        widgets = {
            'image': forms.FileInput(attrs = {'class': 'form-control', 'type': 'file'}),
            'image_name': forms.TextInput(attrs = {'class': 'form-control form-floating mb-3', 'Placeholder': 'Image Title'}),
            'image_caption': forms.Textarea(attrs = {'class': 'form-control','Label': '', 'Placeholder': 'Image Description'}),
            # 'posted_by': forms.TextInput(attrs = {'class': 'form-control','id': 'user', 'value': '', 'type': 'hidden'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'posted_by', 'post')

        widgets = {
            'body': forms.TextInput(attrs={'class':"form-control comment", 'placeholder':"Add a comment...", 'aria-label':"Add a comment..."}),
            'posted_by': forms.TextInput(attrs = {'class': 'form-control','id': 'user', 'value': '', 'type': 'hidden'}),
            'post': forms.TextInput(attrs = {'class': 'form-control','id': 'post', 'value': '', 'type': 'hidden'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio','user') 

        widgets = {
            'bio': forms.Textarea(attrs={'class':"form-control bio", 'label': 'Bio', 'placeholder':"Add your bio...", 'aria-label':"Add your bio..."}),
            'user': forms.TextInput(attrs = {'class': 'form-control','id': 'user', 'value': '', 'type': 'hidden'}),
            'profile_photo': forms.FileInput(attrs = {'class': 'form-control', 'type': 'file'})
        }