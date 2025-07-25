import streamlit as st
from googlesearch import search as google_search
from youtubesearchpython import VideosSearch

st.set_page_config(page_title="InfluScore Real", page_icon="🔍", layout="wide")
st.title("🔍 InfluScore Real")
st.write("Busca real no Google, YouTube e Twitter/X")

query = st.text_input("Digite o nome do influenciador")

if st.button("🔍 Buscar"):
    if not query:
        st.error("Por favor, digite um nome para buscar.")
    else:
        # Google Results
        st.subheader("Resultados Google")
        google_results = []
        for url in google_search(query, num_results=5, lang='pt'):
            google_results.append(url)
        st.write(google_results)

        # YouTube Results
        st.subheader("Resultados YouTube")
        try:
            videos_search = VideosSearch(query, limit=5)
            youtube_results = []
            for v in videos_search.result().get('result', []):
                youtube_results.append({
                    "title": v.get('title'),
                    "link": v.get('link')
                })
            st.write(youtube_results)
        except Exception as e:
            st.error(f"Erro na busca do YouTube: {e}")

        # Twitter Results via Google
        st.subheader("Resultados Twitter/X")
        twitter_results = []
        for url in google_search(f"site:twitter.com {query}", num_results=5, lang='pt'):
            twitter_results.append(url)
        st.write(twitter_results)
