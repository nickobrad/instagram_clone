from cloudinary.uploader import upload
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=CASCADE)
    profile_photo = models.ImageField(upload_to = 'profile_pictures/', default = 'photo.jpg', blank = True)
    bio = models.TextField(blank=True) 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField(User, related_name = 'following', blank= True)
    followers = models.ManyToManyField(User, related_name= 'followers', blank= True)

    def __str__(self) -> str:
        return self.user.username 

    def save_profile(self):
        return self.save()

    def delete_profile(self):
        return self.delete()

    @classmethod
    def update_profile(cls, profile_id, new_bio):
        profile = cls.objects.filter(id = profile_id).update(bio = new_bio)
        return profile

    @classmethod
    def search_by_username(cls,search_term):
        users = cls.objects.filter(user__username__icontains = search_term)
        return users

    def get_absolute_url(self):
        return reverse('myprofile', args=(str(self.pk)))

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

    def save_image(self):
        return self.save()

    def delete_image(self):
        return self.delete()

    @classmethod
    def update_image_name(cls, image_id, new_name):
        image = cls.objects.filter(id = image_id).update(image_name = new_name)
        return image

    class Meta:
        ordering = ['-date_published']
    

class Comment(models.Model):
    post = models.ForeignKey(Image, on_delete=CASCADE, related_name='comments')
    posted_by = models.ForeignKey(Profile, on_delete=CASCADE)
    body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.post.image_name, self.posted_by.username)

    def save_comment(self):
        return self.save()

    def delete_comment(self):
        return self.delete() 

    @classmethod
    def update_comment(cls, comment_id, new_body):
        comment = cls.objects.filter(id = comment_id).update(body = new_body)
        return comment
