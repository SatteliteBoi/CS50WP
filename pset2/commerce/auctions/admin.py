from django.contrib import admin
from .models import User, Listing, Bid, Comment, WatchListItem, Category

# Register your models here.

admin.register(Listing, Comment, Bid)(admin.ModelAdmin)
