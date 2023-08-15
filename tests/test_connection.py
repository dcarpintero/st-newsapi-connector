import pytest
import requests_mock
from unittest.mock import MagicMock

from newsapi.connection import NewsAPIConnection


@pytest.fixture
def news_api_connection():
    return NewsAPIConnection(
        connection_name="NewsAPI", type=NewsAPIConnection)


def test_query(news_api_connection):
    response = news_api_connection.everything("ChatGPT")

    assert response.get("status") == 'ok'
    assert response.get("totalResults") > 0
    assert "ChatGPT" in response.get("articles")[0].get("title")


def test_top(news_api_connection):
    response = news_api_connection.top_headlines(category="Business")

    assert response.get("status") == 'ok'
    assert response.get("totalResults") > 0
