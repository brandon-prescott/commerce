from django import forms

from .models import Listing, Bid, Comment


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
            "placeholder": "Enter a starting price",
            "min": 0.01,
            "max": 1000000000,
            "class": "form-control"
            }),
            "category": forms.Select(attrs={
            "class": "form-control"
            })
        }


class BidForm(forms.ModelForm):
    # Creates form for submitting bids
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={
            "placeholder": "Bid",
            "min": 0.01,
            "max": 1000000000,
            "class": "form-control"
            })
        }


class CommentForm(forms.ModelForm):
    # Creates form for submitting comments
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={
            "placeholder": "Add a comment",
            "class": "form-control",
            "rows": 2
            })
        }



    


            
