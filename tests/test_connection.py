import pytest
from newsapi.connection import NewsAPIConnection


@pytest.fixture
def newsapi_conn():
    return NewsAPIConnection(
        connection_name="NewsAPI", type=NewsAPIConnection)


def test_query(newsapi_conn):
    response = newsapi_conn.everything(q="ChatGPT")

    assert response.get("status") == 'ok'
    assert response.get("totalResults") > 0
    assert "ChatGPT" in response.get("articles")[0].get("title")


def test_top(newsapi_conn):
    response = newsapi_conn.top_headlines(category="Business", country="us")

    assert response.get("status") == 'ok'
    assert response.get("totalResults") > 0
