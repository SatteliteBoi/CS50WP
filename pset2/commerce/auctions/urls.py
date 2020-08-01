from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<str:inputlistid>", views.getlisting, name="listing"),
    path("bidupdate", views.bidupdate, name="bidupdate"),
    path("bidclose", views.bidclose, name="bidclose"),
    path("createcomment", views.createcomment, name="createcomment"),
    path("watch", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist")
]
