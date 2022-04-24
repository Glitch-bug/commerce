from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new listing", views.new_listing, name ="new listing"),
    path('listing/<int:pk>/', views.listing, name='listing'),
    path('watchlist/<int:pk>/', views.add_watchlist, name='add_watch'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('bid/<int:pk>/', views.bid, name="bid")
]
