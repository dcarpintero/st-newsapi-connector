"""
Web-based Demo App for the Streamlit-NewsAPI Connector.

Author:
    @dcarpintero : https://github.com/dcarpintero
"""
import streamlit as st
import pycountry

from newsapi.connection import NewsAPIConnection

st.set_page_config(
    page_title="Streamlit-NewsAPI Demo App",
    page_icon="☘️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Made by @dcarpintero"},
)

_usr = {
    "topic": "",
    "category": "",
    "country_code": "",
    "yy_start": 2020,
    "yy_end": 2023,
}

country_codes = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt',
                 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru',
                 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']

country_names = [pycountry.countries.get(
    alpha_2=code).name for code in country_codes]
country_dict = dict(zip(country_names, country_codes))


def _get_country_code(country_name: str) -> str:
    """Returns the 2-letter country code for a given country name."""
    try:
        return country_dict[country_name]
    except KeyError:
        raise ValueError(f'No country code found for "{country_name}"')


def sidebar():
    """
    Defines User Options.
    """
    st.sidebar.header("NewsAPI")

    Topic = st.sidebar.checkbox("Topic", value=True, disabled=False)
    TopHeadlines = st.sidebar.checkbox(
        "Top-Headlines", value=False, disabled=False)

    with st.sidebar.expander("Topic:", expanded=True):
        _usr["topic"] = st.text_input(
            'Keywords or phrases to search in the News', 'Tesla')

    with st.sidebar.expander("Top-Headlines:", expanded=True):
        _usr["category"] = st.selectbox(
            'Category', ('Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'))

        _usr["country"] = st.selectbox(
            'Country', (country_names))


def layout():
    """
    Defines Interface Layout
    """
    news = st.experimental_connection("NewsAPI", type=NewsAPIConnection)

    df = news.query('Tesla')

    if df is None:
        st.info("No News")
    else:
        st.write('Tesla News:')
        st.dataframe(df.head(5))

    df = news.top(country='US', category='Business')
    if df is None:
        st.info("No News")
    else:
        st.write('Top Business News:')
        st.dataframe(df.head(5))

    df = news.top()
    if df is None:
        st.info("No News")
    else:
        st.write('Top News:')
        st.dataframe(df.head(5))


def main():
    """
    Set up user preferences, and layout
    """
    sidebar()
    layout()


if __name__ == "__main__":
    main()
