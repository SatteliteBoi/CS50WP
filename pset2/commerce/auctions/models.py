from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidprice = models.IntegerField()
    def __str__(self):
        return f"{self.bidder} bidded {self.bidprice}"
        
class Listing(models.Model):
    startingprice = models.IntegerField()
    title = models.CharField(max_length=50)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    imgurl = models.CharField(max_length=500, blank = True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=50000)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL,related_name="itemsincategory", blank=True, null=True)
    open = models.BooleanField(default=True)
    bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, related_name="listbiddings", blank=True, null=True)
    def __str__(self):
        return f"{self.title}: by {self.poster}"

class BidListings(models.Model):
    bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name="bidlistings", blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingbids")

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.commenter} said {self.listing}"

class WatchListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listed = models.BooleanField()
    listingid = models.ForeignKey(Listing, on_delete=models.CASCADE)