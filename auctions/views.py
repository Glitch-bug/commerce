from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Listing, WatchList, Bid


def index(request):
    listings = Listing.objects.all()
    print(listings)
    context = {'listings': listings}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == 'POST':
        # assign form answers to variables
        title = request.POST['title']
        description = request.POST['description']
        min_bid = request.POST['min_bid']
        image = request.FILES.get('image')

        # Create and save a new Bid 
        bid = Bid(owner=request.user, amount=min_bid)
        bid.save()
        
        # Create and save a new Listing
        listing = Listing(owner=request.user, title=title, description=description, cur_bid=bid, image=image)
        listing.save()
        return redirect('auctions:index')
    else:
        return render(request, 'auctions/new_listing.html')

def listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    return render(request, 'auctions/listing.html', {'listing': listing})

def add_watchlist(request, pk):
    listing = Listing.objects.get(pk=pk)
    if WatchList.objects.filter(owner=request.user, listing=listing):
        #TODO: Add message to say duplication not allowed
        return redirect('auctions:index')
    #TODO: Add message to say item added to watchlist
    watchlist = WatchList(owner=request.user, listing=listing)
    watchlist.save()
    return redirect('auctions:index')

def watchlist(request):
    watchlist = WatchList.objects.filter(owner=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist':watchlist})

def bid(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(pk=pk) 
        bid = listing.cur_bid
        new_bid = int(request.POST['new_bid'])
        if new_bid > bid.amount:  
            bid.amount = request.POST['new_bid']
            bid.owner  = request.user
            bid.date_added = timezone.now()
            bid.save()
    return redirect('auctions:listing', pk)