from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_sentences(user_input, data_list):
    # Add user input to data list
    data_list.append(user_input)

    # Vectorize the data
    vectorizer = CountVectorizer().fit_transform(data_list)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

    # Sort sentences based on similarity scores
    sorted_sentences = sorted(
        zip(data_list[:-1], cosine_similarities), key=lambda x: x[1], reverse=True
    )

    # Return sorted sentences
    return sorted_sentences


# Sample data
user_input = "i love apple"
data_list = [
    "apple is fruit.",
    "apple are apple",
    "i love eating",
    "i love apple",
    "apple is love",
    "messi scored goal",
    "war is to be stopped",
    "apple day keep doctor away",
]

# Get similar sentences
similar_sentences = get_similar_sentences(user_input, data_list)

# Print the result
for sentence, similarity in similar_sentences:
    print(f"Similarity: {similarity:.2f}, Sentence: {sentence}")
