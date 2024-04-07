from datetime import datetime

import requests
import xmltodict
from bs4 import BeautifulSoup as BSoup
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from .models import Headline


def get_similar_news(news_id):
    # Input and output data
    articles = Headline.objects.all()
    article_titles = [article.description for article in articles]
    article_link = [article.url for article in articles]

    article_read = Headline.objects.get(id=news_id).description
    article_url = Headline.objects.get(id=news_id).url

    custom_stop_words = {"OnlineKhabar", "English", "News", "Enewspolar"}
    all_stop_words = custom_stop_words.union(sklearn_stop_words)
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95, min_df=2, stop_words=list(all_stop_words)
    )
    tfidf_features = tfidf_vectorizer.fit_transform(article_titles)

    nmf = NMF(n_components=6)
    nmf_features = nmf.fit_transform(tfidf_features)
    normalized_features = normalize(nmf_features)

    current_article_index = article_titles.index(article_read)
    current_article = normalized_features[current_article_index, :]

    # Calculate cosine similarities
    similarities = cosine_similarity(
        normalized_features, current_article.reshape(1, -1)
    )

    # Get indices of similar articles (excluding the clicked article itself)
    similar_article_indices = similarities.flatten().argsort()

    recommended_article = article_titles[similar_article_indices[0]]
    recommended_url = article_link[similar_article_indices[0]]

    return f"""<h1>Article Read:</h1><h2>{article_read}<a href='{article_url}' target="_blank">{article_url}</a></h2><br><br><h1>Article Recommend: </h1><h2>{recommended_article}<a href='{recommended_url}' target="_blank">{recommended_url}</a></h2><br><br>
    <h2>Similarities</h2><p>{similarities}</p>
    <h2>Similarity index</h2><p>{similar_article_indices}</p>"""
    return f"Given Article: {article_titles[clicked_article_index]}<br><br>Recommended Article: {recommended_article}"


def scrape_news():
    feed_url_list = [
        "https://english.onlinekhabar.com/feed/",
        "https://enewspolar.com/feed/",
        "https://techspecsnepal.com/feed/",
    ]

    for feed_url in feed_url_list:
        response = requests.get(feed_url)
        content = response.content
        data_dict = xmltodict.parse(content)

        news_items = data_dict.get("rss").get("channel").get("item")
        for news in news_items:
            title = news["title"].strip("'\"`")

            # Get Description Text
            desc = news["description"].strip("'\"`")
            soup_desc = BSoup(desc, "html.parser")
            desc = soup_desc.get_text()
            news_source = (
                feed_url.replace("https://", "")
                .replace(".com/feed/", "")
                .replace("english.", "")
            )

            url = news["link"]
            pub_date = news["pubDate"]
            pub_date_format = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")

            try:
                content = news["content:encoded"]
                # Extracting the image path
                soup = BSoup(content, "html.parser")
                img_tag = soup.find("img")
                img_src = img_tag.get("src")

            except:
                img_src = None

            news_obj = Headline.objects.filter(title=title)
            if news_obj.exists() == False:
                head_line_obj = Headline(
                    title=title,
                    description=desc,
                    url=url,
                    image=img_src,
                    pub_date=pub_date_format,
                    news_source=news_source,
                )
                head_line_obj.save()
