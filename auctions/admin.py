from django.contrib import admin
from .models import User, Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "category", "image")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)