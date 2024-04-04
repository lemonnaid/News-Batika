import requests
import xmltodict
#import nltk
from datetime import datetime
from random import sample

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm
from .cosine_similarity import calculate_similarity_with_models

# from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup as BSoup

from news.models import Headline


def scrape(request):


    urls = [
        "https://english.onlinekhabar.com/feed/",
        "https://enewspolar.com/feed/",
    ]
    

    for u in urls:

        response = requests.get(u)
        content = response.content
        data_dict = xmltodict.parse(content)

        for data in data_dict:
            news_items = data_dict.get("rss").get("channel").get("item")
            for news in news_items:
                title = news["title"]
                desc = news["description"]
                url = news["link"]
                pub_date = news["pubDate"]
                # print("---------daet---------",pub_date)
                pub_date_format = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")

                try:
                    content = news["content:encoded"]
                    #Extracting the image path
                    soup = BSoup(content, 'html.parser')
                    img_tag = soup.find('img')
                    img_src = img_tag.get('src')
                except:
                    img_src = None

                news_obj = Headline.objects.filter(title=title)
                if news_obj.exists()==False:
                    if img_src is not None:
                        Headline.objects.create(title=title, description=desc, url=url, image=img_src, pub_date=pub_date_format)
                    else:
                        Headline.objects.create(title=title, description=desc, url=url, pub_date=pub_date_format)
                else:
                    pass

                
    
                # return JsonResponse(news)

    return redirect("break")


def news_list(request):
    headlines = Headline.objects.all().order_by('-id')
    query = request.GET.get("intreast")
    if query:
        headlines = calculate_similarity_with_models(query)
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)


def index(request):
    news = Headline.objects.all()
    random_three = sample(list(news), 3)
    random_twelve = sample(list(news), 12)
    head=Headline.objects.first()
    print(head)
    try:
        soup = BSoup(head.description, 'html.parser')
        clean_text = soup.get_text()
    except:
        clean_text = "Nothing"
    context={'head':head, 'random_three':random_three, 'random_twelve':random_twelve, 'clean_text': clean_text}
    return render(request,'news/index.html',context)

def base(request):
    return render(request,'news/base.html')



def login(request):
      return render(request,'news/login.html')


def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = RegisterForm()
    # context = {"form": form}
    return render(request, 'news/register.html')
