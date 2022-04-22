from django.contrib import admin
from .models import User, Listing, Watched, Bid, Comment, Auction


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "category", "image")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "title", "user")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Auction)
admin.site.register(Watched)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)