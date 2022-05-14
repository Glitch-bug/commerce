import datetime

from django.test import TestCase, Client
from django.utils import timezone

from .models import Listing, User

def create_listing(title, days, pk, user):
    user = user
    time = timezone.now() + datetime.timedelta(days=days)
    return Listing.objects.create(title=title, date_added=time, owner=user, pk=pk)


class ListingModelTests(TestCase):
    # Continue work here
    def test_cur_bid_no_bids(self):
        """
        Tests what happens when no bids have been made
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        listing = create_listing('hey', 0, 5, self.user)
        self.assertEqual(listing.cur_bid(), 0)
    
    def test_cur_bid_one_bid(self):
        """
        Tests what happens when one bid has been made
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        listing = create_listing('hey', 0, 5, self.user)
        amount = 1
        bid = listing.bid_set.create(owner=listing.owner, amount=amount, date_added = timezone.now())
        listing = Listing.objects.get(pk=listing.id)  # needed to recall listing object after bid made for recent results
        self.assertEqual(listing.cur_bid(), bid)
        print(bid)


# class BidModelTests(TestCase):
    # def test_