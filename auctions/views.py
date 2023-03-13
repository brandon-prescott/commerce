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
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Get data from form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]

            # Save to database
            new_listing = Listing(
                user = User.objects.get(id=request.user.id),
                title = title,
                description = description,
                image_url = image_url,
                price = price,
                category = category
            )
            new_listing.save()
            return redirect(index)
    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm
        })


def listing(request, listing_id):
    if request.method == "POST":
        # TO DO
        return redirect(index)
    else:
        listing = Listing.objects.get(id=int(listing_id))
        seller = User.objects.get(id=listing.user.id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": BidForm,
            "seller_username": seller.username,
            "category": listing.category,
        })
    
@login_required(login_url="auctions:login")
def bid(request):
    if request.method == "POST":
        # TO DO
        return redirect(index)
    else:
        # TO DO
        return redirect(index)


def categories(request):
    # TO DO
    return redirect(index)


def watchlist(request):
    # TO DO
    return redirect(index)