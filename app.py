"""
Web-based Demo App for the Streamlit-NewsAPI Connector.

Author:
    @dcarpintero : https://github.com/dcarpintero
"""
import streamlit as st
import pandas as pd

from pycountry import countries
from typing import Any, Dict, List, Optional
from datetime import datetime


from st_newsapi_connector.connection import NewsAPIConnection


def get_country_code(name: str) -> str:
    """Return the 2-letter country code for a given country name."""
    try:
        return countries.get(name=name).alpha_2
    except AttributeError:
        raise ValueError(f'No country code found for "{name}"')


def get_country_names(codes: List[str]) -> List[str]:
    """Return a list of country names for the given list of country codes."""
    return [countries.get(alpha_2=code).name for code in codes]


def format_date(date_string: str) -> Optional[str]:
    try:
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    except (ValueError, TypeError):
        return None
    return date.strftime('%d %B %Y')


def to_dataframe(data: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    """
    Converts the JSON data containing News Articles into a DataFrame.

    :param data: JSON data from the NewsAPI response
    :return: DataFrame of News Articles, None if no Articles were found
    """
    if data is None:
        return None

    articles = data.get('articles', None)
    return pd.DataFrame(articles)


COUNTRY_CODES = [
    'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb',
    'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl',
    'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua',
    'us', 've', 'za'
]

COUNTRY_NAMES = get_country_names(COUNTRY_CODES)


def sidebar():
    """Configure the sidebar and return the user's preferences."""
    st.sidebar.header("💡 Streamlit-NewsAPI-Connector")
    with st.sidebar.expander("🔎 TOPIC", expanded=True):
        topic = st.text_input(
            'Keywords or phrases to search in the News', 'AI, LLMs')
        topic = topic.strip()
        if not topic:
            st.warning('Please enter a valid topic.')

    with st.sidebar.expander("🔝 TOP-STORIES", expanded=True):
        category = st.selectbox(
            'Category', ('Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'), index=4)

        country = st.selectbox('Country', COUNTRY_NAMES, index=51)

    with st.sidebar.expander("🔧 FIELDS", expanded=True):
        fields = st.multiselect(
            "Fields",
            ['source', 'author', 'title', 'description',
                'url', 'urlToImage', 'publishedAt', 'content'],
            ['title', 'description', 'url', 'publishedAt'],
            key="Fields",
            label_visibility="hidden"
        )

    feed = st.sidebar.slider('Story Feed', min_value=0,
                             max_value=100, value=10, step=5)

    return topic, category, country, fields, feed


def display_news(df, feed=5):
    if df is None:
        st.info("No News")
    else:
        for i in range(min(feed, len(df))):
            story = df.iloc[i]

            title = story["title"]
            url = story["url"]
            urlToImage = story["urlToImage"]
            publishedAt = format_date(story["publishedAt"])

            if title is not None:
                if publishedAt is not None:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if urlToImage is not None:
                            st.image(urlToImage, width=150)
                    with col2:
                        st.markdown(f'[{title}]({url})')
                        st.text(publishedAt)


def display_news_as_raw(df, fields):
    if df is None:
        st.info("No News")
    else:
        st.dataframe(df[fields], hide_index=True)


def layout(conn_newsapi, topic, category, country, fields, feed):
    """
    Defines Interface Layout
    """
    st.header("📰 Your Briefing Articles")
    tab_topic, tab_headlines, tab_raw = st.tabs(
        [topic, f'Top Stories in {category} ({country})', "Raw"])

    # Your Topic
    with tab_topic:
        if topic:
            data = conn_newsapi.everything(q=topic)
            df = to_dataframe(data)
            display_news(df, feed)

    # Top Stories
    with tab_headlines:
        data = conn_newsapi.top_headlines(
            country=get_country_code(country), category=category)
        df = to_dataframe(data)
        display_news(df, feed)

    # Raw
    with tab_raw:
        data = conn_newsapi.everything(q=topic)
        df = to_dataframe(data)
        display_news_as_raw(df, fields)


def main():
    """
    Set up user preferences, and layout.
    """
    st.set_page_config(
        page_title="Streamlit-NewsAPI Demo App",
        page_icon="📰",
        initial_sidebar_state="expanded",
        menu_items={"About": "Built by @dcarpintero with Streamlit & NewsAPI"},
    )

    conn_newsapi = st.connection(
        "NewsAPI", type=NewsAPIConnection)
    topic, category, country, fields, feed = sidebar()
    layout(conn_newsapi, topic, category, country, fields, feed)


if __name__ == "__main__":
    main()
