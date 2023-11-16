[![Open_inStreamlit](https://img.shields.io/badge/Open%20In-Streamlit-red?logo=Streamlit)](https://newsapi-connector.streamlit.app/)
[![Python](https://img.shields.io/badge/python-%203.8-blue.svg)](https://www.python.org/)
[![PyPi](https://img.shields.io/pypi/v/st-newsapi-connector)](https://pypi.org/project/st-newsapi-connector/)
[![Build](https://img.shields.io/github/actions/workflow/status/dcarpintero/st-newsapi-connector/codecov.yml?branch=main)](https://pypi.org/project/st-newsapi-connector/)
[![CodeFactor](https://www.codefactor.io/repository/github/dcarpintero/st-newsapi-connector/badge)](https://www.codefactor.io/repository/github/dcarpintero/st-newsapi-connector)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/dcarpintero/st-newsapi-connector/blob/main/LICENSE)

# 📰 Streamlit-NewsAPI Data Connector

<p align="center">
  <img src="./assets/st-newsapi-connector.png">
</p>

Connect to [NewsAPI](https://newsapi.org/) from your Streamlit app. Powered by ```st.experimental_connection()```. Works with Streamlit >= 1.28. Read more about Streamlit Connections in the [official docs](https://blog.streamlit.io/introducing-st-experimental_connection/). 

Contributions to this repo are welcome. If you are interested in helping to maintain it, reach out to us. 

## 🚀 Quickstart

1. Clone the repository:
```
git clone git@github.com:dcarpintero/st-newsapi-connector.git
```

2. Create and Activate a Virtual Environment:

```
Windows:

py -m venv .venv
.venv\scripts\activate

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Launch Web Application

```
streamlit run ./app.py
```

## 📄 Minimal Integration

```python
# src/app.py

import streamlit as st
from st_newsapi_connector.connection import NewsAPIConnection

conn_newsapi = st.connection("NewsAPI", type=NewsAPIConnection)

# Retrieves News Articles on a specific topic from the NewsAPI
df = conn_newsapi.everything(topic="AI, LLMs")
st.dataframe(df)

# Retrieves Top-Headlines in a country and category from the NewsAPI
df = conn_newsapi.top_headlines(country='US', category='Science')
st.dataframe(df)
```

```toml
# .streamlit/secrets.toml

NEWSAPI_KEY = 'your-newsapi-key'
NEWSAPI_BASE_URL = 'https://newsapi.org/v2/'
```

```txt
# requirements.txt

pandas==1.5.1
pycountry==22.3.5
requests==2.31.0
streamlit==1.28.1
```

## 👩‍💻 Streamlit Web App

Demo Web App deployed to [Streamlit Cloud](https://streamlit.io/cloud) and available at https://newsapi-connector.streamlit.app/ 

## 📚 References

- [Streamlit BaseConnection](https://docs.streamlit.io/library/api-reference/connections/st.connections.baseconnection)
- [Streamlit Connection](https://docs.streamlit.io/library/api-reference/connections/st.connection)
- [Get Started with Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [NewsAPI Dcoumentation](https://newsapi.org/docs)

