import os
from datetime import datetime


def save_blog(title, blog, summary, seo):

    os.makedirs("generated_blogs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"generated_blogs/blog_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:

        file.write("BLOG TITLE\n")
        file.write("=" * 50 + "\n")
        file.write(title + "\n\n")

        file.write("BLOG\n")
        file.write("=" * 50 + "\n")
        file.write(blog + "\n\n")

        file.write("SUMMARY\n")
        file.write("=" * 50 + "\n")
        file.write(summary + "\n\n")

        file.write("SEO\n")
        file.write("=" * 50 + "\n")
        file.write(seo + "\n")

    return filename