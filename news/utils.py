from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Headline


from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from .models import Headline
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words


def get_similar_news(news_id):
    # Input and output data
    articles = Headline.objects.all()
    article_titles = [article.description for article in articles]
    article_read = Headline.objects.get(id=news_id).description

    custom_stop_words = {"OnlineKhabar English News"}
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
    return f"""<h1>Article Read:</h1><h2>{article_read}</h2><br><br><h1>Article Recommend: </h1><h2>{recommended_article}</h2><br><br>
    <h2>Similarities</h2><p>{similarities}</p>
    <h2>Similarity index</h2><p>{similar_article_indices}</p>"""
    return f"Given Article: {article_titles[clicked_article_index]}<br><br>Recommended Article: {recommended_article}"
