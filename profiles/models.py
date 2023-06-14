from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/')
