from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    time_created = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    image2 = models.FilePathField(default='/images/avatar.png', verbose_name='image')
    
def five_days_later():
    return timezone.now() + timezone.timedelta(days=5)
    
class AuctionListings(models.Model):
    auction_id = models.AutoField(primary_key=True )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    auction = models.CharField(max_length=300)
    price = models.DecimalField(max_digits= 100, decimal_places=2 , default = 0.0)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='static/images/', verbose_name='image', default='images/no_image.jpg')
    image2 = models.FilePathField(default='images/no_image.jpg', verbose_name='image')
    expire_time = models.DateTimeField(default=five_days_later)
    categories = None

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, idx, value):
        self.categories = value
        return

class Category(models.Model):
    auction_id = models.ForeignKey(
        AuctionListings,
        on_delete=models.CASCADE
    )
    category = models.CharField(max_length=50, default = None)
class Bids(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    ) 
    auction_id = models.ForeignKey(
        AuctionListings,
        on_delete=models.CASCADE
    ) 
    bid = models.DecimalField(max_digits= 100, decimal_places=2, default = 0.0)

class Comments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null= True
    ) 
    auction_id = models.ForeignKey(
        AuctionListings,
        on_delete=models.CASCADE
    ) 
    comment = models.CharField(max_length=300)
    timestamp = models.DateTimeField(default=timezone.now)


class WatchList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    ) 
    auction_id = models.ForeignKey(
        AuctionListings,
        on_delete=models.CASCADE
    ) 
    
from django import forms


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),label='Listing Auction Title',max_length = 100 )
    price = forms.DecimalField(label = "Starting Price of the current Item")
    category = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),label='Categories seperaties with ,', required = False)