from django import forms
from django.forms import ModelForm, NumberInput, HiddenInput
from .models import Listing, Bid


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ("title", "description", "starting_bid", "category", "image")

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ("bid",)
        widgets = {
            "bid": NumberInput
        }