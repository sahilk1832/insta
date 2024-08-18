from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from datetime import datetime

User = get_user_model()

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images/', default='blanck_profile_picture.jpg')
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True,blank=True)
    no_of_followers = models.IntegerField(default=0)
    no_of_following = models.IntegerField(default=0)
    
    
   
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    
    def _str_(self):
        return self.caption

    def increment_like(self):
        self.no_of_likes += 1
        self.save()

class Likes(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    comments = models.CharField(max_length=200,default="comments")
    created_at = models.DateTimeField(default=datetime.now)
    
    
   
