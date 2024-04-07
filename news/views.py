import requests
import xmltodict
#import nltk
from datetime import datetime
from random import sample

from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import NewsCatrgoryForm
from .cosine_similarity import calculate_similarity_with_models
from django.shortcuts import render

# from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup as BSoup

from news.models import Headline,intrest,CustomUser, newsCategory

from django.contrib import auth

def scrape(request):


    urls = [
        "https://english.onlinekhabar.com/feed/",
        "https://enewspolar.com/feed/",
        "https://techspecsnepal.com/feed/",
        "https://www.prasashan.com/category/english/feed/",
    ]
    

    for u in urls:

        response = requests.get(u)
        content = response.content
        data_dict = xmltodict.parse(content)

        news_items = data_dict.get("rss").get("channel").get("item")
        for news in news_items:
            title = news["title"]

            # Get Description Text
            desc = news["description"]
            soup_desc = BSoup(desc, 'html.parser')
            desc = soup_desc.get_text()

            url = news["link"]
            pub_date = news["pubDate"]
            pub_date_format = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            categories = news['category']

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
                head_line_obj = Headline(title=title, description=desc, url=url, image=img_src, pub_date=pub_date_format)
                head_line_obj.save()
                
                for category in categories:
                    category, created = newsCategory.objects.get_or_create(category_name=category)
                    head_line_obj.news_category.add(category)

                head_line_obj.save()

            else:
                pass 
    
    return redirect("home")


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
    random_three = Headline.objects.order_by('?')[:3]
    random_twelve = Headline.objects.order_by('?')[:12]

    first_news = Headline.objects.first()
    clean_text = "No Data. Please run Fetch News"
    if first_news:
        clean_text = first_news.description

    context = {
        'head': first_news,
        'random_three': random_three,
        'random_twelve': random_twelve,
        'clean_text': clean_text,
        'date': datetime.now()
    }
    return render(request, 'news/index.html', context)


def userp(request):
    random_three = Headline.objects.order_by('?')[:3]
    random_twelve = Headline.objects.order_by('?')[:12]

    first_news = Headline.objects.first()
    clean_text = "Nothing"
    if first_news:
        clean_text = first_news.description
    
    context = {
        'head': first_news,
        'random_three': random_three,
        'random_twelve': random_twelve,
        'clean_text': clean_text
    }
    return render(request, 'news/logined.html', context)


def base(request):
    return render(request,'news/base.html')



def save_preference(request):
    form = NewsCatrgoryForm()
    return render(request, 'news/logined.html', {'form': form})
    # if request.method == 'POST':
    #     form = NewsCatrgoryForm(request.POST)
    #     if form.is_valid():
    #         preference = form.cleaned_data.get('PreferencedNews')
    #         preference = intrest(PreferencedNews=preference)
    #         preference.save()
    #         return redirect('userprofile')  # Redirect to the homepage or any other page
    # else:
    #     form = NewsCatrgoryForm()
    # return render( request, 'news/logined.html', {'form':form})
        

# register,login and logout using bultin django authication
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'news/register.html', {'error': 'Username is already taken', 'date': datetime.now()})
        else:
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            auth.login(request, user)
            return redirect('/')
    else:
        return render(request, 'news/register.html', {'date': datetime.now()})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('userprofile')
        else:
            return render(request, 'news/login.html', {'error': 'Invalid credentials', 'date': datetime.now()})
    else:
        return render(request, 'news/login.html', {'date': datetime.now()})

def logout(request):
    auth.logout(request)
    return redirect('/')