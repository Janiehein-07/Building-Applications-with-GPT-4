import re


def preprocess_text(text):
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove unwanted special characters
    text = re.sub(r'[^\w\s.,;:!?()%-]', '', text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text