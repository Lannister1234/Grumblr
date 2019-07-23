from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    text = models.CharField(max_length=42)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=42)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    photo = models.ImageField(default="images/users/default.jpg", upload_to="images/users/", blank=True)
    bio = models.CharField(max_length=420, default="Write something to introduce yourself")
    followed = models.ManyToManyField(User, blank=True, related_name='follow_map')

    def __str__(self):
        return self.first_name