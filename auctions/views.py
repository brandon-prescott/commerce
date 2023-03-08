from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Category, Listing


class CreateListingForm(forms.ModelForm):
    # Creates form for Listing model
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "price", "category"]
        labels = {
            "title": "Title",
            "description": "Description",
            "image_url": "Image URL",
            "price": "Price",
            "category": "Category"
        }
        widgets = {
            "title": forms.TextInput(attrs={
            "placeholder": "Enter a title for this item",
            "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
            "placeholder": "Describe this item in more detail",
            "class": "form-control"
            }),
            "image_url": forms.URLInput(attrs={
            "placeholder": "A URL can be used to display an image",
            "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
            "placeholder": "Enter a starting bid",
            "min": 0.01,
            "max": 1000000000,
            "class": "form-control"
            }),
            "category": forms.Select(attrs={
            "class": "form-control"
            })
        }

def index(request):
    return render(request, "auctions/index.html")


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
        return render(request, "auctions/index.html")

    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm
        })
