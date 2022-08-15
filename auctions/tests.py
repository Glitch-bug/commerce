#TODO: Create a view test
import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Listing, User, WatchList

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
        listing.save()
        bid.save()
        self.assertEqual(listing.cur_bid(), bid)
    
    def test_cur_bid_mult_bids(self):
        """
        Tests that highest bid is current bid when many bids have been made
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing('hey', 0, 5, self.user, status=True)
        bids = []
        for i in range(5):
            bid = listing.bid_set.create(owner=listing.owner, amount=i, date_added = timezone.now())
            bids.append(bid)
            bid.save()
        listing.save()
        self.assertEqual(listing.cur_bid(), bids[4])

# class BidModelTests(TestCase):
#      def setUp(self):
#         self.user = User.objects.create_user(username='testusers', password='123456')

#     def test_no_bid




class WatchListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='123456')
        self.user.save()


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
    

    def test_first_watchlist(self):
        login = self.client.login(username='testusers', password='123456')
        item = create_listing('hey', 0, 5, self.user, status=True)
        watchlist = WatchList(owner=self.user)
        watchlist.save()
        watchlist.listing.add(item)
        self.assertEqual(list(watchlist.listing.all()), [item])
    
    
    def test_create_two_watchlists_for_one_user(self):
        """
        Tests to ensure two or more watchlists cannote be made for the same user
        """
        login = self.client.login(username='testusers', password='123456')
        item = create_listing('hey', 0, 5, self.user, status=True)
        watchlist = WatchList(owner=self.user)
        watchlist.listing.add(item)
        watchlist.save()
        watchlist2 = WatchList(owner=self.user)
        watchlist2.save()
        self.assertEqual(watchlist, watchlist2)