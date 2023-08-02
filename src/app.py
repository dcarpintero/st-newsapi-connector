from newsapi.connection import NewsAPIConnection
import streamlit as st

st.set_page_config(page_title="NewsAPI-Streamlit Connection Demo App")
st.title("NewsAPI-Streamlit Connector App")

conn = st.experimental_connection("NewsAPI", type=NewsAPIConnection)
df = conn.query('Tesla')

if df is None:
    st.info("No News")
else:
    st.write('Tesla News:')
    st.dataframe(df.head(5))

df = conn.top(country='US', category='Business')
if df is None:
    st.info("No News")
else:
    st.write('Top Business News:')
    st.dataframe(df.head(5))
