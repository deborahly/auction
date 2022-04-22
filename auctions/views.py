from ast import operator
from operator import methodcaller
# from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from .models import User, Listing, Watched, Bid, Comment, Auction
from .forms import ListingForm, BidForm

import operator


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

# NEW VIEW
def categories(request):
    return render(request, "auctions/categories.html")

# NEW VIEW
def watchlist(request):
    if request.method == "POST":
        form = request.POST
        title = Listing.objects.get(title=form["listing"])
        w = Watched(user=request.user, title=title)
        w.save()

        return render(request, "auctions/watchlist.html", {
            "watched": Watched.objects.filter(user=request.user)
        })
    
    else:
        return render(request, "auctions/watchlist.html", {
            "watched": Watched.objects.filter(user=request.user)
        })

# NEW VIEW
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
            
    else:
        form = ListingForm
        return render(request, "auctions/create.html", {
        "form": form
        })

# NEW VIEW
def listing(request, title):
    listing = Listing.objects.get(title=title)
    listing_id = listing.id
    comments = Comment.objects.filter(title=listing_id)
    auction = Auction.objects.get(title=listing_id)

    # FORMS
    bid_form = BidForm(initial={"title": listing_id})
    
    try:
        watched = Watched.objects.get(user=request.user, title=listing_id)
               
    except:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "auction": auction,
            "bid_form": bid_form
        })
    
    else:    
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "auction": auction,
            "watched": watched,
            "bid_form": bid_form
        })

# NEW VIEW
def bids(request):
    if request.method == "POST":
        form = request.POST
        title = form["title"]

        listing = Listing.objects.get(title=title)
        listing_id = listing.id
        
        bid_form = BidForm(request.POST)
        
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data["bid"]
        
        bids = Bid.objects.filter(title=listing_id)
        last_bid = Bid.objects.all().last().bid
        
        if new_bid > last_bid:
            user = User.objects.get(username=request.user)
            b = Bid(bid=new_bid, title=listing, user=user)
            b.save()
            return HttpResponseRedirect(reverse("listing", args=(title,)))
    
        else:
            return HttpResponseRedirect(reverse("error"))

# NEW VIEW
def error(request):
    pass