from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment, WatchListItem, Category
from django.db.models import Q
from django.db import transaction

class ListingForm(forms.Form):
    startingprice = forms.IntegerField(label="Starting Price")
    title = forms.CharField(label="Name of Listing")
    description = forms.CharField(label="Description")
    imgurl = forms.CharField(label="Image URL", required=False)
    category = forms.CharField(label="Category", required=False)
    bidid = forms.IntegerField(widget=forms.HiddenInput, required=False)

class Bidform(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    bidprice = forms.IntegerField(label="Bid price")
    listid = forms.UUIDField(widget=forms.HiddenInput())

class CloseForm(forms.Form):
    listid = forms.UUIDField(widget=forms.HiddenInput())
    bidid = forms.IntegerField(widget=forms.HiddenInput, required=False)
    listid = forms.UUIDField(widget=forms.HiddenInput())

class CommentingForm(forms.Form):
    comment = forms.CharField(label="Comment")
    listid = forms.UUIDField(widget=forms.HiddenInput())

class WatchListForm(forms. Form):
    user = forms.CharField(widget=forms.HiddenInput, required=False)
    listid = forms.UUIDField(widget=forms.HiddenInput, required=False)
    listed = forms.BooleanField(widget=forms.HiddenInput, required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "lst":  Listing.objects.filter(open = True)
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
            catobj = Category.objects.filter(name = lst['category']).first()
            if catobj==None:
                catobj=Category(name=lst['category'])
                catobj.save()
            bid = Bid.objects.filter(id = lst["bidid"]).first()
            listing = Listing(title=lst["title"], bid=bid, startingprice=lst["startingprice"], description=lst["description"], poster=request.user, category=catobj, imgurl=lst["imgurl"])
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/createlisting.html",{
            "form": f
            })
    else:
        return HttpResponse("Whos joe")

def getlisting(request, inputlistid):
    
    wlitem = WatchListItem.objects.filter(listingid=inputlistid).first()
    addedtowatch = True
    if wlitem == None or wlitem.listed == False:
        addedtowatch = False

    closed = False
    winner = False
    close = None
    commentingform = CommentingForm(initial={'listid': inputlistid})
    listobj = Listing.objects.filter(id=inputlistid).first()
    oldcomments = Comment.objects.filter(listing=listobj)
    obj = Listing.objects.filter(Q(id=inputlistid) & Q(open=True)).first()
    if obj is None:
        closed = True
        obj = Listing.objects.filter(id=inputlistid).first()
        if obj.bid is not None and obj.bid.bidder == request.user:
            winner = True
    else:
        bidid = None
        if(obj.bid != None):
            bidid = obj.bid.id
        close = CloseForm(initial={'listid': inputlistid, 'bidid': bidid})
    bform = Bidform(initial={'listid': inputlistid})
    wlf = WatchListForm(initial = {'listid': inputlistid, 'listed': not addedtowatch})
    return render(request, "auctions/listing.html",{
        "obj": obj,
        "form": bform,
        "isposter": (obj.poster == request.user),
        "close": close,
        "winner": winner,
        "closed": closed,
        "commentingform": commentingform,
        "oldcomments": oldcomments,
        "watchlistform": wlf,
        "addedtowatch": addedtowatch
    })

def bidupdate(request):
    if request.method == "POST":
        form = Bidform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            listing = Listing.objects.filter(id=data["listid"]).first()
            minprice = listing.startingprice
            if listing.bid is not None:
                minprice = listing.bid.bidprice

            if data["bidprice"] <= minprice:
                return HttpResponse("Error")
            else:
                bid = Bid(bidprice=data["bidprice"], bidder=request.user)
                bid.save()

                listing.bid = bid
                listing.save()

                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(form.data)            
    else:
        return HttpResponse("finnatrynagetdis")

def bidclose(request):
    if request.method == "POST":
        form = CloseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            listing = Listing.objects.filter(id= data["listid"]).first()
            listing.open = False
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(form.data)
    else:
        return HttpResponse("bidclose didn't get post")

def createcomment(request):
    if request.method == "POST":
        cform = CommentingForm(request.POST)
        if cform.is_valid():
            data = cform.cleaned_data
            listobj = Listing.objects.filter(id = data['listid']).first()
            commentobj = Comment(commenter=request.user, comment = data['comment'], listing = listobj)
            commentobj.save()
            return HttpResponseRedirect("listing/"+str(data["listid"]))
        else:
            return HttpResponse(commentobj.data)
    else:
        return HttpResponse("createcomment didn't get post")

def watch(request):
    if request.method == "POST":
        wlform = WatchListForm(request.POST)
        if wlform.is_valid():
            data=wlform.cleaned_data
            wli = WatchListItem.objects.filter(listingid=data['listid']).first()
            if wli == None:
                listobj = Listing.objects.filter(id = data['listid']).first()
                wli = WatchListItem(user= request.user, listingid=listobj)
            wli.listed=data['listed']
            wli.save()
            return HttpResponseRedirect("listing/"+str(data["listid"]))
        else:
            return HttpResponse("invalid")
    else:
        return HttpResponse("didnt post watchlist")

def watchlist(request):
    if request.user.is_authenticated==False:
        HttpResponse("login bruv")
    watchlist=WatchListItem.objects.filter(listed=True, user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    lst = Category.objects.filter(~Q(name = ""))
    return render(request, "auctions/category.html", {
        "lst": lst
    })

def specificcategory(request, ctname):
    catobj=Category.objects.filter(name = ctname).first()
    lst = catobj.itemsincategory.filter(open = True)
    return render(request, "auctions/specificcategory.html", {
        "lst": lst
    })