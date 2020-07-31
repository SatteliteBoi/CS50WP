from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comments

class ListingForm(forms.Form):
    title = forms.CharField(label="Name of Listing")
    startingprice = forms.IntegerField(label="Starting Price")
    description = forms.CharField(label="Description")
    imgurl = forms.CharField(label="Image URL", required=False)
    category = forms.CharField(label="Category", required=False)

class Bidform(forms.Form):
    bidprice = forms.IntegerField(label="Starting Price")
    listid = forms.UUIDField(widget=forms.HiddenInput())

def index(request):
    return render(request, "auctions/index.html", {
        "lst":  Listing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlisting(request):
    if request.method == "GET":
        return render(request, "auctions/createlisting.html",{
            "form": ListingForm()
        })
    elif request.method == "POST":
        f = ListingForm(request.POST)
        if f.is_valid():
            lst = f.cleaned_data
            listing = Listing(title=lst["title"], price=lst["price"], description=lst["description"], poster=request.user, category=lst["category"], imgurl=lst["imgurl"])
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/createlisting.html",{
            "form": f
            })
    else:
        return HttpResponse("Whos joe")

def getlisting(request, inputlistid):
    bform = Bidform(initial={'listid': inputlistid})
    return render(request, "auctions/listing.html",{
        "obj": Listing.objects.filter(id=inputlistid).first(),
        "form": bform
    })

def bidupdate(request):
    if request.method == "POST":
        form = Bidform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            listing = Listing.objects.filter(id= data["listid"]).first()
            if data["bidprice"] <= listing.price:
                return HttpResponse("Error")
            else:
                bid = Bid(bidprice=data["bidprice"], listing=listing, bidder=request.user)
                bid.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(form.data)            
    else:
        return HttpResponse("finnatrynagetdis")