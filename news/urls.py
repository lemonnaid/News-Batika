from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("scrape/", views.scrape, name="scrape"),
    path(
        "similar_news/<int:news_id>/", views.get_similar_news, name="get_similar_news"
    ),
    path("search/<str:search_text>", views.search_news, name="search_news"),
]
