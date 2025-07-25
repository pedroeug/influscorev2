import streamlit as st
from googlesearch import search as google_search
import requests, re, json
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

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

        # YouTube Results via scraping
        st.subheader("Resultados YouTube")
        try:
            yt_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            headers = {"User-Agent":"Mozilla/5.0"}
            resp = requests.get(yt_url, headers=headers, timeout=10)
            html = resp.text
            data_match = re.search(r"var ytInitialData = (\{.*?\});", html, re.DOTALL)
            youtube_results = []
            if data_match:
                data = json.loads(data_match.group(1))
                sections = data.get("contents", {})                              .get("twoColumnSearchResultsRenderer", {})                              .get("primaryContents", {})                              .get("sectionListRenderer", {})                              .get("contents", [])
                for sec in sections:
                    items = sec.get("itemSectionRenderer", {}).get("contents", [])
                    for it in items:
                        video = it.get("videoRenderer")
                        if not video: continue
                        title = video.get("title", {}).get("runs", [{}])[0].get("text", "")
                        vid = video.get("videoId", "")
                        url = f"https://www.youtube.com/watch?v={vid}"
                        youtube_results.append({"title": title, "url": url})
                        if len(youtube_results) >= 5: break
                    if len(youtube_results) >= 5: break
            else:
                st.warning("Não foi possível extrair dados do YouTube; tente novamente mais tarde.")
            st.write(youtube_results)
        except Exception as e:
            st.error(f"Erro na busca do YouTube: {e}")

        # Twitter Results via Google
        st.subheader("Resultados Twitter/X")
        twitter_results = []
        for url in google_search(f"site:twitter.com {query}", num_results=5, lang='pt'):
            twitter_results.append(url)
        st.write(twitter_results)
