import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from urllib.parse import quote_plus
import re

# Configuração da página
st.set_page_config(
    page_title="InfluScore - Avaliador de Influenciadores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .score-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 1rem 0;
    }
    
    .risk-very-low { color: #10b981; }
    .risk-low { color: #84cc16; }
    .risk-medium { color: #f59e0b; }
    .risk-high { color: #f97316; }
    .risk-very-high { color: #ef4444; }
    
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .source-status {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    
    .source-success { background: #dcfce7; color: #166534; }
    .source-error { background: #fef2f2; color: #991b1b; }
    
    .article-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .keyword-positive { 
        background: #dcfce7; 
        color: #166534; 
        padding: 0.25rem 0.5rem; 
        border-radius: 0.25rem; 
        margin: 0.25rem;
        display: inline-block;
    }
    
    .keyword-negative { 
        background: #fef2f2; 
        color: #991b1b; 
        padding: 0.25rem 0.5rem; 
        border-radius: 0.25rem; 
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class InfluencerAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            'sucesso', 'família', 'caridade', 'educação', 'conquista', 'prêmio', 
            'reconhecimento', 'inovação', 'inspiração', 'liderança', 'amor',
            'felicidade', 'vitória', 'crescimento', 'desenvolvimento', 'ajuda',
            'solidariedade', 'responsabilidade', 'ética', 'transparência'
        ]
        
        self.negative_keywords = [
            'roubo', 'casino', 'preso', 'escândalo', 'polêmica', 'fraude',
            'golpe', 'processo', 'condenação', 'drogas', 'violência', 'agressão',
            'corrupção', 'crime', 'prisão', 'investigação', 'acusação',
            'controversia', 'problema', 'conflito', 'briga', 'discussão'
        ]
    
    def search_google(self, query, max_results=10):
        """Simula busca no Google (em produção, usar API real)"""
        try:
            # Simulação de resultados do Google
            results = [
                {
                    'title': f'{query} - Últimas notícias e atualizações',
                    'url': f'https://example.com/news/{query.lower().replace(" ", "-")}',
                    'snippet': f'Confira as últimas notícias sobre {query}. Acompanhe todas as novidades e atualizações.',
                    'source': 'Google News'
                },
                {
                    'title': f'{query} fala sobre novos projetos',
                    'url': f'https://example.com/interview/{query.lower().replace(" ", "-")}',
                    'snippet': f'Em entrevista exclusiva, {query} comenta sobre seus próximos projetos e planos.',
                    'source': 'Portal de Notícias'
                },
                {
                    'title': f'Biografia e carreira de {query}',
                    'url': f'https://example.com/bio/{query.lower().replace(" ", "-")}',
                    'snippet': f'Conheça a trajetória de sucesso de {query} e suas principais conquistas.',
                    'source': 'Biografia'
                }
            ]
            return results[:max_results]
        except Exception as e:
            st.error(f"Erro na busca Google: {str(e)}")
            return []
    
    def search_youtube(self, query, max_results=5):
        """Simula busca no YouTube"""
        try:
            results = [
                {
                    'title': f'{query} - Vídeo mais recente',
                    'url': f'https://youtube.com/watch?v=abc123',
                    'description': f'Último vídeo publicado por {query}',
                    'views': '1.2M visualizações',
                    'source': 'YouTube'
                },
                {
                    'title': f'Entrevista com {query}',
                    'url': f'https://youtube.com/watch?v=def456',
                    'description': f'Entrevista exclusiva com {query}',
                    'views': '850K visualizações',
                    'source': 'YouTube'
                }
            ]
            return results[:max_results]
        except Exception as e:
            st.error(f"Erro na busca YouTube: {str(e)}")
            return []
    
    def search_twitter(self, query, max_results=5):
        """Simula busca no Twitter/X"""
        try:
            results = [
                {
                    'text': f'{query} compartilha momento especial com a família',
                    'url': f'https://twitter.com/user/status/123',
                    'likes': 15000,
                    'retweets': 3500,
                    'source': 'Twitter/X'
                },
                {
                    'text': f'Novo projeto de {query} promete revolucionar a educação',
                    'url': f'https://twitter.com/user/status/456',
                    'likes': 8200,
                    'retweets': 2100,
                    'source': 'Twitter/X'
                }
            ]
            return results[:max_results]
        except Exception as e:
            st.error(f"Erro na busca Twitter: {str(e)}")
            return []
    
    def analyze_sentiment(self, text):
        """Analisa sentimento do texto"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def calculate_score(self, google_results, youtube_results, twitter_results):
        """Calcula score baseado nos resultados"""
        all_texts = []
        
        # Coleta todos os textos
        for result in google_results:
            all_texts.append(result.get('title', '') + ' ' + result.get('snippet', ''))
        
        for result in youtube_results:
            all_texts.append(result.get('title', '') + ' ' + result.get('description', ''))
        
        for result in twitter_results:
            all_texts.append(result.get('text', ''))
        
        # Análise de sentimento
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        found_positive_keywords = set()
        found_negative_keywords = set()
        
        for text in all_texts:
            text_lower = text.lower()
            sentiment = self.analyze_sentiment(text)
            
            if sentiment == 'positive':
                positive_count += 1
            elif sentiment == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
            
            # Encontra palavras-chave específicas
            for keyword in self.positive_keywords:
                if keyword in text_lower:
                    found_positive_keywords.add(keyword)
            
            for keyword in self.negative_keywords:
                if keyword in text_lower:
                    found_negative_keywords.add(keyword)
        
        # Cálculo do score
        total_results = len(all_texts)
        if total_results == 0:
            return 50, 'medium', '#f59e0b', found_positive_keywords, found_negative_keywords
        
        # Score baseado em sentimento (40%)
        sentiment_score = (positive_count / total_results) * 40
        
        # Score baseado em frequência (30%)
        frequency_score = min(total_results / 20, 1) * 30
        
        # Score baseado em palavras-chave (30%)
        keyword_score = (len(found_positive_keywords) - len(found_negative_keywords)) * 5
        keyword_score = max(-15, min(15, keyword_score)) + 15  # Normaliza para 0-30
        
        final_score = sentiment_score + frequency_score + keyword_score
        final_score = max(0, min(100, final_score))
        
        # Determina nível de risco
        if final_score >= 90:
            risk_level = 'Muito Baixo'
            risk_color = '#10b981'
        elif final_score >= 70:
            risk_level = 'Baixo'
            risk_color = '#84cc16'
        elif final_score >= 50:
            risk_level = 'Médio'
            risk_color = '#f59e0b'
        elif final_score >= 30:
            risk_level = 'Alto'
            risk_color = '#f97316'
        else:
            risk_level = 'Muito Alto'
            risk_color = '#ef4444'
        
        return int(final_score), risk_level, risk_color, found_positive_keywords, found_negative_keywords

def create_score_gauge(score, risk_color):
    """Cria gráfico de gauge para o score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score de Confiança"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': risk_color},
            'steps': [
                {'range': [0, 30], 'color': "#fef2f2"},
                {'range': [30, 50], 'color': "#fef3c7"},
                {'range': [50, 70], 'color': "#fef9e3"},
                {'range': [70, 90], 'color': "#f0fdf4"},
                {'range': [90, 100], 'color': "#dcfce7"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 InfluScore</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Avalie o risco de parcerias com influenciadores</p>', unsafe_allow_html=True)
    
    # Input do usuário
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "Digite o nome do influenciador:",
            placeholder="Ex: Felipe Neto, Whindersson Nunes...",
            key="influencer_input"
        )
        
        analyze_button = st.button("🔍 Analisar Influenciador", use_container_width=True, type="primary")
    
    if analyze_button and influencer_name:
        with st.spinner(f"Analisando {influencer_name}..."):
            analyzer = InfluencerAnalyzer()
            
            # Progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Busca dados
            status_text.text("🔍 Buscando no Google...")
            google_results = analyzer.search_google(influencer_name)
            progress_bar.progress(33)
            
            status_text.text("📺 Buscando no YouTube...")
            youtube_results = analyzer.search_youtube(influencer_name)
            progress_bar.progress(66)
            
            status_text.text("🐦 Buscando no Twitter/X...")
            twitter_results = analyzer.search_twitter(influencer_name)
            progress_bar.progress(100)
            
            status_text.text("📊 Calculando score...")
            time.sleep(1)
            
            # Calcula score
            score, risk_level, risk_color, positive_keywords, negative_keywords = analyzer.calculate_score(
                google_results, youtube_results, twitter_results
            )
            
            # Remove progresso
            progress_bar.empty()
            status_text.empty()
            
            # Resultados
            st.markdown("---")
            st.markdown(f"## 📊 Análise de {influencer_name}")
            
            # Layout principal
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Score principal
                st.markdown("### 🎯 Score de Confiança")
                fig = create_score_gauge(score, risk_color)
                st.plotly_chart(fig, use_container_width=True)
                
                # Nível de risco
                risk_class = f"risk-{risk_level.lower().replace(' ', '-')}"
                st.markdown(f"""
                <div class="score-card">
                    <h3>Nível de Risco</h3>
                    <h2 class="{risk_class}">{risk_level.upper()}</h2>
                    <p>Score: {score}/100</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Estatísticas
                st.markdown("### 📈 Estatísticas")
                
                col2_1, col2_2, col2_3 = st.columns(3)
                with col2_1:
                    st.metric("Google", len(google_results), "resultados")
                with col2_2:
                    st.metric("YouTube", len(youtube_results), "vídeos")
                with col2_3:
                    st.metric("Twitter/X", len(twitter_results), "posts")
                
                # Status das fontes
                st.markdown("### 🔗 Status das Fontes")
                sources_html = f"""
                <div>
                    <span class="source-status source-success">✅ Google News</span>
                    <span class="source-status source-success">✅ YouTube</span>
                    <span class="source-status source-success">✅ Twitter/X</span>
                </div>
                """
                st.markdown(sources_html, unsafe_allow_html=True)
                
                # Recomendação
                st.markdown("### 💡 Recomendação")
                if score >= 70:
                    st.success("✅ **RECOMENDADO** para parcerias")
                elif score >= 50:
                    st.warning("⚠️ **CAUTELA** - Avaliar contexto")
                else:
                    st.error("❌ **NÃO RECOMENDADO** - Alto risco")
            
            # Análise de palavras-chave
            if positive_keywords or negative_keywords:
                st.markdown("---")
                st.markdown("### 🔍 Análise de Palavras-Chave")
                
                col3, col4 = st.columns(2)
                
                with col3:
                    st.markdown("**Palavras Positivas Encontradas:**")
                    if positive_keywords:
                        keywords_html = "".join([f'<span class="keyword-positive">{kw}</span>' for kw in positive_keywords])
                        st.markdown(keywords_html, unsafe_allow_html=True)
                    else:
                        st.info("Nenhuma palavra positiva específica encontrada")
                
                with col4:
                    st.markdown("**Palavras Negativas Encontradas:**")
                    if negative_keywords:
                        keywords_html = "".join([f'<span class="keyword-negative">{kw}</span>' for kw in negative_keywords])
                        st.markdown(keywords_html, unsafe_allow_html=True)
                    else:
                        st.success("Nenhuma palavra negativa encontrada")
            
            # Preview das matérias
            st.markdown("---")
            st.markdown("### 📰 Preview das Últimas Matérias")
            
            # Combina todos os resultados
            all_results = []
            all_results.extend([(r, 'Google') for r in google_results[:3]])
            all_results.extend([(r, 'YouTube') for r in youtube_results[:2]])
            all_results.extend([(r, 'Twitter/X') for r in twitter_results[:2]])
            
            for result, source in all_results:
                title = result.get('title', result.get('text', 'Sem título'))[:100]
                description = result.get('snippet', result.get('description', result.get('text', 'Sem descrição')))[:200]
                
                st.markdown(f"""
                <div class="article-card">
                    <h4>{title}</h4>
                    <p>{description}</p>
                    <small>📍 Fonte: {source}</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Botão para nova análise
            st.markdown("---")
            if st.button("🔄 Analisar Outro Influenciador", use_container_width=True):
                st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("Por favor, digite o nome de um influenciador para analisar.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>© 2025 InfluScore. Desenvolvido para análise de risco de influenciadores.</p>
        <p>⭐ <strong>Streamlit Version</strong> - Otimizado para deploy na nuvem</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

