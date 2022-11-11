from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def upload_path(instance, filename):
    return '/'.join(['images', str(instance.name)])

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']
    
    def __str__(self):
        return str(self.id)


class Gallery(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=555)
    image = models.ImageField(upload_to=upload_path)
    image_size = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
