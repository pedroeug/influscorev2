import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import defaultdict
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Configuração da página
st.set_page_config(
    page_title="InfluScore Real - Busca Verdadeira",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS omitido para brevidade...

class RealSearchAnalyzer:
    def __init__(self):
        # keywords omitted for brevidade...
        self.positive_keywords = [...]
        self.negative_keywords = [...]

    def search_web_real(self, query, max_results=25):
        """Realiza busca simples no Google sem usar API."""
        try:
            st.info(f"🔍 Fazendo busca REAL no Google para: {query}")
            url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}&hl=pt-BR"
            headers = {"User-Agent":("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "lxml")

            results = []
            for block in soup.select("div.tF2Cxc, div.g"):
                anchor = block.find("a", href=True)
                title = block.find("h3")
                snippet = block.find("div", class_="VwiC3b") or block.find("span", class_="aCOpRe")
                if anchor and title:
                    href = anchor["href"]
                    if href.startswith("/url"):
                        m = re.search(r"q=([^&]+)", href)
                        if m: href = requests.utils.unquote(m.group(1))
                    results.append({"title": title.get_text(strip=True),
                                    "snippet": snippet.get_text(" ",strip=True) if snippet else "",
                                    "url": href, "source": "Google"})
                if len(results) >= max_results: break
            st.success(f"✅ Coletados {len(results)} resultados REAIS do Google")
            return results
        except Exception as e:
            st.error(f"Erro na busca real: {str(e)}")
            return []

    def search_youtube_real(self, query, max_results=25):
        """Busca vídeos do YouTube sem usar API, com fallback Invidious."""
        try:
            st.info(f"📺 Fazendo busca REAL no YouTube para: {query}")
            url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            headers = {"User-Agent":"Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            data_match = re.search(r"var ytInitialData = (\{.*?\});", response.text, re.DOTALL)
            results = []
            if data_match:
                data = json.loads(data_match.group(1))
                contents = data.get("contents", {})                               .get("twoColumnSearchResultsRenderer", {})                               .get("primaryContents", {})                               .get("sectionListRenderer", {})                               .get("contents", [])
                for sec in contents:
                    items = sec.get("itemSectionRenderer", {}).get("contents", [])
                    for it in items:
                        vid = it.get("videoRenderer")
                        if not vid: continue
                        title = vid.get("title", {}).get("runs", [{}])[0].get("text","")
                        video_id = vid.get("videoId","")
                        desc_runs = vid.get("descriptionSnippet", {}).get("runs", [])
                        desc = " ".join(r.get("text","") for r in desc_runs)
                        url_vid = f"https://www.youtube.com/watch?v={video_id}"
                        results.append({"title":title, "description":desc, "url":url_vid, "source":"YouTube"})
                        if len(results)>=max_results: break
                    if len(results)>=max_results: break
            # Fallback via Invidious API
            if not results:
                inv_url = f"https://yewtu.be/api/v1/search?q={quote_plus(query)}"
                inv_resp = requests.get(inv_url, headers=headers, timeout=10)
                if inv_resp.status_code == 200:
                    inv_data = inv_resp.json()
                    for entry in inv_data[:max_results]:
                        title = entry.get("title","")
                        url_vid = "https://www.youtube.com/watch?v=" + entry.get("videoId","")
                        desc = entry.get("description","")
                        results.append({"title":title, "description":desc, "url":url_vid, "source":"YouTube"})
            st.success(f"✅ Coletados {len(results)} vídeos REAIS do YouTube")
            return results
        except Exception as e:
            st.error(f"Erro na busca YouTube real: {str(e)}")
            return []

    def search_twitter_real(self, query, max_results=25):
        """Busca posts do Twitter/X usando Google como intermediário."""
        try:
            st.info(f"🐦 Fazendo busca REAL no Twitter/X para: {query}")
            google_results = self.search_web_real(f"site:twitter.com {query}", max_results)
            tweets = []
            for item in google_results:
                url = item.get("url","")
                if "twitter.com" in url and "/status/" in url:
                    tweets.append({"text": item.get("snippet",""), "url":url, "source":"Twitter"})
                    if len(tweets)>=max_results: break
            st.success(f"✅ Coletados {len(tweets)} posts REAIS do Twitter/X")
            return tweets
        except Exception as e:
            st.error(f"Erro na busca Twitter real: {str(e)}")
            return []

    # demais métodos omitidos para brevidade...

# rest of the streamlit app omitted...
