from cloudinary.uploader import upload
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.deletion import CASCADE
# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=CASCADE)
    profile_photo = models.ImageField(upload_to = 'profile_pictures/')
    bio = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField(User, related_name = 'following', blank= True)

    def profiles_posts(self):
        self.image_set.all() 

    def __str__(self) -> str:
        return self.user.username

    @classmethod
    def search_by_username(cls,search_term):
        users = cls.objects.filter(user__username__icontains = search_term)
        return users

class Image(models.Model):
    image_name = models.CharField(max_length=50)
    image_caption = models.TextField()
    image = CloudinaryField('image')
    posted_by = models.ForeignKey(Profile, on_delete=CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes') 

    def all_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.image_name)

    class Meta:
        ordering = ['-date_published']
    

class Comment(models.Model):
    post = models.ForeignKey(Image, on_delete=CASCADE, related_name='comments')
    posted_by = models.ForeignKey(User, on_delete=CASCADE)
    body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.post.image_name, self.posted_by.username)

class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    another_user = models.ManyToManyField(User, related_name = 'another_user')

    def __str__(self) -> str:
        return self.user.username