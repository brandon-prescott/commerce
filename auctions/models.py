from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    image_url = models.CharField(max_length=1500)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user") # One user can be associated with many listings
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category") # One category can be associated with many listings
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title