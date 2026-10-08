import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_similar_email(customer_email):

    df = pd.read_csv("data/emails.csv")

    emails = df["Customer_Email"].fillna("").tolist()

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(emails + [customer_email])

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    best_index = similarities.argmax()

    best_email = df.iloc[best_index]

    return {
        "previous_email": best_email["Customer_Email"],
        "previous_reply": best_email["Previous_Reply"],
        "similarity": similarities[best_index]
    }