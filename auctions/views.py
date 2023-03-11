from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Category, Listing
from .forms import CreateListingForm, BidForm


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "all_listings": all_listings
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


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        # Create a copy of the POST request to make it mutable
        # This was done so the user id can be added inside this view
        form_data = request.POST.copy()
        form_data["user"] = request.user.id
        form = CreateListingForm(form_data)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm
        })


def listing(request, listing_id):
    if request.method == "POST":
        form_data = request.POST.copy()
        form_data["user"] = request.user.id
        form_data["listing"] = int(listing_id)
        
        listing = Listing.objects.get(id=int(listing_id))
        current_price = listing.price
        print(form_data["amount"])

        if float(form_data["amount"]) <= current_price:
            owner = User.objects.get(id=listing.user.id)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "form": BidForm,
                "owner_username": owner.username,
                "category": listing.category,
                "bid_error": 1 
            })
        else:
            # TO DO: Add bid to datbase and overwrite current bid on listing
            return redirect(index)
    else:
        listing = Listing.objects.get(id=int(listing_id))
        owner = User.objects.get(id=listing.user.id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": BidForm,
            "owner_username": owner.username,
            "category": listing.category,
            "bid_error": 0
        })
    

def categories(request):
    return redirect(index)


def watchlist(request):
    return redirect(index)