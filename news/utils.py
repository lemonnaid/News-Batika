import logging
from datetime import datetime

import requests
import xmltodict
from background_task import background
from bs4 import BeautifulSoup as BSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Headline


logger = logging.getLogger(__name__)


def get_similar_news(news_id):
    data_list = [
        "apple is fruit.",
        "apple are apple",
        "i love eating",
        "apple is love",
        "messi scored goal",
        "war is to be stopped",
        "apple day keep doctor away",
    ]

    # Add user input to data list
    data_list.append(news_id)

    # Vectorize the data
    vectorizer = CountVectorizer().fit_transform(data_list)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

    # Sort sentences based on similarity scores
    sorted_sentences = sorted(
        zip(data_list[:-1], cosine_similarities), key=lambda x: x[1], reverse=True
    )

    result_similarity = [
        f"{sentence}: {similarity}" for sentence, similarity in sorted_sentences
    ]
    return f"User Input: {news_id}<br><br>Similar News:<br>" + "<br>".join(
        result_similarity
    )

    # Input and output data
    # articles = Headline.objects.all()
    # article_titles = [article.description for article in articles]
    # article_link = [article.url for article in articles]

    # article_read = Headline.objects.get(id=news_id).description
    # article_url = Headline.objects.get(id=news_id).url

    # custom_stop_words = {"OnlineKhabar", "English", "News", "Enewspolar"}
    # all_stop_words = custom_stop_words.union(sklearn_stop_words)
    # tfidf_vectorizer = TfidfVectorizer(
    #     max_df=0.95, min_df=2, stop_words=list(all_stop_words)
    # )
    # tfidf_features = tfidf_vectorizer.fit_transform(article_titles)

    # nmf = NMF(n_components=6)
    # nmf_features = nmf.fit_transform(tfidf_features)
    # normalized_features = normalize(nmf_features)

    # current_article_index = article_titles.index(article_read)
    # current_article = normalized_features[current_article_index, :]

    # # Calculate cosine similarities
    # similarities = cosine_similarity(normalized_features[-1], normalized_features[:-1]).flatten()

    # # Get indices of similar articles (excluding the clicked article itself)
    # similar_article_indices = similarities.flatten().argsort()

    # recommended_article = article_titles[similar_article_indices[0]]
    # recommended_url = article_link[similar_article_indices[0]]

    # return f"""<h1>Article Read:</h1><h2>{article_read}<a href='{article_url}' target="_blank">{article_url}</a></h2><br><br><h1>Article Recommend: </h1><h2>{recommended_article}<a href='{recommended_url}' target="_blank">{recommended_url}</a></h2><br><br>
    # <h2>Similarities</h2><p>{similarities}</p>
    # <h2>Similarity index</h2><p>{similar_article_indices}</p>"""
    # return f"Given Article: {article_titles[clicked_article_index]}<br><br>Recommended Article: {recommended_article}"


@background(schedule=5)
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
        except Exception:
            logger.error(f"Error fetching data from {feed_url}")
            logger.error(Exception)
            continue
    logger.info("Fetching news completed")
