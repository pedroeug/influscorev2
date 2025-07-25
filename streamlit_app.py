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
    .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%); background-size: 200% 200%; animation: gradientShift 6s ease infinite; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; line-height: 1.1; }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .subtitle { text-align: center; color: #64748b !important; font-size: 1.4rem; margin-bottom: 2rem; font-weight: 400; line-height: 1.5; }
    .real-badge { background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: white !important; padding: 0.5rem 1rem !important; border-radius: 20px !important; font-size: 0.9rem !important; font-weight: 600 !important; margin: 0.3rem !important; }
    .search-result { background: white !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 1rem !important; margin: 0.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# Função para converter texto de data relativa em dias
def relative_to_days(text: str) -> int:
    m = re.search(r"(\d+)", text)
    num = int(m.group(1)) if m else 0
    t = text.lower()
    if 'ano' in t: return num * 365
    if 'mês' in t or 'mes' in t: return num * 30
    if 'semana' in t: return num * 7
    if 'dia' in t: return num
    return 9999

# Data inicial para filtro de 90 dias
ninety_days_ago = datetime.now() - timedelta(days=90)
start_date_str = ninety_days_ago.strftime("%Y-%m-%d")

class RealSearchAnalyzer:
    def search_web_real(self, query: str, max_results: int = 10):
        st.info(f"🔍 Buscando REAL no Google: {query} (desde {start_date_str})")
        q = f"{query} after:{start_date_str}"
        results = [{'url': url, 'source': 'Google'} for url in google_search(q, num_results=max_results, lang='pt')]
        st.success(f"✅ {len(results)} resultados REAIS do Google")
        return results

    def search_youtube_real(self, query: str, max_results: int = 10):
        st.info(f"📺 Buscando REAL no YouTube: {query} (até 90 dias)")
        yt_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(yt_url, headers=headers, timeout=10)
        data_match = re.search(r"var ytInitialData = (\{.*?\});", resp.text, re.DOTALL)
        results = []
        if data_match:
            data = json.loads(data_match.group(1))
            contents = data.get('contents', {})                .get('twoColumnSearchResultsRenderer', {})                .get('primaryContents', {})                .get('sectionListRenderer', {})                .get('contents', [])
            for sec in contents:
                items = sec.get('itemSectionRenderer', {}).get('contents', [])
                for it in items:
                    vid = it.get('videoRenderer')
                    if not vid: continue
                    pub = vid.get('publishedTimeText', {}).get('simpleText', '')
                    if relative_to_days(pub) > 90: continue
                    title = vid.get('title', {}).get('runs', [{}])[0].get('text', '')
                    vid_id = vid.get('videoId', '')
                    results.append({'title': title, 'url': f"https://www.youtube.com/watch?v={vid_id}", 'source': 'YouTube'})
                    if len(results) >= max_results: break
                if len(results) >= max_results: break
        st.success(f"✅ {len(results)} vídeos REAIS do YouTube")
        return results

    def search_twitter_real(self, query: str, max_results: int = 10):
        st.info(f"🐦 Buscando REAL no Twitter/X: {query} (desde {start_date_str})")
        q = f"site:twitter.com {query} since:{start_date_str}"
        results = [{'url': url, 'source': 'Twitter'} for url in google_search(q, num_results=max_results, lang='pt')]
        st.success(f"✅ {len(results)} resultados REAIS do Twitter/X")
        return results

# Interface do usuário
st.markdown('<h1 class="main-header">🔍 InfluScore Real</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análise REAL - Últimos 90 dias apenas</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;">'
             '<span class="real-badge">🔍 Google REAL</span>'
             '<span class="real-badge">📺 YouTube REAL</span>'
             '<span class="real-badge">🐦 Twitter/X REAL</span>'
             '</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    influencer = st.text_input("", placeholder="Digite o nome do influenciador...", key="input")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Fazer Busca REAL", use_container_width=True):
        if not influencer:
            st.error("⚠️ Por favor, digite um influenciador.")
        else:
            analyzer = RealSearchAnalyzer()
            prog = st.progress(0)
            google_res = analyzer.search_web_real(influencer)
            prog.progress(33)
            yt_res = analyzer.search_youtube_real(influencer)
            prog.progress(66)
            tw_res = analyzer.search_twitter_real(influencer)
            prog.progress(100)
            prog.empty()

            st.markdown("---")
            st.subheader("🔍 Resultados Google")
            for item in google_res:
                st.markdown(f"- {item['url']}")

            st.subheader("📺 Resultados YouTube")
            for item in yt_res:
                st.markdown(f"- {item['title']} (<a href='{item['url']}' target='_blank'>Link</a>)", unsafe_allow_html=True)

            st.subheader("🐦 Resultados Twitter/X")
            for item in tw_res:
                st.markdown(f"- <a href='{item['url']}' target='_blank'>{item['url']}</a>", unsafe_allow_html=True)

            st.markdown("---")
            if st.button("🔄 Nova Busca", use_container_width=True): st.experimental_rerun()