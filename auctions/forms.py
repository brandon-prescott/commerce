from django import forms

from .models import User, Category, Listing, Bid


class CreateListingForm(forms.ModelForm):
    # Creates form for Listing model
    class Meta:
        model = Listing # Creates the link to the Listing SQL table
        fields = ["title", "description", "image_url", "price", "category", "user"] # Fields is essentially saying which attributes to pull in from the model/SQL table
        # Labels define what goes in the label tag on the form
        labels = {
            "title": "Title",
            "description": "Description",
            "image_url": "Image URL",
            "price": "Price",
            "category": "Category",
            "user": "User"
        }
        # Widgets is for formatting the form
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
            }),
            "user": forms.NumberInput(attrs={
            "placeholder": 0
            })
        }


class BidForm(forms.ModelForm):
    # Creates form for submitting bids
    class Meta:
        model = Bid
        fields = ["user", "listing", "amount"]
        widgets = {
            "user": forms.NumberInput(attrs={
            "placeholder": 0
            }),
            "listing": forms.NumberInput(attrs={
            "placeholder": 0
            }),
            "amount": forms.NumberInput(attrs={
            "placeholder": "Bid",
            "min": 0.01,
            "max": 1000000000,
            "class": "form-control"
            })
        }
