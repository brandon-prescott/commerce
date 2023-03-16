from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Category, Listing, Bid, Watchlist
from .forms import CreateListingForm, BidForm


def index(request):
    all_listings = Listing.objects.all().order_by("-time")
    return render(request, "auctions/index.html", {
        "heading": "Active Listings",
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
            # Save form data to database
            new_listing = Listing(
                user = User.objects.get(id=request.user.id),
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                image_url = form.cleaned_data["image_url"],
                price = form.cleaned_data["price"],
                category = form.cleaned_data["category"]
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
        form = BidForm(request.POST)
        if form.is_valid():
            # Get data
            amount = form.cleaned_data["amount"]
            listing_id = int(request.POST["listing_id"])
            listing = Listing.objects.get(id=int(listing_id))
            current_price = listing.price

            # Validate data
            if amount <= current_price:
                return render(request, "auctions/error.html", {
                    "message": "Bid must exceed the current listing price",
                    "code": "400"
                })
            
            seller = User.objects.get(id=listing.user.id)
            seller_id = seller.id
            user_id = request.user.id

            if user_id == seller_id:
                return render(request, "auctions/error.html", {
                    "message": "Seller cannot bid on their own item",
                    "code": "400"
                })
            
            # Create new bid entry in database
            new_bid = Bid(
                user = User.objects.get(id=request.user.id),
                listing = listing,
                amount = amount
            )
            new_bid.save()

            # Update current price in database
            listing.price = amount
            listing.save()

        return redirect(f"/listing/{listing_id}")
    else:
        return redirect(index)


# known bug: trying to type in a url path with a string in causes a value conversion error with the int funciton - Potentially use a Try Exception case to handle
def categories(request, category_arg):
    all_categories = Category.objects.all().order_by("category_name")

    if category_arg == "all":
        return render(request, "auctions/categories.html", {
            "all_categories": all_categories
        })
    
    list_categories_by_id = []
    for category in all_categories:
        list_categories_by_id.append(category.id)

    if int(category_arg) not in list_categories_by_id:
        return render(request, "auctions/error.html", {
            "message": "Category does not exist",
            "code": "404"
        })
    
    category_listings = Listing.objects.filter(category=int(category_arg))
    category_name = Category.objects.get(id=int(category_arg))
    return render(request, "auctions/index.html", {
        "heading": f"Active Listings: {category_name}",
        "all_listings": category_listings
    })


@login_required(login_url="auctions:login")
def watchlist(request):

    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        watchlist_action = request.POST["watchlist_action"]

        if watchlist_action not in ["add", "remove"]:
            return render(request, "auctions/error.html", {
            "message": "Bad request",
            "code": "404"
        })

        if watchlist_action == "add":
            new_watchlist = Watchlist(
                user = User.objects.get(id=request.user.id),
                listing = Listing.objects.get(id=listing_id),
            )
            new_watchlist.save()
            return redirect(listing, listing_id=listing_id)
        
        if watchlist_action == "remove":
            user_id = request.user.id
            filter = {"user": user_id, "listing": listing_id}
            Watchlist.objects.filter(**filter).delete()
            return redirect(listing, listing_id=listing_id)

    else:
        user_id = request.user.id
        watchlist = Watchlist.objects.filter(user=user_id).order_by("-time")

        watchlist_listings = []
        for item in watchlist:
            watchlist_listings.append(item.listing)

        return render(request, "auctions/index.html", {
            "heading": "Watchlist",
            "all_listings": watchlist_listings
        })