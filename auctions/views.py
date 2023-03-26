from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, Bid, Watchlist, Comment
from .forms import CreateListingForm, BidForm, CommentForm


def index(request):
    all_listings = Listing.objects.filter(is_active=True).order_by("-time")
    number_of_listings = len(all_listings)
    return render(request, "auctions/index.html", {
        "heading": "Active Listings",
        "all_listings": all_listings,
        "number_of_listings": number_of_listings
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
    user_id = request.user.id
    filter = {"user": user_id, "listing": listing_id}

    if len(Watchlist.objects.filter(**filter)) == 1:
        in_watchlist = True
    else:
        in_watchlist = False
    
    current_listing = Listing.objects.get(id=int(listing_id))
    seller = User.objects.get(id=current_listing.user.id)
    comments = Comment.objects.filter(listing=current_listing.id).order_by("-time")
    bids = Bid.objects.filter(listing=current_listing.id)

    number_of_bids = len(bids)
    if number_of_bids > 0:
        highest_bid = bids.order_by("-amount")[0]
        winner_id = highest_bid.user.id
    else:
        highest_bid = None
        winner_id = None

    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "user_id": user_id,
        "in_watchlist": in_watchlist,
        "number_of_bids": number_of_bids,
        "winner_id": winner_id,
        "bid_form": BidForm,
        "comment_form": CommentForm,
        "seller": seller,
        "comments": comments
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
    
    filter = {"category": int(category_arg), "is_active": True}
    category_listings = Listing.objects.filter(**filter)
    category_name = Category.objects.get(id=int(category_arg))

    number_of_listings = len(category_listings)

    return render(request, "auctions/index.html", {
        "heading": f"Active Listings: {category_name}",
        "all_listings": category_listings,
        "number_of_listings": number_of_listings
    })


@login_required(login_url="auctions:login")
def watchlist(request):

    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        watchlist_action = request.POST["watchlist_action"]

        if watchlist_action not in ["add", "remove"]:
            return render(request, "auctions/error.html", {
            "message": "Bad request",
            "code": "400"
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

        number_of_listings = len(watchlist_listings)

        return render(request, "auctions/index.html", {
            "heading": "Watchlist",
            "all_listings": watchlist_listings,
            "number_of_listings": number_of_listings
        })
    

@login_required(login_url="auctions:login")
def comment(request):

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Get data
            comment = form.cleaned_data["comment"]
            listing_id = int(request.POST["listing_id"])
            listing = Listing.objects.get(id=listing_id)
            
            # Create new comment entry in database
            new_comment = Comment(
                user = User.objects.get(id=request.user.id),
                listing = listing,
                comment = comment
            )
            new_comment.save()

            return redirect(f"/listing/{listing_id}")
    else:
        return redirect(index)
    

@login_required(login_url="auctions:login")
def close_listing(request):

    if request.method == "POST":
        # Update current listing to inactive in database
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(id=listing_id)
        listing.is_active = False
        listing.save()
        
        return redirect(index)
    else:
        return redirect(index)