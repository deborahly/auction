from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories,name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("bids", views.bids, name="bids"),
    path("error", views.error, name="error")
]

