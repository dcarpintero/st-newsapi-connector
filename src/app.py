from newsapi.connection import NewsAPIConnection
import streamlit as st

st.set_page_config(page_title="NewsAPI-Streamlit Connection Demo App")

st.title("NewsAPI-Streamlit Connector App")

conn = st.experimental_connection("news_data", type=NewsAPIConnection)
df = conn.query('tesla')

st.write('Tesla News:')
st.dataframe(df.head(5))
