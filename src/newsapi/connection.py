from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
import pandas as pd
import streamlit as st

import requests


class NewsAPIConnection(ExperimentalBaseConnection):
    """Basic st.experimental_connection implementation for NewsAPI"""

    def _connect(self):
        self.key = st.secrets['NEWSAPI_KEY']
        self.base = st.secrets['NEWSAPI_BASE_URL']

    def query(self, topic: str, ttl: int = 3600) -> pd.DataFrame:

        @cache_data(ttl=ttl)
        def _query(topic: str) -> pd.DataFrame:
            url = f"{self.base}everything?q={topic}&apiKey={self.key}"
            response = requests.get(url)
            data = response.json()

            return pd.DataFrame(data['articles'])

        return _query(topic)
