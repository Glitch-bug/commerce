from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Listing, WatchList


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        min_bid = request.POST['min_bid']
        image = request.FILES.get('image')
        listing = Listing(owner=request.user, title=title, description=description, min_bid=min_bid, image=image)
        listing.save()
        return redirect('auctions:index')
    else:
        return render(request, 'auctions/new_listing.html')

def listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    return render(request, 'auctions/listing.html', {'listing': listing})

def watchlist(request, pk):
    listing = Listing.objects.get(pk=pk)
    watchlist = WatchList(owner=request.user, listing=listing)
    return redirect('auctions:index')