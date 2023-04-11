from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Gallery model


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=555)
    image_uuid = models.CharField(max_length=200)
    image_size = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
