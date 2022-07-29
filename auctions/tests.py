import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Listing, User

def create_listing(title, days, pk, user, status):
    user = user
    time = timezone.now() + datetime.timedelta(days=days)
    return Listing.objects.create(title=title, date_added=time, owner=user, pk=pk, status=status)


class ListingModelTests(TestCase):
    # Continue work here
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='123456')
        
    def test_cur_bid_no_bids(self):
        """
        Tests what happens when no bids have been made
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing('hey', 0, 5, self.user, status=True)
        self.assertEqual(listing.cur_bid(), 0)
    
    def test_cur_bid_one_bid(self):
        """
        Tests what happens when one bid has been made
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing('hey', 0, 5, self.user, status=True)
        amount = 1
        bid = listing.bid_set.create(owner=listing.owner, amount=amount, date_added = timezone.now())
        listing = Listing.objects.get(pk=listing.id)  # needed to recall listing object after bid made for recent results
        self.assertEqual(listing.cur_bid(), bid)
        


# class BidModelTests(TestCase):
    # def test_

class WatchListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='123456')

    def test_no_watchlist(self):
        """
        Test to run when no watchlist has been created yet
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing('hey', 0, 5, self.user, status=True)
        try:
            self.user.watchlist
        except ObjectDoesNotExist:
            pass
    
    # def test_first_watchlist(self):
    #     login = self.client.login(username='testusers', password='123456')
    #     listing = create_listing('hey', 0, 5, self.user, status=True)

    #     watchlist = WatchList(owner=self.user)
    #     watchlist.listing.add(listing)
    #     self.assertEqual(list(self.user.li.all()), [listing]
        