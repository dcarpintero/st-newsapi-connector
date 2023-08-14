import requests
import pandas as pd
import streamlit as st

from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Dict, Optional
from requests.adapters import HTTPAdapter


class NewsAPIConnection(ExperimentalBaseConnection[requests.session]):
    """
    Handles a connection with the NewsAPI and retrieves news articles.

    See also: https://docs.streamlit.io/library/advanced-features/connecting-to-data#build-your-own-connection
              https://newsapi.org/docs 
    """

    def _connect(self, **kwargs) -> requests.session:
        """
        Initializes the connection parameters and creates a persistent requests.Session for connecting with the NewsAPI.
        The Session object uses an HTTPAdapter to allow for maximum retries in case of network issues.

        See also: https://docs.python-requests.org/en/latest/user/advanced/#session-objects

        :return: A requests.Session object, with a mounted HTTPAdapter for connection retries
        """
        self.key = st.secrets['NEWSAPI_KEY']
        if not self.key:
            raise ValueError('Missing NEWSAPI_KEY')

        self.base = st.secrets['NEWSAPI_BASE_URL']
        if not self.base:
            raise ValueError('Missing NEWSAPI_BASE_URL')

        self.retries = st.secrets.get('NEWSAPI_MAX_RETRIES', 5)

        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=self.retries))
        return self.session

    def cursor(self) -> requests.Session:
        """
        Gets the current session object, creating a new one if it doesn't exist.

        :return: A requests.Session object for making API requests
        """
        if self.session is None:
            self._connect()
        return self.session

    def _make_api_request(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Performs a GET request to the provided URL and returns the parsed JSON response.

        :param url: URL to send the GET request to
        :return: JSON response data as a dictionary, None in case of an error
        """
        try:
            response = self.cursor().get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except (requests.exceptions.RequestException, ValueError) as e:
            st.error(f'NewsAPI Server Error')
            return None

    def _to_dataframe(self, data: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
        """
        Converts the JSON data containing News Articles into a DataFrame.

        :param data: JSON data from the NewsAPI response
        :return: DataFrame of News Articles, None if no Articles were found
        """
        if data is None:
            return None

        articles = data.get('articles', None)
        return pd.DataFrame(articles)

    def query(self, topic: str, ttl: int = 3600) -> Optional[pd.DataFrame]:
        """
        Retrieves News Articles on a specific topic from the NewsAPI.
        The results are cached for a period specified by ttl.

        :param topic: Keywords or phrases to search for in the article title and body.
        :param ttl: Duration to cache the result (in seconds)

        :return: DataFrame containing News Articles on the topic, None in case of an error
        """
        @cache_data(ttl=ttl)
        def _query(topic: str) -> Optional[pd.DataFrame]:
            """
            Performs the actual API call and data conversion.
            """
            url = f"{self.base}everything?q={topic}&apiKey={self.key}"

            data = self._make_api_request(url)
            return self._to_dataframe(data)

        return _query(topic)

    def top(self, country: str = 'US', category: str = '', ttl: int = 3600) -> Optional[pd.DataFrame]:
        """
        Retrieves Top-Headlines Articles in a specific country ('US' by default) and category from the NewsAPI.
        The results are cached for a period specified by ttl.

        :param country: The 2-letter ISO 3166-1 code of the country you want to get headlines for.
        :param category: The category of the news. Options include: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'
        :param ttl: Duration to cache the result (in seconds)
        :return: DataFrame containing the Top-Headlines Articles, None in case of an error
        """
        @cache_data(ttl=ttl)
        def _query(country: str, category: str) -> Optional[pd.DataFrame]:
            """
            Performs the actual API call and data conversion.
            """
            url = f"{self.base}top-headlines?country={country}&category={category}&apiKey={self.key}"

            data = self._make_api_request(url)
            return self._to_dataframe(data)

        return _query(country, category)
