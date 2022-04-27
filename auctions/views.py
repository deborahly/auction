from ast import operator
from operator import methodcaller
from typing import List
# from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from .models import User, Listing, Watched, Bid, Comment, Auction
from .forms import CommentForm, ListingForm, BidForm

import operator


def index(request):
    listings = Listing.objects.all()
    active_listings = []
    
    for listing in listings:
        auction = listing.auction_set.get()
        
        if auction.status == "ACTIVE":
            active_listings.append(listing)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

# NEW VIEW
def closed(request):
    listings = Listing.objects.all()
    closed_listings = []
    for listing in listings:
        auction = listing.auction_set.get()
        if auction.status == "CLOSED":
            closed_listings.append(listing)

    return render(request, "auctions/closed.html", {
        "closed_listings": closed_listings
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
    categories = Listing.objects.values_list("category", flat=True).distinct()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

#NEW VIEW
def category(request,category):
    category_listings = Listing.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "category_listings": category_listings,
        "category": category
    })

# NEW VIEW
@login_required
def watchlist(request):
    if request.method == "POST":
        
        form = request.POST
        
        if form["watching"] == "add":    
            title = Listing.objects.get(title=form["listing"])
            w = Watched(user=request.user, title=title)
            w.save()

            return HttpResponseRedirect(reverse("listing", args=(title,)))

        elif form["watching"] == "remove":  
            title = Listing.objects.get(title=form["listing"])
            user = User.objects.get(username=request.user)
            w = Watched.objects.get(user=user, title=title)
            w.delete()

            return HttpResponseRedirect(reverse("listing", args=(title,)))

    else:
        return render(request, "auctions/watchlist.html", {
            "watched": Watched.objects.filter(user=request.user)
        })

# NEW VIEW
@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            form.instance.current_price = form.cleaned_data["starting_bid"]
            form.save()

            listing = Listing.objects.get(title=title)

            user = User.objects.get(username=request.user)

            auction = Auction(user=user, title=listing)
            auction.save()

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
    
    # comments = Comment.objects.filter(listing=listing_id)
    comments = listing.comments.filter(active=True)
    
    # bids = Bid.objects.filter(title=listing_id)
    # last_bid = bids.last()
    
    auction = Auction.objects.get(title=listing_id)

    # FORMS
    bid_form = BidForm(initial={"title": listing_id})
    comment_form = CommentForm
    
    try:
        watched = Watched.objects.get(user=request.user, title=listing_id)
               
    except:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            # "last_bid": last_bid,
            "auction": auction,
            "bid_form": bid_form,
            "comment_form": comment_form
        })

    else:    
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            # "last_bid": last_bid,
            "auction": auction,
            "watched": watched,
            "bid_form": bid_form,
            "comment_form": comment_form
        })

# NEW VIEW
@login_required
def bids(request):
    if request.method == "POST":
        # Get the forms
        bid_form = BidForm(request.POST)
        form = request.POST
        
        # Get the listing
        listing_id = form["listing"]
        listing = Listing.objects.get(id=listing_id)
        
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data["bid"]
        
            bids = Bid.objects.filter(listing=listing_id)
            last_bid = bids.last()
        
            if (last_bid and new_bid > last_bid.bid) or (not last_bid and new_bid >= listing.starting_bid):
                user = User.objects.get(username=request.user)
                b = Bid(bid=new_bid, listing=listing, user=user)
                b.save()
                
                listing.current_price = new_bid
                listing.save()

                return HttpResponseRedirect(reverse("listing", args=(title,)))
        
            else:
                return HttpResponseRedirect(reverse("error"))
        
        else:
            return HttpResponseRedirect(reverse("error"))

    if request.method == "GET":
        return render(request, "auctions/bids.html", {
            "bids": Bid.objects.filter(user=request.user)
        })

# NEW VIEW
@login_required
def close(request, id, title):
    if request.method == "POST":
        auction = Auction.objects.get(title=id)
        auction.status = "CLOSED"

        Watched.objects.filter(title=id).delete()
        
        bids = Bid.objects.filter(title=id)
        last_bid = bids.last()
        
        if last_bid == None:
            auction.save()

            return HttpResponseRedirect(reverse("listing", args=(title,)))

        else:    
            auction.winner = last_bid.user
            auction.save()

            return HttpResponseRedirect(reverse("listing", args=(title,)))

# NEW VIEW
@login_required
def comments(request, title):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        listing = Listing.objects.get(title=title)

        if comment_form.is_valid:
            # Create object but don't save yet
            new_comment = comment_form.save(commit=False)
            # Assign listing to the comment
            new_comment.listing = listing
            # Assign user to the comment
            new_comment.user = request.user
            # Save to the database
            new_comment.save()

            return HttpResponseRedirect(reverse("listing", args=(title,)))
        
        else:
            return HttpResponseRedirect(reverse("error"))

# NEW VIEW
def error(request):
    return render(request, "auctions/error.html")