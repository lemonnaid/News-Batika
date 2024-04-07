from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Headline

def get_similar_news(news_id):
    articles = Headline.objects.all()
    article_titles = [article.title for article in articles]

    clicked_article = Headline.objects.get(id=news_id).title

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(article_titles)

    clicked_article_tfidf = tfidf_matrix.transform([clicked_article])
    cosine_similarities = cosine_similarity(clicked_article_tfidf, tfidf_matrix).flatten()
    return f'{cosine_similarities}'
    # Get indices of similar articles (excluding the clicked article itself)
    # https://kavita-ganesan.com/tfidftransformer-tfidfvectorizer-usage-differences/
    similar_article_indices = cosine_similarities.argsort()[:-2:-1]
    
    recommended_article = article_titles[similar_article_indices[0]]
    return f'Given Article: {article_titles[clicked_article_index]}<br><br>Recommended Article: {recommended_article}'
