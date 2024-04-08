from datetime import datetime

from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from news import utils
from news.models import CustomUser
from news.models import Headline
# import nltk
# from nltk.tokenize import word_tokenize


def scrape(request):
    utils.scrape_news()
    return redirect("home")


def index(request):
    random_three = Headline.objects.order_by("-pub_date")[1:4]
    latest_all_news = Headline.objects.order_by("-pub_date")[4:]
    latest_news = Headline.objects.order_by("-pub_date").first()

    clean_text = "No Data. Please Click Fetch News Above"
    if latest_news:
        clean_text = latest_news.description

    context = {
        "head": latest_news,
        "random_three": random_three,
        "latest_all_news": latest_all_news,
        "clean_text": clean_text,
        "date": datetime.now(),
        "authenticated": request.user.is_authenticated,
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
    user_input = "i love apple"
    similar_news = utils.get_similar_news(user_input)
    return HttpResponse(f"<h1>{similar_news}</h1>")
    similar_news = ["news_1", "news_2"]
    return JsonResponse(similar_news, safe=False)
