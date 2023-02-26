from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist # Database tables

# Register your models here.
# This allows a superuser to interact with the database on the admin site
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)