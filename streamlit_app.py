import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
from urllib.parse import quote_plus
import re

# Configuração da página
st.set_page_config(
    page_title="InfluScore - Avaliador de Influenciadores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS moderno com fundo branco e gradiente roxo-azul
st.markdown("""
<style>
    /* Reset e base */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Fundo branco limpo */
    .stApp {
        background: #ffffff;
    }
    
    /* Header com gradiente roxo-azul */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.25rem;
        margin-bottom: 3rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    /* Input moderno */
    .stTextInput > div > div > input {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Botão moderno */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Cards modernos */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .score-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Níveis de risco com cores modernas */
    .risk-very-low { 
        color: #059669; 
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(5, 150, 105, 0.1);
    }
    .risk-low { 
        color: #65a30d; 
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(101, 163, 13, 0.1);
    }
    .risk-medium { 
        color: #d97706; 
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(217, 119, 6, 0.1);
    }
    .risk-high { 
        color: #dc2626; 
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(220, 38, 38, 0.1);
    }
    .risk-very-high { 
        color: #991b1b; 
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(153, 27, 27, 0.1);
    }
    
    /* Status das fontes */
    .source-status {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }
    
    .source-success { 
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    
    .source-loading { 
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    /* Cards de artigos */
    .article-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .article-card:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Keywords com gradiente */
    .keyword-positive { 
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        margin: 0.25rem;
        display: inline-block;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #a7f3d0;
    }
    
    .keyword-negative { 
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        margin: 0.25rem;
        display: inline-block;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fecaca;
    }
    
    /* Progress bar com gradiente */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Métricas modernas */
    .stMetric {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Seções com títulos modernos */
    h3 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Alertas modernos */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Spinner customizado */
    .stSpinner {
        color: #667eea;
    }
    
    /* Dividers sutis */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

class RealInfluencerAnalyzer:
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
            'verdade', 'sinceridade', 'autenticidade', 'integridade'
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
            'intolerância', 'machismo', 'homofobia', 'xenofobia'
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_google_real(self, query, max_results=10):
        """Busca real no Google"""
        try:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Busca resultados orgânicos
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:max_results]:
                try:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        url = link_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        if url.startswith('/url?q='):
                            url = url.split('/url?q=')[1].split('&')[0]
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'Google Search'
                        })
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            st.error(f"Erro na busca Google: {str(e)}")
            return []
    
    def search_youtube_real(self, query, max_results=8):
        """Busca real no YouTube"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Extrai dados do JavaScript
            content = response.text
            results = []
            
            # Busca por padrões de vídeos no HTML
            video_pattern = r'"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"}.*?"viewCountText":{"simpleText":"([^"]+)"}'
            matches = re.findall(video_pattern, content)
            
            for match in matches[:max_results]:
                video_id, title, views = match
                results.append({
                    'title': title,
                    'url': f'https://youtube.com/watch?v={video_id}',
                    'description': f'Vídeo do YouTube sobre {query}',
                    'views': views,
                    'source': 'YouTube'
                })
            
            # Se não encontrou pelo regex, usa busca alternativa
            if not results:
                soup = BeautifulSoup(content, 'html.parser')
                scripts = soup.find_all('script')
                
                for script in scripts:
                    if 'ytInitialData' in script.text:
                        # Extrai títulos básicos
                        titles = re.findall(r'"title":"([^"]+)"', script.text)
                        for i, title in enumerate(titles[:max_results]):
                            if query.lower() in title.lower():
                                results.append({
                                    'title': title,
                                    'url': f'https://youtube.com/results?search_query={quote_plus(title)}',
                                    'description': f'Conteúdo relacionado a {query}',
                                    'views': 'N/A',
                                    'source': 'YouTube'
                                })
                        break
            
            return results
            
        except Exception as e:
            st.error(f"Erro na busca YouTube: {str(e)}")
            return []
    
    def search_twitter_real(self, query, max_results=8):
        """Busca real no Twitter/X (método alternativo)"""
        try:
            # Busca no Google por tweets
            search_query = f"site:twitter.com {query}"
            search_url = f"https://www.google.com/search?q={quote_plus(search_query)}&num={max_results}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:max_results]:
                try:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                    
                    if title_elem and link_elem and 'twitter.com' in str(link_elem):
                        title = title_elem.get_text(strip=True)
                        url = link_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        if url.startswith('/url?q='):
                            url = url.split('/url?q=')[1].split('&')[0]
                        
                        results.append({
                            'text': title + ' ' + snippet,
                            'url': url,
                            'source': 'Twitter/X'
                        })
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            st.error(f"Erro na busca Twitter: {str(e)}")
            return []
    
    def analyze_sentiment(self, text):
        """Análise de sentimento avançada"""
        if not text:
            return 'neutral', 0, []
        
        text_lower = text.lower()
        
        found_positive = []
        found_negative = []
        
        for keyword in self.positive_keywords:
            if keyword in text_lower:
                found_positive.append(keyword)
        
        for keyword in self.negative_keywords:
            if keyword in text_lower:
                found_negative.append(keyword)
        
        # Análise contextual
        positive_patterns = [
            r'\b(muito bom|excelente|fantástico|incrível|maravilhoso|ótimo)\b',
            r'\b(amo|adoro|gosto muito|curto|apoio)\b',
            r'\b(parabéns|congratulações|felicitações|sucesso)\b',
            r'\b(orgulho|feliz|alegre|contente|satisfeito)\b'
        ]
        
        negative_patterns = [
            r'\b(muito ruim|péssimo|horrível|terrível|decepcionante)\b',
            r'\b(odeio|detesto|não suporto|repudio)\b',
            r'\b(fracasso|derrota|falha|erro|problema)\b',
            r'\b(triste|chateado|irritado|revoltado)\b'
        ]
        
        for pattern in positive_patterns:
            if re.search(pattern, text_lower):
                found_positive.append('contexto_positivo')
        
        for pattern in negative_patterns:
            if re.search(pattern, text_lower):
                found_negative.append('contexto_negativo')
        
        positive_score = len(found_positive) * 2
        negative_score = len(found_negative) * 3
        
        if positive_score > negative_score:
            sentiment = 'positive'
            confidence = min((positive_score - negative_score) / 10, 1.0)
        elif negative_score > positive_score:
            sentiment = 'negative'
            confidence = min((negative_score - positive_score) / 10, 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return sentiment, confidence, found_positive + found_negative
    
    def calculate_score(self, google_results, youtube_results, twitter_results):
        """Cálculo de score baseado em dados reais"""
        all_content = []
        source_weights = {'google': 0.4, 'youtube': 0.35, 'twitter': 0.25}
        
        # Processa resultados do Google
        for result in google_results:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            sentiment, confidence, keywords = self.analyze_sentiment(content)
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'source': 'google',
                'weight': source_weights['google']
            })
        
        # Processa resultados do YouTube
        for result in youtube_results:
            content = f"{result.get('title', '')} {result.get('description', '')}"
            sentiment, confidence, keywords = self.analyze_sentiment(content)
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'source': 'youtube',
                'weight': source_weights['youtube']
            })
        
        # Processa resultados do Twitter
        for result in twitter_results:
            content = result.get('text', '')
            sentiment, confidence, keywords = self.analyze_sentiment(content)
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'source': 'twitter',
                'weight': source_weights['twitter']
            })
        
        if not all_content:
            return 50, 'Médio', '#d97706', set(), set(), {}
        
        # Calcula scores ponderados
        weighted_positive = 0
        weighted_negative = 0
        total_weight = 0
        
        all_positive_keywords = set()
        all_negative_keywords = set()
        
        for item in all_content:
            weight = item['weight']
            confidence = item['confidence']
            
            if item['sentiment'] == 'positive':
                weighted_positive += weight * confidence
            elif item['sentiment'] == 'negative':
                weighted_negative += weight * confidence
            
            total_weight += weight
            
            # Coleta palavras-chave
            for keyword in item['keywords']:
                if keyword in self.positive_keywords:
                    all_positive_keywords.add(keyword)
                elif keyword in self.negative_keywords:
                    all_negative_keywords.add(keyword)
        
        # Normaliza scores
        if total_weight > 0:
            weighted_positive /= total_weight
            weighted_negative /= total_weight
        
        # Calcula score final (0-100)
        base_score = 60
        
        # Ajusta baseado no sentimento
        sentiment_adjustment = (weighted_positive - weighted_negative) * 25
        
        # Ajusta baseado na quantidade de conteúdo
        content_bonus = min(len(all_content) / 15, 1) * 10
        
        # Ajusta baseado nas palavras-chave
        keyword_adjustment = (len(all_positive_keywords) - len(all_negative_keywords) * 1.5) * 3
        
        final_score = base_score + sentiment_adjustment + content_bonus + keyword_adjustment
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
        
        # Estatísticas
        stats = {
            'total_content': len(all_content),
            'positive_ratio': weighted_positive,
            'negative_ratio': weighted_negative,
            'google_count': len(google_results),
            'youtube_count': len(youtube_results),
            'twitter_count': len(twitter_results),
            'positive_keywords_count': len(all_positive_keywords),
            'negative_keywords_count': len(all_negative_keywords)
        }
        
        return int(final_score), risk_level, risk_color, all_positive_keywords, all_negative_keywords, stats

def create_modern_gauge(score, risk_color):
    """Cria gauge moderno com gradiente roxo-azul"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score de Confiança", 'font': {'size': 24, 'color': '#1e293b', 'family': 'Inter'}},
        number = {'font': {'size': 48, 'color': risk_color, 'family': 'Inter'}},
        gauge = {
            'axis': {
                'range': [None, 100], 
                'tickwidth': 2, 
                'tickcolor': "#cbd5e1",
                'tickfont': {'size': 14, 'color': '#64748b'}
            },
            'bar': {'color': risk_color, 'thickness': 0.4},
            'bgcolor': "#f8fafc",
            'borderwidth': 3,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 30], 'color': "#fee2e2"},
                {'range': [30, 50], 'color': "#fed7aa"},
                {'range': [50, 70], 'color': "#fef3c7"},
                {'range': [70, 85], 'color': "#d1fae5"},
                {'range': [85, 100], 'color': "#a7f3d0"}
            ],
            'threshold': {
                'line': {'color': "#667eea", 'width': 4},
                'thickness': 0.8,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#1e293b", 'family': "Inter"}
    )
    
    return fig

def main():
    # Header moderno
    st.markdown('<h1 class="main-header">📊 InfluScore</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análise inteligente de influenciadores com dados reais</p>', unsafe_allow_html=True)
    
    # Input elegante
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "",
            placeholder="Digite o nome do influenciador (ex: Felipe Neto, Whindersson Nunes...)",
            key="influencer_input",
            label_visibility="collapsed"
        )
        
        analyze_button = st.button("🔍 Analisar Influenciador", use_container_width=True, type="primary")
    
    if analyze_button and influencer_name:
        with st.spinner(f"Coletando dados reais sobre {influencer_name}..."):
            analyzer = RealInfluencerAnalyzer()
            
            # Container para status
            status_container = st.container()
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
            
            with status_container:
                status_col1, status_col2, status_col3 = st.columns(3)
                
                with status_col1:
                    google_status = st.empty()
                    google_status.markdown('<span class="source-status source-loading">🔍 Buscando no Google...</span>', unsafe_allow_html=True)
                
                with status_col2:
                    youtube_status = st.empty()
                    youtube_status.markdown('<span class="source-status source-loading">📺 Aguardando...</span>', unsafe_allow_html=True)
                
                with status_col3:
                    twitter_status = st.empty()
                    twitter_status.markdown('<span class="source-status source-loading">🐦 Aguardando...</span>', unsafe_allow_html=True)
            
            # Busca no Google
            google_results = analyzer.search_google_real(influencer_name)
            google_status.markdown('<span class="source-status source-success">✅ Google Concluído</span>', unsafe_allow_html=True)
            progress_bar.progress(33)
            time.sleep(0.5)
            
            # Busca no YouTube
            youtube_status.markdown('<span class="source-status source-loading">📺 Buscando no YouTube...</span>', unsafe_allow_html=True)
            youtube_results = analyzer.search_youtube_real(influencer_name)
            youtube_status.markdown('<span class="source-status source-success">✅ YouTube Concluído</span>', unsafe_allow_html=True)
            progress_bar.progress(66)
            time.sleep(0.5)
            
            # Busca no Twitter
            twitter_status.markdown('<span class="source-status source-loading">🐦 Buscando no Twitter/X...</span>', unsafe_allow_html=True)
            twitter_results = analyzer.search_twitter_real(influencer_name)
            twitter_status.markdown('<span class="source-status source-success">✅ Twitter/X Concluído</span>', unsafe_allow_html=True)
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Calcula score
            score, risk_level, risk_color, positive_keywords, negative_keywords, stats = analyzer.calculate_score(
                google_results, youtube_results, twitter_results
            )
            
            # Remove containers de progresso
            progress_container.empty()
            status_container.empty()
            
            # Resultados modernos
            st.markdown("---")
            st.markdown(f"## 📊 Análise de {influencer_name}")
            
            # Layout principal
            col1, col2 = st.columns([1.2, 0.8])
            
            with col1:
                # Score principal
                fig = create_modern_gauge(score, risk_color)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Card de risco
                risk_class = f"risk-{risk_level.lower().replace(' ', '-')}"
                st.markdown(f"""
                <div class="score-card">
                    <h3 style="margin-bottom: 1rem; color: #1e293b;">🛡️ Nível de Risco</h3>
                    <h1 class="{risk_class}" style="font-size: 2.5rem; margin: 1rem 0;">{risk_level.upper()}</h1>
                    <p style="font-size: 1.3rem; color: #64748b; margin: 0;">Score: <strong>{score}/100</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Recomendação
                if score >= 70:
                    st.success("✅ **RECOMENDADO** para parcerias")
                elif score >= 50:
                    st.warning("⚠️ **CAUTELA** - Avaliar contexto")
                else:
                    st.error("❌ **NÃO RECOMENDADO** - Alto risco")
            
            # Estatísticas
            st.markdown("### 📈 Dados Coletados")
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            
            with col_stats1:
                st.metric("🔍 Google", len(google_results), "resultados")
            with col_stats2:
                st.metric("📺 YouTube", len(youtube_results), "vídeos")
            with col_stats3:
                st.metric("🐦 Twitter/X", len(twitter_results), "posts")
            with col_stats4:
                st.metric("📊 Total", stats['total_content'], "conteúdos")
            
            # Análise de palavras-chave
            if positive_keywords or negative_keywords:
                st.markdown("---")
                st.markdown("### 🔍 Palavras-Chave Encontradas")
                
                col_kw1, col_kw2 = st.columns(2)
                
                with col_kw1:
                    st.markdown("**🟢 Palavras Positivas:**")
                    if positive_keywords:
                        keywords_html = "".join([f'<span class="keyword-positive">{kw}</span>' for kw in list(positive_keywords)[:8]])
                        st.markdown(keywords_html, unsafe_allow_html=True)
                        if len(positive_keywords) > 8:
                            st.info(f"+ {len(positive_keywords) - 8} outras")
                    else:
                        st.info("Nenhuma palavra positiva encontrada")
                
                with col_kw2:
                    st.markdown("**🔴 Palavras Negativas:**")
                    if negative_keywords:
                        keywords_html = "".join([f'<span class="keyword-negative">{kw}</span>' for kw in list(negative_keywords)[:8]])
                        st.markdown(keywords_html, unsafe_allow_html=True)
                        if len(negative_keywords) > 8:
                            st.warning(f"+ {len(negative_keywords) - 8} outras")
                    else:
                        st.success("✅ Nenhuma palavra negativa encontrada")
            
            # Preview dos resultados reais
            st.markdown("---")
            st.markdown("### 📰 Conteúdos Encontrados")
            
            # Combina resultados reais
            all_results = []
            all_results.extend([(r, 'Google', '🔍') for r in google_results[:3]])
            all_results.extend([(r, 'YouTube', '📺') for r in youtube_results[:2]])
            all_results.extend([(r, 'Twitter/X', '🐦') for r in twitter_results[:2]])
            
            if all_results:
                for result, source, icon in all_results:
                    title = result.get('title', result.get('text', 'Sem título'))
                    if len(title) > 120:
                        title = title[:120] + "..."
                    
                    description = result.get('snippet', result.get('description', result.get('text', 'Sem descrição')))
                    if len(description) > 250:
                        description = description[:250] + "..."
                    
                    url = result.get('url', '#')
                    
                    st.markdown(f"""
                    <div class="article-card">
                        <h4 style="margin-bottom: 0.5rem; color: #1e293b;">{icon} {title}</h4>
                        <p style="color: #64748b; margin: 0.5rem 0; line-height: 1.5;">{description}</p>
                        <div style="margin-top: 1rem;">
                            <small style="color: #9ca3af;">📍 Fonte: {source}</small>
                            {f'<small style="color: #9ca3af; margin-left: 1rem;">🔗 <a href="{url}" target="_blank" style="color: #667eea;">Ver original</a></small>' if url != '#' else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum conteúdo específico encontrado. Tente um nome mais conhecido.")
            
            # Botão para nova análise
            st.markdown("---")
            if st.button("🔄 Analisar Outro Influenciador", use_container_width=True):
                st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("⚠️ Por favor, digite o nome de um influenciador para analisar.")
    
    # Informações sobre o sistema
    if not analyze_button:
        st.markdown("---")
        st.markdown("### ℹ️ Como Funciona")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("""
            <div class="metric-card">
                <h4>🔍 Coleta Real de Dados</h4>
                <p>• Busca no Google Search<br>
                • Análise de vídeos do YouTube<br>
                • Monitoramento do Twitter/X<br>
                • Dados 100% reais e atualizados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info2:
            st.markdown("""
            <div class="metric-card">
                <h4>🧠 Análise Inteligente</h4>
                <p>• 40+ palavras-chave positivas<br>
                • 30+ palavras-chave negativas<br>
                • Análise de sentimento contextual<br>
                • Ponderação por fonte de dados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info3:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Score de Risco</h4>
                <p>• 85-100: Muito Baixo (Verde)<br>
                • 70-84: Baixo (Verde claro)<br>
                • 50-69: Médio (Amarelo)<br>
                • 30-49: Alto (Laranja)<br>
                • 0-29: Muito Alto (Vermelho)</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer elegante
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 2rem; font-family: 'Inter', sans-serif;">
        <p style="margin-bottom: 0.5rem;">© 2025 InfluScore - Análise inteligente de influenciadores</p>
        <p style="margin: 0; font-size: 0.9rem;">🚀 <strong>Dados reais</strong> • 🎨 <strong>Design moderno</strong> • ⚡ <strong>Análise instantânea</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

