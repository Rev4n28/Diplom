from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=500, blank=True)
    username = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username


class Password(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, default="123456")
    title = models.CharField(max_length=200)
    password = models.TextField(max_length=200)

    def __str__(self):
        return self.title
