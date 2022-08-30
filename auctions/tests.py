#TODO: Create a view test
import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

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
        listing = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
        self.assertEqual(listing.cur_bid(), 0)
    
    def test_cur_bid_one_bid(self):
        """
        Tests what happens when one bid has been made
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
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
        listing = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
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




class WatchListModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='123456')
        self.user.save()


    def test_no_watchlist(self):
        """
        Test to run when no watchlist has been created yet
        """
        login = self.client.login(username='testusers', password='123456')
        listing = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
        try:
            self.user.watchlist
        except ObjectDoesNotExist:
            pass
    

    def test_first_watchlist(self):
        login = self.client.login(username='testusers', password='123456')
        item = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
        watchlist = WatchList(owner=self.user)
        watchlist.save()
        watchlist.listing.add(item)
        self.assertQuerysetEqual(watchlist.listing.all(), [item])
    
    
    def test_create_two_watchlists_for_one_user(self):
        """
        Tests to ensure two or more watchlists cannote be made for the same user
        """
        login = self.client.login(username='testusers', password='123456')
        item = create_listing(title='hey', days=0, pk=5, user=self.user, status=True)
        watchlist = WatchList(owner=self.user)
        watchlist.listing.add(item)
        watchlist.save()
        watchlist2 = WatchList(owner=self.user)
        watchlist2.save()
        self.assertEqual(watchlist, watchlist2)

class IndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='123456')
        self.user.save()

    def test_no_auctions(self):
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no listings available at this time...')
        self.assertQuerysetEqual(response.context['listings'], [])
    
    #Fails because I need to ensure that listings with publishing dates in the future don't show
    def test_future_auction(self):
        login = self.client.login(username='testusers', password='123456')
        item = create_listing(title='hey', days=5, pk=5, user=self.user, status=True)
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['listings'], [])

    
    def test_past_auction(self):
        login = self.client.login(username='testusers', password='123456')
        item = create_listing(title='hey', days=-5, pk=5, user=self.user, status=True)
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['listings'], [item])
    
    def test_closed_auction(self):
        login = self.client.login(username='testusers', password='123456')
        item = create_listing(title='hey', days=0, pk=5, user=self.user, status=False)
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['listings'], [])
    