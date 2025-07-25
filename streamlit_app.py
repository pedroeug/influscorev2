import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import re
from googlesearch import search as google_search
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# Configuração da página e CSS moderno
st.set_page_config(
    page_title="InfluScore Real - Busca Verdadeira",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    .main .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1200px; color: #1e293b !important; font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important; color: #1e293b !important; }
    * { color: #1e293b !important; font-family: 'Inter', sans-serif !important; }
    .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%); background-size: 200% 200%; animation: gradientShift 6s ease infinite; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 4rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; letter-spacing: -0.03em; line-height: 1.1; }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .subtitle { text-align: center; color: #64748b !important; font-size: 1.4rem; margin-bottom: 4rem; font-weight: 400; line-height: 1.5; }
    .real-badge { background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: white !important; padding: 0.5rem 1rem !important; border-radius: 20px !important; font-size: 0.9rem !important; font-weight: 600 !important; display: inline-block !important; margin: 0.3rem !important; box-shadow: 0 4px 6px -1px rgba(16,185,129,0.3) !important; }
</style>
""", unsafe_allow_html=True)

# Helper para converter texto relativo em dias
def relative_to_days(text: str) -> int:
    m = re.search(r"(\d+)", text)
    num = int(m.group(1)) if m else 0
    text = text.lower()
    if 'ano' in text:
        return num * 365
    if 'mês' in text or 'mes' in text:
        return num * 30
    if 'semana' in text:
        return num * 7
    if 'dia' in text:
        return num
    return 9999

# Calcula data de 90 dias atrás
ninety_days_ago = datetime.now() - timedelta(days=90)
start_date_str = ninety_days_ago.strftime("%Y-%m-%d")

class RealSearchAnalyzer:
    def search_web_real(self, query: str, max_results: int = 10):
        st.info(f"🔍 Buscando no Google por: {query} (últimos 90 dias)")
        results = []
        q = f"{query} after:{start_date_str}"
        for url in google_search(q, num_results=max_results, lang='pt'):
            results.append({'url': url, 'source': 'Google'})
        st.success(f"✅ {len(results)} resultados do Google")
        return results

    def search_youtube_real(self, query: str, max_results: int = 10):
        st.info(f"📺 Buscando no YouTube por: {query} (últimos 90 dias)")
        yt_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(yt_url, headers=headers, timeout=10)
        html = resp.text
        data_match = re.search(r"var ytInitialData = (\{.*?\});", html, re.DOTALL)
        results = []
        if data_match:
            data = json.loads(data_match.group(1))
            sections = data.get("contents", {})\
                          .get("twoColumnSearchResultsRenderer", {})\
                          .get("primaryContents", {})\
                          .get("sectionListRenderer", {})\
                          .get("contents", [])
            for sec in sections:
                items = sec.get("itemSectionRenderer", {}).get("contents", [])
                for it in items:
                    video = it.get("videoRenderer")
                    if not video:
                        continue
                    pub = video.get("publishedTimeText", {}).get("simpleText", "")
                    if relative_to_days(pub) > 90:
                        continue
                    title = video.get("title", {}).get("runs", [{}])[0].get("text", "")
                    vid_id = video.get("videoId", "")
                    url = f"https://www.youtube.com/watch?v={vid_id}"
                    results.append({'title': title, 'url': url, 'source': 'YouTube'})
                    if len(results) >= max_results:
                        break
                if len(results) >= max_results:
                    break
        st.success(f"✅ {len(results)} vídeos do YouTube")
        return results

    def search_twitter_real(self, query: str, max_results: int = 10):
        st.info(f"🐦 Buscando no Twitter/X por: {query} (últimos 90 dias)")
        results = []
        q = f"site:twitter.com {query} since:{start_date_str}"
        for url in google_search(q, num_results=max_results, lang='pt'):
            results.append({'url': url, 'source': 'Twitter'})
        st.success(f"✅ {len(results)} resultados do Twitter/X")
        return results

# Interface
st.markdown('<h1 class="main-header">🔍 InfluScore Real</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análise com Busca REAL - Apenas últimos 90 dias</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    influencer_name = st.text_input("", placeholder="Digite o nome do influenciador...", key="influencer_input")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Fazer Busca Real", use_container_width=True):
        if not influencer_name:
            st.error("⚠️ Digite um influenciador para busca real.")
        else:
            analyzer = RealSearchAnalyzer()
            progress = st.progress(0)
            g = analyzer.search_web_real(influencer_name)
            progress.progress(33)
            y = analyzer.search_youtube_real(influencer_name)
            progress.progress(66)
            t = analyzer.search_twitter_real(influencer_name)
            progress.progress(100)
            progress.empty()

            st.markdown("---")
            st.markdown("## 🔍 Resultados")
            st.subheader("Google")
            for item in g:
                st.write(item['url'])
            st.subheader("YouTube")
            for item in y:
                st.write(f"{item['title']} - {item['url']}")
            st.subheader("Twitter/X")
            for item in t:
                st.write(item['url'])
            st.button("🔄 Nova Busca")
