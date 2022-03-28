from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    min_bid = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the model"""
        return f"{self.title[:50]}"

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)