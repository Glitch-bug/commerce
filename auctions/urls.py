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
    path('bid/<int:pk>/', views.bid, name="bid"),
    path('remove_item/<int:pk>/', views.rem_watchlist, name='rem_watch'),
    path('close_listing/<int:pk>/', views.close_listing, name="close"),
    path('categories', views.categories, name="categories"),
    path('category/<str:category>', views.category, name="category"),
    path('edit_listing/<int:pk>', views.edit_listing, name="edit_listing")
]
