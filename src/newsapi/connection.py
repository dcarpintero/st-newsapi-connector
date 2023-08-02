import requests
import pandas as pd
import streamlit as st

from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Dict, Optional


class NewsAPIConnection(ExperimentalBaseConnection):
    """Handles connection with the NewsAPI to retrieve news articles."""

    def _connect(self):
        """Initializes parameters to connect with the NewsAPI."""
        self.key = st.secrets['NEWSAPI_KEY']
        self.base = st.secrets['NEWSAPI_BASE_URL']

    def _make_api_request(self, url: str) -> Optional[Dict[str, Any]]:
        """Makes a GET request to the provided URL and returns the parsed JSON response."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except (requests.exceptions.RequestException, ValueError) as e:
            st.error(f'Error: {e}')
            return None

    def query(self, topic: str, ttl: int = 3600) -> Optional[pd.DataFrame]:
        """
        Queries the NewsAPI for news articles on a given topic.
        Data is cached for a duration given by ttl.
        """

        @cache_data(ttl=ttl)
        def _query(topic: str) -> Optional[pd.DataFrame]:
            """Performs the actual API call and data processing."""
            url = f"{self.base}everything?q={topic}&apiKey={self.key}"

            data = self._make_api_request(url)
            if data is None:
                return None

            articles = data.get('articles', None)

            if articles is None:
                st.info('No News found')
                return None

            return pd.DataFrame(articles)

        return _query(topic)
