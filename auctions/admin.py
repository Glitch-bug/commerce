from django.contrib import admin

from .models import Bid, Listing, WatchList, User
# Register your models here.
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(WatchList)
admin.site.register(User)