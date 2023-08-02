"""
Web-based Demo App for the Streamlit-NewsAPI Connector.

Author:
    @dcarpintero : https://github.com/dcarpintero
"""
import streamlit as st

from pycountry import countries
from typing import List
from datetime import datetime


from newsapi.connection import NewsAPIConnection


def get_country_code(name: str) -> str:
    """Return the 2-letter country code for a given country name."""
    try:
        return countries.get(name=name).alpha_2
    except AttributeError:
        raise ValueError(f'No country code found for "{name}"')


def get_country_names(codes: List[str]) -> List[str]:
    """Return a list of country names for the given list of country codes."""
    return [countries.get(alpha_2=code).name for code in codes]


def format_date(date_string: str) -> str:
    date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date.strftime('%d %B %Y')


COUNTRY_CODES = [
    'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb',
    'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl',
    'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua',
    'us', 've', 'za'
]

COUNTRY_NAMES = get_country_names(COUNTRY_CODES)


def sidebar():
    """Configure the sidebar and return the user's preferences."""
    with st.sidebar.expander("Topic:", expanded=True):
        topic = st.text_input(
            'Keywords or phrases to search in the News', 'ChatGPT')

    with st.sidebar.expander("Top-Headlines:", expanded=True):
        category = st.selectbox(
            'Category', ('Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'), index=6)

        country = st.selectbox('Country', COUNTRY_NAMES, index=51)

    with st.sidebar.expander("Fields:", expanded=True):
        fields = st.multiselect(
            "Fields",
            ['source', 'author', 'title', 'description',
                'url', 'urlToImage', 'publishedAt', 'content'],
            ['title', 'description', 'url', 'publishedAt'],
            key="Fields",
            label_visibility="hidden"
        )

    return topic, category, country, fields


def display_news(df):
    if df is None:
        st.info("No News")
    else:
        for i in range(min(5, len(df))):
            story = df.iloc[i]
            col1, col2 = st.columns([1, 3])
            with col1:
                if story["urlToImage"] is not None:
                    st.image(story["urlToImage"], width=150)
            with col2:
                st.markdown(f'[{story["title"]}]({story["url"]})')
                st.text(format_date(story["publishedAt"]))


def layout(conn_newsapi, topic, category, country):
    """
    Layout
    """
    st.header("📰 Your Briefing Articles")

    # Your Topic
    st.subheader(f'{topic} ::')
    display_news(conn_newsapi.query(topic))

    # Top Stories
    st.subheader(f'Top Stories in {category} ({country}) ::')
    display_news(conn_newsapi.top(country=get_country_code(country),
                                  category=category))


def main():
    """
    Set up user preferences, and layout.
    """
    st.set_page_config(
        page_title="Streamlit-NewsAPI Demo App",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"About": "Built by @dcarpintero"},
    )

    conn_newsapi = st.experimental_connection(
        "NewsAPI", type=NewsAPIConnection)
    topic, category, country, fields = sidebar()
    layout(conn_newsapi, topic, category, country)


if __name__ == "__main__":
    main()
