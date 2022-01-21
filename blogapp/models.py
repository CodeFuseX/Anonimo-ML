from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.timezone import now


class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.ForeignKey(User, blank=True, null=True, on_delete= models.CASCADE)
    body = RichTextField(blank=True, null=True)
    liked = models.ManyToManyField(User,blank=True, related_name='liked')
    slug = models.CharField(max_length=130)
    
    #created = models.DateTimeField(auto_now_add=True, default=True)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
        ('Like','Like'),
        ('Unlike', 'Unlike'),
    )

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)


class Badges(models.Model):
    post = models.CharField(max_length=1000)
    gold = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    bronze = models.IntegerField(default=0)
    platinum = models.IntegerField(default=0)


class Report(models.Model):
    post_title = models.CharField(max_length=1000)
    post_content = models.CharField(max_length=5000)
    reason = models.CharField(max_length=1000)
