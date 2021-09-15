from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("user/<str:username>/watchlist", views.watchlist, name = "watchlist"),
    path("listing", views.listing, name="listing"),
    path("listings/<int:auction_id>", views.listings, name="listings"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlists", views.delete_watchlist, name = "delete_watchlist"),
    path("user/<str:username>", views.user, name = "user"),
    path("comment/<int:auction_id>", views.comment, name = "comment"),
    path("deletecomment", views.deletecomment, name = "deletecomment"),
    path("update_datetime/<int:auction_id>", views.update_datetime, name = "update_datetime"),
    path("autocomplete/category_autocomplete/" , views.category_autocomplete , name='category_autocomplete'),

]
