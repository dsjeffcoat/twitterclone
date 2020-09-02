from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class TwitterUser(AbstractUser):
    display_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    tweets = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name
