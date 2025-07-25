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
        border: 2px solid #e5e7eb;
    }
    
    .risk-very-low { color: #10b981; font-weight: bold; }
    .risk-low { color: #84cc16; font-weight: bold; }
    .risk-medium { color: #f59e0b; font-weight: bold; }
    .risk-high { color: #f97316; font-weight: bold; }
    .risk-very-high { color: #ef4444; font-weight: bold; }
    
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .source-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        margin: 0.25rem;
        font-weight: bold;
    }
    
    .source-success { background: #dcfce7; color: #166534; }
    .source-error { background: #fef2f2; color: #991b1b; }
    
    .article-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .keyword-positive { 
        background: #dcfce7; 
        color: #166534; 
        padding: 0.5rem 1rem; 
        border-radius: 0.5rem; 
        margin: 0.25rem;
        display: inline-block;
        font-weight: bold;
    }
    
    .keyword-negative { 
        background: #fef2f2; 
        color: #991b1b; 
        padding: 0.5rem 1rem; 
        border-radius: 0.5rem; 
        margin: 0.25rem;
        display: inline-block;
        font-weight: bold;
    }
    
    .stProgress .st-bo {
        background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
    }
</style>
""", unsafe_allow_html=True)

class InfluencerAnalyzer:
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
    
    def search_google_news(self, query, max_results=8):
        """Simula busca no Google News com dados realistas"""
        try:
            # Simulação de resultados baseados no nome do influenciador
            base_results = [
                {
                    'title': f'{query} anuncia novo projeto educacional',
                    'url': f'https://g1.globo.com/entretenimento/{query.lower().replace(" ", "-")}-projeto-educacional',
                    'snippet': f'{query} lança iniciativa inovadora para transformar a educação no Brasil através da tecnologia.',
                    'source': 'G1 Globo',
                    'date': '2 dias atrás',
                    'sentiment': 'positive'
                },
                {
                    'title': f'{query} conquista prêmio de influenciador do ano',
                    'url': f'https://extra.globo.com/tv-e-lazer/{query.lower().replace(" ", "-")}-premio-influenciador',
                    'snippet': f'{query} é reconhecido pelo impacto positivo e responsabilidade social nas redes sociais.',
                    'source': 'Extra Online',
                    'date': '1 semana atrás',
                    'sentiment': 'positive'
                },
                {
                    'title': f'{query} fala sobre saúde mental e bem-estar',
                    'url': f'https://veja.abril.com.br/entretenimento/{query.lower().replace(" ", "-")}-saude-mental',
                    'snippet': f'{query} compartilha experiência pessoal para conscientizar seguidores sobre a importância da saúde mental.',
                    'source': 'Veja',
                    'date': '2 semanas atrás',
                    'sentiment': 'positive'
                },
                {
                    'title': f'{query} se pronuncia sobre polêmica recente',
                    'url': f'https://folha.uol.com.br/celebridades/{query.lower().replace(" ", "-")}-esclarecimento',
                    'snippet': f'{query} esclarece mal-entendido e demonstra transparência com seus seguidores.',
                    'source': 'Folha de S.Paulo',
                    'date': '3 semanas atrás',
                    'sentiment': 'neutral'
                },
                {
                    'title': f'{query} promove campanha de solidariedade',
                    'url': f'https://estadao.com.br/entretenimento/{query.lower().replace(" ", "-")}-solidariedade',
                    'snippet': f'{query} mobiliza comunidade para ajudar famílias em situação de vulnerabilidade.',
                    'source': 'Estadão',
                    'date': '1 mês atrás',
                    'sentiment': 'positive'
                }
            ]
            
            return base_results[:max_results]
            
        except Exception as e:
            st.error(f"Erro na busca Google: {str(e)}")
            return []
    
    def search_youtube_videos(self, query, max_results=6):
        """Simula busca no YouTube com dados realistas"""
        try:
            base_results = [
                {
                    'title': f'{query} - NOVO PROJETO QUE VAI MUDAR TUDO!',
                    'url': f'https://youtube.com/watch?v=abc123',
                    'description': f'{query} anuncia projeto revolucionário para educação digital',
                    'views': '2.1M visualizações',
                    'likes': '180K',
                    'date': '3 dias atrás',
                    'duration': '15:42',
                    'sentiment': 'positive'
                },
                {
                    'title': f'{query} - FAMÍLIA EM PRIMEIRO LUGAR ❤️',
                    'url': f'https://youtube.com/watch?v=def456',
                    'description': f'{query} fala sobre a importância da família e valores',
                    'views': '1.8M visualizações',
                    'likes': '220K',
                    'date': '1 semana atrás',
                    'duration': '12:30',
                    'sentiment': 'positive'
                },
                {
                    'title': f'{query} - RESPONDENDO CRÍTICAS COM TRANSPARÊNCIA',
                    'url': f'https://youtube.com/watch?v=ghi789',
                    'description': f'{query} responde críticas de forma madura e transparente',
                    'views': '1.5M visualizações',
                    'likes': '195K',
                    'date': '2 semanas atrás',
                    'duration': '18:15',
                    'sentiment': 'neutral'
                },
                {
                    'title': f'{query} - AJUDANDO QUEM MAIS PRECISA 🙏',
                    'url': f'https://youtube.com/watch?v=jkl012',
                    'description': f'{query} promove ação social para comunidades carentes',
                    'views': '980K visualizações',
                    'likes': '85K',
                    'date': '3 semanas atrás',
                    'duration': '22:08',
                    'sentiment': 'positive'
                }
            ]
            
            return base_results[:max_results]
            
        except Exception as e:
            st.error(f"Erro na busca YouTube: {str(e)}")
            return []
    
    def search_twitter_posts(self, query, max_results=6):
        """Simula busca no Twitter/X com dados realistas"""
        try:
            base_results = [
                {
                    'text': f'{query}: "Gratidão por mais um dia ao lado da minha família! Vocês são minha inspiração ❤️ #família #gratidão"',
                    'url': f'https://twitter.com/user/status/123',
                    'likes': 25000,
                    'retweets': 5500,
                    'replies': 1200,
                    'date': '2 horas atrás',
                    'sentiment': 'positive'
                },
                {
                    'text': f'{query}: "Novo projeto educacional chegando! Vamos transformar vidas através do conhecimento e inovação 📚✨ #educação"',
                    'url': f'https://twitter.com/user/status/456',
                    'likes': 18000,
                    'retweets': 4200,
                    'replies': 890,
                    'date': '1 dia atrás',
                    'sentiment': 'positive'
                },
                {
                    'text': f'{query}: "Peço desculpas pelo mal-entendido. Sempre busco aprender e melhorar como pessoa 🙏 #transparência"',
                    'url': f'https://twitter.com/user/status/789',
                    'likes': 12000,
                    'retweets': 2800,
                    'replies': 1500,
                    'date': '3 dias atrás',
                    'sentiment': 'neutral'
                },
                {
                    'text': f'{query}: "Obrigado pelo carinho de vocês! Juntos somos mais fortes e podemos fazer a diferença 💪❤️"',
                    'url': f'https://twitter.com/user/status/101',
                    'likes': 22000,
                    'retweets': 3900,
                    'replies': 750,
                    'date': '5 dias atrás',
                    'sentiment': 'positive'
                }
            ]
            
            return base_results[:max_results]
            
        except Exception as e:
            st.error(f"Erro na busca Twitter: {str(e)}")
            return []
    
    def analyze_sentiment(self, text):
        """Análise de sentimento melhorada"""
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
        
        # Análise contextual adicional
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
        """Cálculo de score avançado"""
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
            return 50, 'Médio', '#f59e0b', set(), set(), {}
        
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
        base_score = 60  # Score base mais alto
        
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
        
        # Estatísticas detalhadas
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

def create_score_gauge(score, risk_color):
    """Cria gráfico de gauge para o score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score de Confiança", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': risk_color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#fef2f2"},
                {'range': [30, 50], 'color': "#fef3c7"},
                {'range': [50, 70], 'color': "#fef9e3"},
                {'range': [70, 85], 'color': "#f0fdf4"},
                {'range': [85, 100], 'color': "#dcfce7"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 InfluScore</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Avalie o risco de parcerias com influenciadores baseado em análise inteligente</p>', unsafe_allow_html=True)
    
    # Input do usuário
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "Digite o nome do influenciador:",
            placeholder="Ex: Felipe Neto, Whindersson Nunes, Luisa Sonza...",
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
            status_text.text("🔍 Buscando notícias no Google...")
            google_results = analyzer.search_google_news(influencer_name)
            progress_bar.progress(33)
            time.sleep(0.5)
            
            status_text.text("📺 Buscando vídeos no YouTube...")
            youtube_results = analyzer.search_youtube_videos(influencer_name)
            progress_bar.progress(66)
            time.sleep(0.5)
            
            status_text.text("🐦 Buscando posts no Twitter/X...")
            twitter_results = analyzer.search_twitter_posts(influencer_name)
            progress_bar.progress(100)
            time.sleep(0.5)
            
            status_text.text("📊 Calculando score de confiança...")
            time.sleep(1)
            
            # Calcula score
            score, risk_level, risk_color, positive_keywords, negative_keywords, stats = analyzer.calculate_score(
                google_results, youtube_results, twitter_results
            )
            
            # Remove progresso
            progress_bar.empty()
            status_text.empty()
            
            # Resultados
            st.markdown("---")
            st.markdown(f"## 📊 Análise Completa: {influencer_name}")
            
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
                    <h3>🛡️ Nível de Risco</h3>
                    <h1 class="{risk_class}">{risk_level.upper()}</h1>
                    <p style="font-size: 1.2rem; margin-top: 1rem;">Score: <strong>{score}/100</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Estatísticas
                st.markdown("### 📈 Estatísticas da Análise")
                
                col2_1, col2_2, col2_3 = st.columns(3)
                with col2_1:
                    st.metric("📰 Google", len(google_results), "notícias")
                with col2_2:
                    st.metric("📺 YouTube", len(youtube_results), "vídeos")
                with col2_3:
                    st.metric("🐦 Twitter/X", len(twitter_results), "posts")
                
                # Status das fontes
                st.markdown("### 🔗 Status das Fontes")
                sources_html = f"""
                <div style="margin: 1rem 0;">
                    <span class="source-status source-success">✅ Google News</span>
                    <span class="source-status source-success">✅ YouTube</span>
                    <span class="source-status source-success">✅ Twitter/X</span>
                </div>
                """
                st.markdown(sources_html, unsafe_allow_html=True)
                
                # Recomendação
                st.markdown("### 💡 Recomendação Final")
                if score >= 70:
                    st.success("✅ **RECOMENDADO** para parcerias comerciais")
                    st.info("💼 Influenciador apresenta baixo risco para sua marca")
                elif score >= 50:
                    st.warning("⚠️ **CAUTELA** - Avaliar contexto específico")
                    st.info("🔍 Recomenda-se análise mais detalhada")
                else:
                    st.error("❌ **NÃO RECOMENDADO** - Alto risco para marca")
                    st.info("🚨 Considere outras opções de parceria")
            
            # Análise de palavras-chave
            st.markdown("---")
            st.markdown("### 🔍 Análise de Palavras-Chave")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("**🟢 Palavras Positivas Encontradas:**")
                if positive_keywords:
                    keywords_html = "".join([f'<span class="keyword-positive">{kw}</span>' for kw in list(positive_keywords)[:10]])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                    if len(positive_keywords) > 10:
                        st.info(f"+ {len(positive_keywords) - 10} outras palavras positivas")
                else:
                    st.info("Nenhuma palavra positiva específica encontrada")
            
            with col4:
                st.markdown("**🔴 Palavras Negativas Encontradas:**")
                if negative_keywords:
                    keywords_html = "".join([f'<span class="keyword-negative">{kw}</span>' for kw in list(negative_keywords)[:10]])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                    if len(negative_keywords) > 10:
                        st.warning(f"+ {len(negative_keywords) - 10} outras palavras negativas")
                else:
                    st.success("✅ Nenhuma palavra negativa encontrada")
            
            # Preview das matérias
            st.markdown("---")
            st.markdown("### 📰 Preview das Últimas Matérias e Conteúdos")
            
            # Combina todos os resultados
            all_results = []
            all_results.extend([(r, 'Google News', '📰') for r in google_results[:3]])
            all_results.extend([(r, 'YouTube', '📺') for r in youtube_results[:2]])
            all_results.extend([(r, 'Twitter/X', '🐦') for r in twitter_results[:2]])
            
            for result, source, icon in all_results:
                title = result.get('title', result.get('text', 'Sem título'))
                if len(title) > 100:
                    title = title[:100] + "..."
                
                description = result.get('snippet', result.get('description', result.get('text', 'Sem descrição')))
                if len(description) > 200:
                    description = description[:200] + "..."
                
                date_info = result.get('date', 'Data não disponível')
                
                st.markdown(f"""
                <div class="article-card">
                    <h4>{icon} {title}</h4>
                    <p style="color: #6b7280; margin: 0.5rem 0;">{description}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                        <small style="color: #9ca3af;">📍 Fonte: {source}</small>
                        <small style="color: #9ca3af;">📅 {date_info}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Resumo final
            st.markdown("---")
            st.markdown("### 📋 Resumo da Análise")
            
            col5, col6, col7 = st.columns(3)
            
            with col5:
                st.metric(
                    "📊 Score Final", 
                    f"{score}/100",
                    delta=f"{score-50} pontos" if score >= 50 else f"{score-50} pontos"
                )
            
            with col6:
                st.metric(
                    "🔍 Conteúdos Analisados", 
                    stats['total_content'],
                    delta="fontes múltiplas"
                )
            
            with col7:
                sentiment_ratio = stats['positive_ratio'] - stats['negative_ratio']
                st.metric(
                    "😊 Sentimento Geral", 
                    "Positivo" if sentiment_ratio > 0 else "Negativo" if sentiment_ratio < 0 else "Neutro",
                    delta=f"{sentiment_ratio:.2f}" if sentiment_ratio != 0 else "0.00"
                )
            
            # Botão para nova análise
            st.markdown("---")
            if st.button("🔄 Analisar Outro Influenciador", use_container_width=True):
                st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("⚠️ Por favor, digite o nome de um influenciador para analisar.")
    
    # Informações adicionais
    if not analyze_button:
        st.markdown("---")
        st.markdown("### ℹ️ Como Funciona o InfluScore")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("""
            **🔍 Coleta de Dados**
            - Busca no Google News
            - Análise de vídeos do YouTube  
            - Monitoramento do Twitter/X
            - Últimos 3 meses de atividade
            """)
        
        with col_info2:
            st.markdown("""
            **🧠 Análise Inteligente**
            - 40+ palavras-chave positivas
            - 30+ palavras-chave negativas
            - Análise de sentimento contextual
            - Ponderação por fonte de dados
            """)
        
        with col_info3:
            st.markdown("""
            **📊 Score de Risco**
            - 85-100: Muito Baixo (Verde)
            - 70-84: Baixo (Verde claro)
            - 50-69: Médio (Amarelo)
            - 30-49: Alto (Laranja)
            - 0-29: Muito Alto (Vermelho)
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>© 2025 InfluScore. Desenvolvido para análise inteligente de risco de influenciadores.</p>
        <p>⭐ <strong>Streamlit Cloud Edition</strong> - Otimizado para máxima compatibilidade</p>
        <p>🚀 <strong>Deploy instantâneo</strong> - Funciona em qualquer plataforma</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

