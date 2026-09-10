import streamlit as st

from blog_generator import generate_blog
from title_generator import generate_title
from summary_generator import generate_summary
from seo_generator import generate_seo
from file_manager import save_blog


st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide"
)


st.title("✍️ AI-Powered Blog Content Generator")

st.write(
    "Generate blogs, titles, summaries, SEO keywords "
    "and meta descriptions using Ollama."
)


topic = st.text_input(
    "Blog Topic",
    placeholder="Enter your blog topic"
)


style = st.selectbox(
    "Writing Style",
    [
        "Professional",
        "Technical",
        "Casual",
        "Educational",
        "Creative"
    ]
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Informative",
        "Persuasive",
        "Conversational"
    ]
)


word_count = st.number_input(
    "Word Count",
    min_value=100,
    max_value=3000,
    value=500,
    step=100
)


if st.button("Generate Blog"):

    if not topic:

        st.warning("Please enter a blog topic.")

    else:

        with st.spinner("Generating blog..."):

            blog = generate_blog(
                topic,
                style,
                tone,
                word_count
            )

            titles = generate_title(topic)

            summary = generate_summary(blog)

            seo = generate_seo(blog)


        st.subheader("Blog Titles")
        st.write(titles)

        st.subheader("Generated Blog")
        st.write(blog)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("SEO Keywords & Meta Description")
        st.write(seo)

        filename = save_blog(
            titles,
            blog,
            summary,
            seo
        )

        st.success(
            f"Blog saved successfully: {filename}"
        )