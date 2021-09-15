from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == "GET" :
        auctions = list(AuctionListings.objects.all())
        for cnt, auction in enumerate(auctions):
            categories = list(Category.objects.filter(auction_id=auction))
            auctions[cnt].categories = categories

        if request.user.is_authenticated:
            watchlists = WatchList.objects.filter(user=request.user)
            watchlist = [i.auction_id for i in watchlists]
            if len(auctions) > 0:
                auctions.sort(reverse = True , key = lambda x : x.timestamp)
            return render(request, "auctions/index.html", {
                "listing" : auctions,
                "watchlist" : watchlist,
                "watchlist_exists" : True,
                "datetime": timezone.now,
                })
        else :
            return render(request, "auctions/index.html", {
                "listing" : auctions,
                "watchlist_exists" : False,
                "datetime": timezone.now,
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

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        return login_view(request)
        #login(request, user)
        #return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def listing(request):
    form = NewPageForm(request.POST)
    if request.method == "POST":
        try:
            auction_listing = AuctionListings.objects.create(user = request.user,price = request.POST["price"], auction = request.POST["title"], image2 = request.POST["image"], expire_time = request.POST["expiration-date"])
            auction_listing.save()
            categories = request.POST["category"]
            for category in categories.split(","):
                categ = Category.objects.create(auction_id=auction_listing, category = category)
                categ.save()
            return HttpResponseRedirect(reverse("listings", args=[auction_listing.auction_id]))
        except IntegrityError:
            return render(request, "auctions/form.html", {
                "message": "Auction listing name already taken. Try another name",
                "form" : form
            })
    elif request.method == "GET":
        return render(request, "auctions/form.html" , {
            "form": form
         })


@login_required
def listings(request, auction_id):
    message = None
    auction_id = AuctionListings.objects.get(auction_id=auction_id)
    bids = Bids.objects.filter(auction_id=auction_id)
    if request.POST.get("bid",False)  :
        if len(bids) > 0 :
            max_bid = max(bids , key = lambda x : x.bid).bid
        else :
            max_bid = 0
        try :
            if ( float(request.POST["bid"]) > float(max_bid)):
                bid = Bids.objects.create(user = request.user , bid = request.POST["bid"], auction_id = auction_id)
                bid.save()
            else :
                message = "You are outbidded"
        except :
                message = "The bid should be a decimal number.."

    bids = Bids.objects.filter(auction_id=auction_id)
    if len(bids) > 0 :
        highest_bidder = max(bids , key = lambda x : x.bid)
        bids_len = len(bids)
    else :
        highest_bidder = None
        bids_len = 0
    
    comments = list(Comments.objects.filter(auction_id=auction_id))
    categories = list(Category.objects.filter(auction_id=auction_id))
    try :
        user_watchlist = list(WatchList.objects.filter(user=request.user , auction_id=auction_id))
    except:
        user_watchlist = None
    return render(request, "auctions/auction.html", {
        "listings" : auction_id,
        "bids" : bids_len,
        "highest_bidder" : highest_bidder,
        "message" : message,
        "datetime": timezone.now,
        "comments": comments,
        "categories": categories,
        "image": auction_id.image2,
        "watchlist": user_watchlist is not None and user_watchlist != []
        }
    )

@login_required    
def categories(request):
    auctions = Category.objects.all()
    categories = list({auction.category for auction in auctions if auction.category})
    categories.sort()
    return render(request, "auctions/categories.html", {
        "categories" : categories
        }
    )

def category_autocomplete(request):
    auctions = Category.objects.all()
    categories = list({auction.category for auction in auctions if auction.category})
    return HttpResponse(json.dumps(categories))
    
@login_required
def category(request, category):
    auction = list(Category.objects.filter(category = category))
    auction.sort(reverse = True , key = lambda x : x.auction_id.timestamp)
    auction = [ x.auction_id for x in auction]
    return render(request, "auctions/category.html", {
        "listing" : auction,
        "category" : category
        }
    )
        
@login_required
def watchlist(request,username):
    user = request.user
    if user.username == username:
        if request.method == "POST" :
            auction = AuctionListings.objects.get(auction_id = request.POST["auction_id"])
            watchlist = WatchList.objects.create(user = user, auction_id = auction)
            watchlist.save()
            redirect_to = request.POST["redirect_to"]
            if redirect_to == 'index':
                return HttpResponseRedirect(reverse("index"))
            return HttpResponseRedirect(reverse(redirect_to, args=[request.POST["auction_id"]]))
        else :
            watchlists = WatchList.objects.filter(user = user)
            watchlist = list( i.auction_id for i in watchlists )
            return render(request, "auctions/watchlist.html", {
                "watchlist" : watchlist[::-1]
                }
            )
    else :
        return HttpResponseRedirect(reverse("index"))
        
@login_required
def delete_watchlist(request):
    user = request.user
    if request.POST["redirect"] == "True" :
        auction_in_watchlist = WatchList.objects.get(user = user, auction_id = request.POST["auction_id"])
        auction_in_watchlist.delete()
        watchlist = WatchList.objects.filter(user = user)
        watchlist = list( i.auction_id for i in watchlist )
        return render(request, "auctions/watchlist.html", {
            "watchlist" : watchlist
            }
        )
    else :
        auction_in_watchlist = WatchList.objects.get(user = user, auction_id = request.POST["auction_id"])
        auction_in_watchlist.delete()
        redirect_to = request.POST["redirect_to"]
        if redirect_to == 'index':
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse(redirect_to,args=[request.POST["auction_id"]]))
@login_required    
def user(request, username):
    user1 = User.objects.get(username = username)
    auctions_by_user = list(AuctionListings.objects.filter(user = user1))
    auctions_by_user.sort(reverse = True , key = lambda x : x.timestamp)
    for cnt, auction in enumerate(auctions_by_user[:5]):
        categories = list(Category.objects.filter(auction_id=auction))
        auctions_by_user[cnt].categories = categories
    bids_by_user = list(Bids.objects.filter(user=user1))
    bids_by_user = list({i.auction_id for i in bids_by_user})
    bids_by_user.reverse()

    comments = list(Comments.objects.filter(user = user1))
    comments.reverse()

    return render(request, "auctions/user.html", {
            "auctions_by_user" : auctions_by_user[:5],
            "user1" : user1,
            "bids" : bids_by_user[:5],
            "comments" : comments[:5]
            }
        )
        
@login_required    
def comment(request, auction_id):
    
    user = request.user
    
    comment = Comments.objects.create(user = user , auction_id = AuctionListings.objects.get(auction_id=auction_id) , comment = request.POST["comment"])
    comment.save()
    return HttpResponseRedirect(reverse("listings", args=[auction_id]))

def deletecomment(request):
    comment = Comments.objects.get(id = request.POST["comment"])
    auction_id = comment.auction_id
    comment.delete()
    return HttpResponseRedirect(reverse("listings", args=[auction_id.auction_id]))
    
def update_datetime(request, auction_id) :
    
    auction = AuctionListings.objects.get(auction_id = auction_id)
    auction.expire_time = timezone.now()
    auction.save()
    
    return HttpResponseRedirect(reverse("listings", args=[auction_id]))
