import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import ollama

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import threading

# LOAD DATASETS

products_df = pd.read_csv("products.csv")
faq_df = pd.read_csv("faq.csv")
reviews_df = pd.read_csv("reviews.csv")

# LOAD EMBEDDING MODEL

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# FAQ EMBEDDINGS

faq_embeddings = embedding_model.encode(
    faq_df["question"].tolist()
)

# PRODUCT TF-IDF

products_df["text"] = (
    products_df["product_name"].astype(str)
    + " "
    + products_df["category"].astype(str)
    + " "
    + products_df["description"].astype(str)
)

tfidf = TfidfVectorizer()

product_vectors = tfidf.fit_transform(
    products_df["text"]
)

# SENTIMENT MODEL

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# FAQ FUNCTION

def find_best_faq(query):

    query_embedding = embedding_model.encode([query])

    similarity = cosine_similarity(
        query_embedding,
        faq_embeddings
    )[0]

    best_index = similarity.argmax()
    best_score = similarity[best_index]

    return best_index, best_score


# PRODUCT SEARCH

def find_similar_products(query, top_k=3):

    query_vector = tfidf.transform([query])

    similarity = cosine_similarity(
        query_vector,
        product_vectors
    )[0]

    indexes = similarity.argsort()[::-1]

    results = []

    for index in indexes:

        if similarity[index] > 0:

            results.append(
                (index, similarity[index])
            )

        if len(results) == top_k:
            break

    return results


# FIND PRODUCT BY NAME

def find_product(query):

    query_lower = query.lower()

    for name in products_df["product_name"]:

        if name.lower() in query_lower:
            return name

    return None


# PRODUCT QUESTION - QWEN

def product_question(query):

    product_name = find_product(query)

    # If exact product name is found,
    # use that product information first.
    if product_name:

        product_data = products_df[
            products_df["product_name"] == product_name
        ]

        product_details = ""

        for _, row in product_data.iterrows():

            product_details += (
                f"Product: {row['product_name']}\n"
                f"Category: {row['category']}\n"
                f"Price: ₹{row['price']}\n"
                f"Description: {row['description']}\n\n"
            )

    else:

        results = find_similar_products(query, 3)

        if not results:
            return "Sorry, I could not find a matching product."

        product_details = ""

        for index, score in results:

            row = products_df.iloc[index]

            product_details += (
                f"Product: {row['product_name']}\n"
                f"Category: {row['category']}\n"
                f"Price: ₹{row['price']}\n"
                f"Description: {row['description']}\n\n"
            )

    prompt = f"""
You are an e-commerce assistant.

Answer the user's question using ONLY the product
information given below.

PRODUCT INFORMATION:
{product_details}

USER QUESTION:
{query}

Give a short, clear and accurate answer.

Do not invent any information that is not present
in the product information.
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful e-commerce assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# PRODUCT RECOMMENDATION

def recommend_products(query):

    results = find_similar_products(query, 3)

    if not results:
        return "Sorry, I could not find matching products."

    answer = "Here are some products you may like:\n\n"

    for index, score in results:

        row = products_df.iloc[index]

        answer += (
            f"• {row['product_name']}\n"
            f"  Price: ₹{row['price']}\n"
            f"  {row['description']}\n\n"
        )

    return answer


# SENTIMENT

def get_sentiment(text):

    result = sentiment_model(text)[0]

    label = result["label"]
    score = result["score"]

    if score < 0.65:
        return "NEUTRAL"

    return label

# REVIEW ANALYSIS

def review_analysis(query):

    product_name = find_product(query)

    if product_name is None:

        results = find_similar_products(query, 1)

        if not results:
            return "Please mention the product name."

        index = results[0][0]

        product_name = products_df.iloc[index]["product_name"]

    product_row = products_df[
        products_df["product_name"] == product_name
    ]

    product_id = product_row.iloc[0]["product_id"]

    reviews = reviews_df[
        reviews_df["product_id"] == product_id
    ]

    if reviews.empty:
        return "No reviews are available for this product."

    positive = 0
    negative = 0
    neutral = 0

    output = f"Reviews for {product_name}\n\n"

    for review in reviews["review_text"]:

        sentiment = get_sentiment(review)

        if sentiment == "POSITIVE":
            positive += 1

        elif sentiment == "NEGATIVE":
            negative += 1

        else:
            neutral += 1

        output += (
            f"Review: {review}\n"
            f"Sentiment: {sentiment}\n\n"
        )

    output += "Review Summary\n"
    output += f"Positive: {positive}\n"
    output += f"Negative: {negative}\n"
    output += f"Neutral: {neutral}"

    return output


# MAIN CHATBOT PROCESS

def process_query(user_query):

    query_lower = user_query.lower()

    # FAQ

    faq_index, faq_score = find_best_faq(user_query)

    if faq_score >= 0.60:

        return faq_df.iloc[faq_index]["answer"]


    # REVIEW

    review_words = [
        "review",
        "reviews",
        "customer",
        "customers",
        "happy",
        "complaint",
        "complaints",
        "opinion",
        "say about"
    ]

    if any(word in query_lower for word in review_words):

        return review_analysis(user_query)


    # RECOMMENDATION

    recommendation_words = [
        "recommend",
        "recommendation",
        "suggest",
        "similar",
        "alternative"
    ]

    if any(
        word in query_lower
        for word in recommendation_words
    ):

        return recommend_products(user_query)


    # PRODUCT QUESTION

    return product_question(user_query)


# GUI

def send_message():

    user_query = entry.get().strip()

    if user_query == "":
        return

    # Display user message
    chat_box.config(state=tk.NORMAL)

    chat_box.insert(
        tk.END,
        "You: " + user_query + "\n\n"
    )

    chat_box.config(state=tk.DISABLED)

    entry.delete(0, tk.END)

    # Show thinking message
    chat_box.config(state=tk.NORMAL)

    chat_box.insert(
        tk.END,
        "Bot: Thinking...\n\n"
    )

    chat_box.config(state=tk.DISABLED)

    # Run chatbot in background
    thread = threading.Thread(
        target=get_bot_response,
        args=(user_query,)
    )

    thread.start()


def get_bot_response(user_query):

    try:

        answer = process_query(user_query)

    except Exception as e:

        answer = "Sorry, an error occurred:\n" + str(e)

    root.after(
        0,
        lambda: display_bot_response(answer)
    )


def display_bot_response(answer):

    chat_box.config(state=tk.NORMAL)

    # Remove "Thinking..."
    content = chat_box.get(
        "1.0",
        tk.END
    )

    if content.endswith("Bot: Thinking...\n\n\n"):
        chat_box.delete(
            "end-3l",
            tk.END
        )

    chat_box.insert(
        tk.END,
        "Bot: " + answer + "\n\n"
    )

    chat_box.config(state=tk.DISABLED)

    chat_box.see(tk.END)


def clear_chat():

    chat_box.config(state=tk.NORMAL)

    chat_box.delete(
        "1.0",
        tk.END
    )

    chat_box.insert(
        tk.END,
        "Bot: Hello! Welcome to the E-Commerce Chatbot.\n"
        "How can I help you today?\n\n"
    )

    chat_box.config(state=tk.DISABLED)


# CREATE WINDOW

root = tk.Tk()

root.title("E-Commerce Chatbot")

root.geometry("800x600")

root.minsize(600, 450)

# TITLE

title = tk.Label(
    root,
    text="E-Commerce Chatbot",
    font=("Arial", 22, "bold")
)

title.pack(pady=10)


subtitle = tk.Label(
    root,
    text="Qwen + Ollama | FAQ | Recommendations | Reviews",
    font=("Arial", 11)
)

subtitle.pack()


# CHAT AREA

chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    state=tk.DISABLED
)

chat_box.pack(
    padx=20,
    pady=15,
    fill=tk.BOTH,
    expand=True
)

# WELCOME MESSAGE

chat_box.config(state=tk.NORMAL)

chat_box.insert(
    tk.END,
    "Bot: Hello! Welcome to the E-Commerce Chatbot.\n"
    "How can I help you today?\n\n"
)

chat_box.config(state=tk.DISABLED)


# INPUT FRAME

input_frame = tk.Frame(root)

input_frame.pack(
    padx=20,
    pady=10,
    fill=tk.X
)


entry = tk.Entry(
    input_frame,
    font=("Arial", 13)
)

entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    padx=(0, 10)
)


send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 12, "bold"),
    command=send_message
)

send_button.pack(
    side=tk.RIGHT
)
# CLEAR BUTTON

clear_button = tk.Button(
    root,
    text="Clear Chat",
    font=("Arial", 10),
    command=clear_chat
)

clear_button.pack(
    pady=(0, 10)
)


# Press Enter to send
entry.bind(
    "<Return>",
    lambda event: send_message()
)


# START GUI

root.mainloop()