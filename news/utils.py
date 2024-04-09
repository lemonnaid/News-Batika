import logging
from datetime import datetime

import requests
import xmltodict
from bs4 import BeautifulSoup as BSoup

from .models import Headline


logger = logging.getLogger(__name__)

# scratch code
import re
from collections import Counter
import math


def tokenize(text):
    # Tokenize text into words
    return re.findall(r"\w+", text.lower())


def get_cosine_similarity(vec1, vec2):
    # Calculate cosine similarity between two vectors
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def get_vector(text):
    # Create a vector (dictionary) of word frequencies
    words = tokenize(text)
    return Counter(words)


def get_similar_news(news_id):
    # Get all headlines excluding the user's news
    headlines = Headline.objects.exclude(id=news_id)

    # Get all news descriptions
    descriptions = [headline.description for headline in headlines]

    # Get the user's news description
    user_news = Headline.objects.get(id=news_id)
    user_description = user_news.description

    # Create vectors for user's news description and other news descriptions
    user_vector = get_vector(user_description)
    vectors = [get_vector(desc) for desc in descriptions]

    # Calculate cosine similarity
    similarities = [get_cosine_similarity(user_vector, vector) for vector in vectors]

    # Sort indices based on similarity scores
    sorted_indices = sorted(
        range(len(similarities)),
        key=lambda x: similarities[x],
        reverse=True,
    )

    similar_news_list = [headlines[i] for i in sorted_indices]
    return similar_news_list


# def get_similar_news(news_id):
#     # Get all headlines excluding the user's news
#     headlines = Headline.objects.exclude(id=news_id)

#     # Get all news descriptions
#     descriptions = [headline.description for headline in headlines]

#     # Get the user's news description
#     user_news = Headline.objects.get(id=news_id)
#     user_description = user_news.description

#     # Add the user's news description to the list
#     descriptions.append(user_description)

#     # Vectorize the data
#     vectorizer = CountVectorizer().fit_transform(descriptions)

#     # Calculate cosine similarity
#     cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

#     # Sort indices based on similarity scores
#     sorted_indices = sorted(
#         range(len(cosine_similarities)),
#         key=lambda x: cosine_similarities[x],
#         reverse=True,
#     )

#     similar_news_list = [headlines[i] for i in sorted_indices]
#     return similar_news_list


def scrape_news():
    feed_url_list = [
        "https://english.onlinekhabar.com/feed/",
        "https://enewspolar.com/feed/",
        "https://techspecsnepal.com/feed/",
        "https://www.prasashan.com/category/english/feed/",
        "https://english.ratopati.com/feed",
        "https://en.setopati.com/feed",
        "https://english.nepalpress.com/feed/",
        "https://techmandu.com/feed/",
        "https://english.aarthiknews.com/feed",
    ]

    for feed_url in feed_url_list:
        logger.info(f"Fetching news from: {feed_url}")
        try:
            response = requests.get(feed_url)
            content = response.content
            data_dict = xmltodict.parse(content)

            news_items = data_dict.get("rss", {}).get("channel", {}).get("item")
            for news in news_items:
                title = news["title"].strip("'\"`")

                # Get Description Text
                desc = news["description"]

                if not desc:
                    continue

                soup_desc = BSoup(desc, "html.parser")
                desc = soup_desc.get_text().strip("'\"`")
                news_source = (
                    feed_url.replace("https://", "")
                    .replace(".com/feed/", "")
                    .replace("english.", "")
                    .replace("www.", "")
                    .replace(".com/category/english/feed/", "")
                    .replace("/feed", "")
                    .replace(".com", "")
                    .replace("en.", "")
                )

                url = news["link"]
                pub_date = news["pubDate"]
                pub_date_format = datetime.strptime(
                    pub_date, "%a, %d %b %Y %H:%M:%S %z"
                )

                try:
                    # For onlinekhabar, newspolar, techkajak
                    if feed_url in (
                        "https://english.onlinekhabar.com/feed/",
                        "https://enewspolar.com/feed/",
                        "https://techspecsnepal.com/feed/",
                    ):
                        content = news.get("content:encoded")
                        soup = BSoup(content, "html.parser")
                        img_tag = soup.find("img")
                        img_src = img_tag.get("src")

                    elif feed_url in (
                        "https://techmandu.com/feed/",
                        "https://www.prasashan.com/category/english/feed/",
                    ):
                        news_resp = requests.get(url)
                        img_soup = BSoup(news_resp.content, "html.parser")
                        img_src = img_soup.find("figure").find("img")["src"]

                    # For Seto Pati and Ratopati
                    if feed_url in (
                        "https://english.ratopati.com/feed",
                        "https://en.setopati.com/feed",
                    ):
                        class_name = "featured-images"
                    elif feed_url == "https://english.nepalpress.com/feed/":
                        class_name = "featured-image"
                    elif feed_url == "https://english.aarthiknews.com/feed":
                        class_name = "td-post-featured-image"

                    news_resp = requests.get(url)
                    img_soup = BSoup(news_resp.content, "html.parser")
                    img_src = img_soup.find("div", class_=class_name).find("img")["src"]

                except Exception:
                    img_src = None

                if not img_src:
                    continue

                news_obj = Headline.objects.filter(url=url)
                if not news_obj.exists():
                    head_line_obj = Headline(
                        title=title,
                        description=desc,
                        url=url,
                        image=img_src,
                        pub_date=pub_date_format,
                        news_source=news_source,
                    )
                    head_line_obj.save()
        except Exception as e:
            logger.exception(f"Error fetching data from {feed_url}: {e}")
            continue
    logger.info("Fetching news completed")
