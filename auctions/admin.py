from django.contrib import admin

from .models import Bid, Listing
# Register your models here.
admin.site.register(Bid)
admin.site.register(Listing)