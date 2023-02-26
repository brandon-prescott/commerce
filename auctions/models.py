from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Inherited from Django implementation
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    image_url = models.CharField(max_length=1500)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_user") # One user can be associated with many listings
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_category") # One category can be associated with many listings
    time = models.DateTimeField(auto_now_add=True) # Auto timestamp

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user") # One user can be associated with many bids
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_listing") # One listing can be associated with many bids
    amount = models.FloatField()
    time = models.DateTimeField(auto_now_add=True) # Auto timestamp

    def __str__(self):
        return f"{str(self.user)}_{str(self.listing)}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user") # One user can be associated with many comments
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing") # One listing can be associated with many comments
    comment = models.CharField(max_length=400)
    time = models.DateTimeField(auto_now_add=True) # Auto timestamp

    def __str__(self):
        return f"{str(self.user)}_{str(self.listing)}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="watchlist_user") # One user can have many 'watches'
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="watchlist_listing") # One listing can be watched many times

    def __str__(self):
        return f"{str(self.user)}_{str(self.listing)}"
