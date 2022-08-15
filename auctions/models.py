#TODO: Finish work on making page for individual categories
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()
    Categories = models.TextChoices('categories', 'Toys Accessorys Appliances Organisms')
    category = models.CharField(max_length=255, choices=Categories.choices)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the model"""
        return f"{self.title[:50]}"

    def cur_bid(self):
        """ Returns a bid object for the highest bid"""
        listings = self.bid_set.all()
        amounts = []
        if listings:
            for i in range(len(listings)):
                amounts.append(listings[i].amount)
            bid = self.bid_set.get(amount=max(amounts))
            return bid
        else:
            return 0
    
    def owner_titled(self):
        return self.owner.username.title()
    #TODO: Create a recent bids on listing method later
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    #TODO: Create a recent bids made result

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    replies_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    # Owner foreign key should be a one to one so each owner has a single list
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Watchlist listing should be a many to many relationship so single watchlist can hold many listings and a single listing can be on many watchlists
    listing = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.owner.username.title()}'s Watchlist"

    def owner_titled(self):
        return self.owner.username.title()
