from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    imgurl = models.CharField(max_length=500, blank = True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=50000)
    category = models.CharField(max_length=50, blank=True, null=True)
    highestbidder = models.CharField(max_length=80, default=poster)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.price} by {self.poster}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidprice = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.bidder} bidded {self.bidprice}"

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