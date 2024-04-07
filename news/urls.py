from django.urls import path
from . import views

urlpatterns = [
    path("scrape/", views.scrape, name="scrape"),
    path("", views.index, name="home"),
    path("register/", views.user_register, name="user_register"),
    path("login/", views.login, name="login"),
    path("userprofile/", views.userp, name="userprofile"),
    path(
        "similar_news/<int:news_id>/", views.get_similar_news, name="get_similar_news"
    ),
    # May need to add param
]
