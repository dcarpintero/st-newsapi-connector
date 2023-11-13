import requests
import streamlit as st

from streamlit.connections import BaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Dict, Optional
from requests.adapters import HTTPAdapter


class NewsAPIConnection(BaseConnection[requests.session]):
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
        self.key = kwargs.get('NEWSAPI_KEY') or st.secrets['NEWSAPI_KEY']
        if not self.key:
            raise ValueError('Missing NEWSAPI_KEY')

        self.base = kwargs.get(
            'NEWSAPI_BASE_URL') or st.secrets['NEWSAPI_BASE_URL']
        if not self.base:
            raise ValueError('Missing NEWSAPI_BASE_URL')

        self.retries = kwargs.get('NEWSAPI_MAX_RETRIES') or st.secrets.get(
            'NEWSAPI_MAX_RETRIES', 5)

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

    def everything(self, ttl: int = 3600, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Retrieves News Articles on a specific topic from the NewsAPI.
        The results are cached for a period specified by ttl.

        :param kwargs: Requests parameters as defined in https://newsapi.org/docs/endpoints/everything
        :param ttl: Duration to cache the result (in seconds)

        :return: Dictionary containing:
            - status: If the request was successful or not
            - totalResults: The total number of results available for your request.
            - articles: The results of the request.
        """
        @cache_data(ttl=ttl)
        def _everything(**_kwargs) -> Optional[Dict[str, Any]]:
            """
            Performs the actual API call and data conversion.
            """
            url = f"{self.base}everything?apiKey={self.key}"
            return self._make_api_request(url=url, params=_kwargs)

        return _everything(**kwargs)

    def top_headlines(self, ttl: int = 3600, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Retrieves Top-Headlines Articles in a specific country ('US' by default) and category from the NewsAPI.
        The results are cached for a period specified by ttl.

        :param kwargs: Requests parameters as defined in https://newsapi.org/docs/endpoints/top-headlines
        :param ttl: Duration to cache the result (in seconds)
        :return: Dictionary containing:
            - status: If the request was successful or not
            - totalResults: The total number of results available for your request.
            - articles: The results of the request.
        """
        @cache_data(ttl=ttl)
        def _top_headlines(**_kwargs) -> Optional[Dict[str, Any]]:
            """
            Performs the actual API call and data conversion.
            """
            url = f"{self.base}top-headlines?apiKey={self.key}"
            return self._make_api_request(url=url, params=_kwargs)

        return _top_headlines(**kwargs)

    def _make_api_request(self, url: str, params: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Performs a GET request to the provided URL and returns the parsed JSON response.

        :param url: URL to send the GET request to
        :return: JSON response data as a dictionary, None in case of an error
        """
        try:
            response = self.cursor().get(url=url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('results') == 0 or data.get('status') != 'ok':
                return None
            return data
        except (requests.exceptions.RequestException, ValueError) as e:
            st.error(f'NewsAPI Server Error')
            return None
