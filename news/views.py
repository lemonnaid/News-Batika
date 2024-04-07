import requests
import xmltodict
from django.contrib.auth import logout

# import nltk
from datetime import datetime
from random import sample

from django.shortcuts import render
from django.shortcuts import render, redirect

from .cosine_similarity import calculate_similarity_with_models
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from news import utils

# from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup as BSoup

from news.models import Headline, CustomUser

from django.contrib import auth


def scrape(request):
    utils.scrape_news()
    return redirect("home")


def index(request):    
    random_three = Headline.objects.order_by("?")[:3]
    latest_all_news = Headline.objects.order_by("-id")
    latest_news = Headline.objects.order_by("-id").first()

    clean_text = "No Data. Please Click Fetch News Above"
    if latest_news:
        clean_text = latest_news.description

    context = {
        "head": latest_news,
        "random_three": random_three,
        "latest_all_news": latest_all_news,
        "clean_text": clean_text,
        "date": datetime.now(),
        "authenticated": request.user.is_authenticated
    }

    return render(request, "news/index.html", context)


# register,login and logout using bultin django authication
def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if CustomUser.objects.filter(username=username).exists():
            return render(
                request,
                "news/register.html",
                {"error": "Username is already taken", "date": datetime.now()},
            )
        else:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            auth.login(request, user)
            return redirect("home")
    else:
        return render(request, "news/register.html", {"date": datetime.now()})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "news/login.html",
                {"error": "Invalid credentials", "date": datetime.now()},
            )
    else:
        return render(request, "news/login.html", {"date": datetime.now()})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect("home")


def get_similar_news(request, news_id):
    similar_news = utils.get_similar_news(news_id)
    return HttpResponse(f"<h1>{similar_news}</h1>")
    similar_news = ["news_1", "news_2"]
    return JsonResponse(similar_news, safe=False)
