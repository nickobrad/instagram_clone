from django.contrib import admin
from .models import Image, Comment, Profile

class UserFollow(admin.ModelAdmin):
    filter_horizontal =('following','followers')

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Profile, UserFollow)
