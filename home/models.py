from django.db import models
from django.contrib.auth.models import User
import datetime
import os

from django.db.models.fields.related import ForeignKey
# Create your models here.
class SignUp(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.username

    empAuth_objects = models.Manager()


class Resources(models.Model):
    img = models.ImageField(upload_to="blog-img/", default="")
    title = models.CharField(max_length=155)
    content = models.TextField()
    link=models.CharField(max_length=500)



def filepath(request,filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('profile/',filename)

class editProfile(models.Model):
    profile_user=models.ForeignKey(User, blank=True, null=True, on_delete= models.CASCADE)
    bio = models.TextField()
    instagram = models.CharField(max_length=155)
    hobbies = models.CharField(max_length=155)
    image = models.ImageField(upload_to=filepath, null=True, blank = True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers") 
    key = models.CharField(max_length=150)


class FollowersCount(models.Model):
    follower = models.CharField(max_length=1000)
    user = models.CharField(max_length=1000)

    def __str__(self):
        return self.user
        

class FriendRequest(models.Model):
    from_user = models.CharField(max_length=1000)
    to_user = models.CharField(max_length=1000)
        

class Bank(models.Model):
    profile_user = ForeignKey(User, blank=True, null=True, on_delete= models.CASCADE )
    account_bal = models.IntegerField(default=0)