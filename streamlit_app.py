import streamlit as st
import requests
import json
import time
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

# CSS moderno mantido
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        color: #1e293b !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #1e293b !important;
    }
    
    * {
        color: #1e293b !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #64748b !important;
        font-size: 1.4rem;
        margin-bottom: 4rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.5;
    }
    
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.1),
            0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
        color: #1e293b !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 10px 15px -3px rgba(102, 126, 234, 0.3),
            0 4px 6px -2px rgba(102, 126, 234, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 0.025em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 20px 25px -5px rgba(102, 126, 234, 0.4),
            0 10px 10px -5px rgba(102, 126, 234, 0.2) !important;
        color: #ffffff !important;
    }
    
    .modern-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        color: #1e293b !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .modern-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.15),
            0 20px 25px -5px rgba(102, 126, 234, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    .real-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 20px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
        margin: 0.3rem !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .search-result {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid #667eea !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        color: #1e293b !important;
    }
    
    .keyword-positive {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        color: #065f46 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 12px !important;
        margin: 0.3rem !important;
        display: inline-block !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .keyword-negative {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        color: #991b1b !important;
        padding: 0.5rem 1rem !important;
        border-radius: 12px !important;
        margin: 0.3rem !important;
        display: inline-block !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.2 !important;
    }
    
    p, span, div {
        color: #1e293b !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

class RealSearchAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            'sucesso', 'família', 'caridade', 'educação', 'conquista', 'prêmio', 
            'reconhecimento', 'inovação', 'inspiração', 'liderança', 'amor',
            'felicidade', 'vitória', 'crescimento', 'desenvolvimento', 'ajuda',
            'solidariedade', 'responsabilidade', 'ética', 'transparência',
            'generosidade', 'bondade', 'compaixão', 'união', 'harmonia', 'paz',
            'transformação', 'mudança positiva', 'impacto social', 'benefício',
            'melhoria', 'progresso', 'evolução', 'avanço', 'conhecimento',
            'ensino', 'aprendizado', 'colaboração', 'parceria', 'confiança',
            'verdade', 'sinceridade', 'autenticidade', 'integridade', 'dedicação',
            'perseverança', 'determinação', 'motivação', 'otimismo', 'esperança'
        ]
        
        self.negative_keywords = [
            'roubo', 'casino', 'preso', 'escândalo', 'polêmica', 'fraude',
            'golpe', 'processo', 'condenação', 'drogas', 'violência', 'agressão',
            'corrupção', 'crime', 'prisão', 'investigação', 'acusação',
            'controversia', 'problema', 'conflito', 'briga', 'discussão',
            'furto', 'entorpecentes', 'álcool', 'dependência', 'abuso',
            'pancadaria', 'luta', 'confronto', 'hostilidade', 'crise',
            'confusão', 'bagunça', 'tumulto', 'alvoroço', 'suborno',
            'propina', 'lavagem', 'sonegação', 'mentira', 'falsidade',
            'enganação', 'trapaça', 'racismo', 'preconceito', 'discriminação',
            'intolerância', 'machismo', 'homofobia', 'xenofobia', 'bullying',
            'assédio', 'exploração', 'manipulação', 'chantagem', 'extorsão'
        ]
    
    def search_web_real(self, query, max_results=25):
        """Realiza busca simples no Google sem usar API."""
        try:
            st.info(f"🔍 Fazendo busca REAL no Google para: {query}")

            params = {"q": query, "num": max_results, "hl": "pt-BR"}
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0 Safari/537.36"
                )
            }
            response = requests.get(
                "https://www.google.com/search", params=params, headers=headers, timeout=10
            )
            soup = BeautifulSoup(response.text, "html.parser")

            blocks = soup.select("div.tF2Cxc")
            if not blocks:
                blocks = soup.select("div.g")

            results = []
            for block in blocks:
                anchor = block.find("a", href=True)
                title = block.find("h3")
                if not anchor or not title:
                    continue
                href = anchor["href"]
                if href.startswith("/url"):
                    q_match = re.search(r"q=([^&]+)", href)
                    if q_match:
                        href = requests.utils.unquote(q_match.group(1))
                snippet = ""
                snip_tag = block.find("div", class_="VwiC3b") or block.find("span", class_="aCOpRe")
                if snip_tag:
                    snippet = snip_tag.get_text(" ", strip=True)
                results.append(
                    {
                        "title": title.get_text(strip=True),
                        "snippet": snippet,
                        "url": href,
                        "source": "Google",
                    }
                )
                if len(results) >= max_results:
                    break

            st.success(f"✅ Coletados {len(results)} resultados REAIS do Google")
            return results

        except Exception as e:
            st.error(f"Erro na busca real: {str(e)}")
            return []
    
    def search_twitter_real(self, query, max_results=25):
        """Busca posts do Twitter usando Google como intermediário."""
        try:
            st.info(f"🐦 Fazendo busca REAL no Twitter/X para: {query}")

            google_results = self.search_web_real(f"site:twitter.com {query}", max_results)

            tweets = []
            for item in google_results:
                if "twitter.com" not in item.get("url", ""):
                    continue
                tweets.append({
                    "text": item.get("snippet", ""),
                    "url": item.get("url"),
                    "source": "Twitter"
                })
                if len(tweets) >= max_results:
                    break

            st.success(f"✅ Coletados {len(tweets)} posts REAIS do Twitter/X")
            return tweets

        except Exception as e:
            st.error(f"Erro na busca Twitter real: {str(e)}")
            return []
    
    def search_youtube_real(self, query, max_results=25):
        """Busca vídeos do YouTube sem usar API."""
        try:
            st.info(f"📺 Fazendo busca REAL no YouTube para: {query}")

            url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            results = []
            data_match = re.search(r"var ytInitialData = (\{.*?\});", response.text)
            if data_match:
                data = json.loads(data_match.group(1))
                sections = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {})\
                    .get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                for sec in sections:
                    items = sec.get("itemSectionRenderer", {}).get("contents", [])
                    for it in items:
                        video = it.get("videoRenderer")
                        if not video:
                            continue
                        title = video.get("title", {}).get("runs", [{}])[0].get("text", "")
                        vid = video.get("videoId")
                        url = f"https://www.youtube.com/watch?v={vid}" if vid else ""
                        desc = ""
                        desc_runs = video.get("descriptionSnippet", {}).get("runs")
                        if desc_runs:
                            desc = " ".join(r.get("text", "") for r in desc_runs)
                        results.append({
                            "title": title,
                            "description": desc,
                            "url": url,
                            "source": "YouTube"
                        })
                        if len(results) >= max_results:
                            break
                    if len(results) >= max_results:
                        break

            st.success(f"✅ Coletados {len(results)} vídeos REAIS do YouTube")
            return results

        except Exception as e:
            st.error(f"Erro na busca YouTube real: {str(e)}")
            return []
    
    def analyze_real_content(self, content):
        """Analisa keywords em conteúdo REAL"""
        if not content:
            return [], []
        
        content_lower = content.lower()
        found_positive = []
        found_negative = []
        
        for keyword in self.positive_keywords:
            if keyword in content_lower:
                found_positive.append(keyword)
        
        for keyword in self.negative_keywords:
            if keyword in content_lower:
                found_negative.append(keyword)
        
        return found_positive, found_negative
    
    def calculate_real_score(self, google_results, youtube_results, twitter_results):
        """Calcula score baseado em dados REAIS"""
        all_content = []
        all_positive_keywords = set()
        all_negative_keywords = set()
        
        # Processa resultados REAIS do Google
        for result in google_results:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            positive_kw, negative_kw = self.analyze_real_content(content)
            
            all_content.append({
                'content': content,
                'source': 'google',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw,
                'url': result.get('url', ''),
                'real': True
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Processa resultados REAIS do YouTube
        for result in youtube_results:
            content = f"{result.get('title', '')} {result.get('description', '')}"
            positive_kw, negative_kw = self.analyze_real_content(content)
            
            all_content.append({
                'content': content,
                'source': 'youtube',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw,
                'url': result.get('url', ''),
                'real': True
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Processa resultados REAIS do Twitter
        for result in twitter_results:
            content = result.get('text', '')
            positive_kw, negative_kw = self.analyze_real_content(content)
            
            all_content.append({
                'content': content,
                'source': 'twitter',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw,
                'url': result.get('url', ''),
                'real': True
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Cálculo do score baseado em dados REAIS
        total_positive = len(all_positive_keywords)
        total_negative = len(all_negative_keywords)
        total_content_count = len(all_content)
        
        # Score base para dados reais
        base_score = 70  # Maior porque são dados reais
        
        # Ajustes baseados em dados reais
        positive_bonus = total_positive * 2
        negative_penalty = total_negative * 4
        real_data_bonus = 10  # Bônus por usar dados reais
        
        final_score = base_score + positive_bonus - negative_penalty + real_data_bonus
        final_score = max(0, min(100, final_score))
        
        # Determina nível de risco
        if final_score >= 85:
            risk_level = 'Muito Baixo'
            risk_color = '#059669'
        elif final_score >= 70:
            risk_level = 'Baixo'
            risk_color = '#65a30d'
        elif final_score >= 50:
            risk_level = 'Médio'
            risk_color = '#d97706'
        elif final_score >= 30:
            risk_level = 'Alto'
            risk_color = '#dc2626'
        else:
            risk_level = 'Muito Alto'
            risk_color = '#991b1b'
        
        stats = {
            'total_content': total_content_count,
            'google_count': len(google_results),
            'youtube_count': len(youtube_results),
            'twitter_count': len(twitter_results),
            'positive_keywords_count': total_positive,
            'negative_keywords_count': total_negative,
            'real_data': True
        }
        
        return int(final_score), risk_level, risk_color, all_positive_keywords, all_negative_keywords, stats, all_content

def create_real_gauge(score, risk_color):
    """Cria gauge para dados reais"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': "Score Baseado em Dados REAIS", 
            'font': {'size': 24, 'color': '#1e293b', 'family': 'Inter'}
        },
        number = {
            'font': {'size': 52, 'color': risk_color, 'family': 'Inter'},
            'suffix': "/100"
        },
        gauge = {
            'axis': {
                'range': [None, 100], 
                'tickwidth': 2, 
                'tickcolor': "#cbd5e1",
                'tickfont': {'size': 14, 'color': '#64748b', 'family': 'Inter'}
            },
            'bar': {'color': risk_color, 'thickness': 0.5},
            'bgcolor': "#f8fafc",
            'borderwidth': 4,
            'bordercolor': "#10b981",  # Verde para indicar dados reais
            'steps': [
                {'range': [0, 30], 'color': "#fee2e2"},
                {'range': [30, 50], 'color': "#fed7aa"},
                {'range': [50, 70], 'color': "#fef3c7"},
                {'range': [70, 85], 'color': "#d1fae5"},
                {'range': [85, 100], 'color': "#a7f3d0"}
            ],
            'threshold': {
                'line': {'color': "#10b981", 'width': 6},  # Verde para dados reais
                'thickness': 0.9,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#1e293b", 'family': "Inter"}
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 InfluScore Real</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análise com Busca REAL - Sem Simulação, Apenas Dados Verdadeiros</p>', unsafe_allow_html=True)
    
    # Badges de dados reais
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <span class="real-badge">🔍 Busca Real no Google</span>
        <span class="real-badge">🐦 Busca Real no Twitter/X</span>
        <span class="real-badge">📺 Busca Real no YouTube</span>
        <span class="real-badge">✅ Zero Simulação</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "",
            placeholder="Digite o nome do influenciador para busca REAL...",
            key="influencer_input",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        analyze_button = st.button("🔍 Fazer Busca REAL (Sem Simulação)", use_container_width=True, type="primary")
    
    if analyze_button and influencer_name:
        analyzer = RealSearchAnalyzer()
        
        # Aviso sobre busca real
        st.markdown(f"""
        <div class="modern-card">
            <h3 style="color: #10b981; text-align: center; margin-bottom: 1rem;">
                🔍 Iniciando Busca REAL sobre {influencer_name}
            </h3>
            <p style="color: #64748b; text-align: center;">
                Coletando dados verdadeiros do Google, YouTube e Twitter/X...
            </p>
            <p style="color: #059669; text-align: center; font-weight: 600;">
                ✅ SEM SIMULAÇÃO - APENAS DADOS REAIS
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        
        # Busca REAL no Google
        google_results = analyzer.search_web_real(influencer_name)
        progress_bar.progress(33)
        time.sleep(1)
        
        # Busca REAL no YouTube
        youtube_results = analyzer.search_youtube_real(influencer_name)
        progress_bar.progress(66)
        time.sleep(1)
        
        # Busca REAL no Twitter
        twitter_results = analyzer.search_twitter_real(influencer_name)
        progress_bar.progress(100)
        time.sleep(1)
        
        # Remove progress
        progress_bar.empty()
        
        # Calcula score com dados reais
        score, risk_level, risk_color, positive_keywords, negative_keywords, stats, all_content = analyzer.calculate_real_score(
            google_results, youtube_results, twitter_results
        )
        
        # Resultados
        st.markdown("---")
        st.markdown(f"## 🔍 Análise REAL: {influencer_name}")
        
        # Contadores de dados reais
        col_count1, col_count2, col_count3 = st.columns(3)
        
        with col_count1:
            st.markdown(f"""
            <div class="modern-card">
                <h3 style="color: #10b981;">🔍 Google (REAL)</h3>
                <h2 style="color: #1e293b; font-size: 2.5rem;">{len(google_results)}</h2>
                <p style="color: #64748b;">resultados REAIS coletados</p>
                <small style="color: #10b981;">✅ Busca real executada</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_count2:
            st.markdown(f"""
            <div class="modern-card">
                <h3 style="color: #10b981;">📺 YouTube (REAL)</h3>
                <h2 style="color: #1e293b; font-size: 2.5rem;">{len(youtube_results)}</h2>
                <p style="color: #64748b;">vídeos REAIS coletados</p>
                <small style="color: #10b981;">✅ Busca real executada</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_count3:
            st.markdown(f"""
            <div class="modern-card">
                <h3 style="color: #10b981;">🐦 Twitter/X (REAL)</h3>
                <h2 style="color: #1e293b; font-size: 2.5rem;">{len(twitter_results)}</h2>
                <p style="color: #64748b;">posts REAIS coletados</p>
                <small style="color: #10b981;">✅ Busca real executada</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Layout principal
        col1, col2 = st.columns([1.3, 0.7])
        
        with col1:
            # Gauge para dados reais
            fig = create_real_gauge(score, risk_color)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Card de risco com dados reais
            st.markdown(f"""
            <div class="modern-card">
                <h3 style="color: #1e293b;">🛡️ Risco (Dados REAIS)</h3>
                <h1 style="color: {risk_color}; font-size: 2.5rem; margin: 1rem 0;">{risk_level.upper()}</h1>
                <p style="color: #64748b; font-size: 1.3rem;">Score: <strong>{score}/100</strong></p>
                <p style="color: #10b981; font-weight: 600;">✅ Baseado em {stats['total_content']} dados REAIS</p>
                <p style="color: #059669; font-size: 0.9rem;">Sem simulação - apenas busca verdadeira</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recomendação
            if score >= 70:
                st.success("✅ **RECOMENDADO** - Dados reais confirmam baixo risco")
            elif score >= 50:
                st.warning("⚠️ **CAUTELA** - Análise real indica risco moderado")
            else:
                st.error("❌ **ALTO RISCO** - Dados reais indicam problemas")
        
        # Keywords encontradas em dados reais
        st.markdown("### 🔍 Keywords Encontradas em Dados REAIS")
        
        col_kw1, col_kw2 = st.columns(2)
        
        with col_kw1:
            st.markdown("**🟢 Palavras Positivas (Dados Reais):**")
            if positive_keywords:
                keywords_html = "".join([f'<span class="keyword-positive">{kw}</span>' for kw in list(positive_keywords)[:10]])
                st.markdown(keywords_html, unsafe_allow_html=True)
                if len(positive_keywords) > 10:
                    st.info(f"+ {len(positive_keywords) - 10} outras palavras positivas em dados reais")
            else:
                st.info("Nenhuma palavra positiva encontrada nos dados reais")
        
        with col_kw2:
            st.markdown("**🔴 Palavras Negativas (Dados Reais):**")
            if negative_keywords:
                keywords_html = "".join([f'<span class="keyword-negative">{kw}</span>' for kw in list(negative_keywords)[:10]])
                st.markdown(keywords_html, unsafe_allow_html=True)
                if len(negative_keywords) > 10:
                    st.warning(f"+ {len(negative_keywords) - 10} outras palavras negativas em dados reais")
            else:
                st.success("✅ Nenhuma palavra negativa encontrada nos dados reais")
        
        # Amostra de dados reais coletados
        st.markdown("### 📰 Amostra dos Dados REAIS Coletados")
        
        # Mostra primeiros resultados reais
        sample_content = all_content[:7]  # Primeiros 7 resultados reais
        
        for item in sample_content:
            content = item['content']
            source = item['source']
            url = item['url']
            positive_kw = item['positive_keywords']
            negative_kw = item['negative_keywords']
            
            # Trunca conteúdo se muito longo
            if len(content) > 200:
                content = content[:200] + "..."
            
            source_icon = '🔍' if source == 'google' else ('📺' if source == 'youtube' else '🐦')
            source_name = 'Google' if source == 'google' else ('YouTube' if source == 'youtube' else 'Twitter/X')
            
            st.markdown(f"""
            <div class="search-result">
                <h4 style="color: #10b981; margin-bottom: 0.5rem;">{source_icon} {source_name} (REAL)</h4>
                <p style="color: #64748b; margin: 0.5rem 0;">{content}</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.5rem 0;">URL: {url}</p>
                <div style="margin-top: 1rem;">
                    <strong style="color: #059669;">Positivas:</strong> {', '.join(positive_kw[:3]) if positive_kw else 'Nenhuma'}<br>
                    <strong style="color: #dc2626;">Negativas:</strong> {', '.join(negative_kw[:3]) if negative_kw else 'Nenhuma'}
                </div>
                <small style="color: #10b981; font-weight: 600;">✅ Dados coletados via busca real</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Estatísticas dos dados reais
        st.markdown("### 📊 Estatísticas dos Dados REAIS")
        
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.metric("📊 Total REAL", stats['total_content'], "dados coletados")
        with col_stats2:
            st.metric("🟢 Keywords Positivas", stats['positive_keywords_count'], "em dados reais")
        with col_stats3:
            st.metric("🔴 Keywords Negativas", stats['negative_keywords_count'], "em dados reais")
        with col_stats4:
            st.metric("🎯 Score REAL", f"{score}/100", f"Risco {risk_level}")
        
        # Botão para nova análise
        st.markdown("---")
        if st.button("🔄 Fazer Nova Busca REAL", use_container_width=True):
            st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("⚠️ Por favor, digite o nome de um influenciador para busca REAL.")
    
    # Informações sobre busca real
    if not analyze_button:
        st.markdown("---")
        st.markdown("### ℹ️ Como Funciona a Busca REAL")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #10b981;">🔍 Busca Real no Google</h4>
                <p style="color: #64748b;">• <strong>25 resultados</strong> coletados diretamente<br>
                • <strong>Títulos e snippets</strong> reais<br>
                • <strong>URLs verificáveis</strong><br>
                • <strong>Zero simulação</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info2:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #10b981;">🐦 Busca Real no Twitter/X</h4>
                <p style="color: #64748b;">• <strong>25 posts</strong> coletados via busca<br>
                • <strong>Textos reais</strong> de tweets<br>
                • <strong>Links verificáveis</strong><br>
                • <strong>Dados verdadeiros</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info3:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #10b981;">📺 Busca Real no YouTube</h4>
                <p style="color: #64748b;">• <strong>25 vídeos</strong> encontrados<br>
                • <strong>Títulos e descrições</strong> reais<br>
                • <strong>URLs verificáveis</strong><br>
                • <strong>Dados autênticos</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 2rem;">
        <p style="color: #10b981; font-weight: 600;">© 2025 InfluScore Real - Busca Verdadeira Sem Simulação</p>
        <p style="color: #94a3b8; font-size: 0.9rem;">🔍 <strong>Busca Real</strong> • ✅ <strong>Zero Fake</strong> • 📊 <strong>Dados Verdadeiros</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

