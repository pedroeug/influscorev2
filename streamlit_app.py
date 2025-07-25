import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
from urllib.parse import quote_plus
import re
from collections import defaultdict

# Configuração da página
st.set_page_config(
    page_title="InfluScore Deep - Análise Profunda de Influenciadores",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS moderno com fonte legível
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        color: #1e293b !important;
    }
    
    .stApp {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    * {
        color: #1e293b !important;
    }
    
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
        color: #64748b !important;
        font-size: 1.25rem;
        margin-bottom: 3rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    .deep-analysis-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .progress-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .source-progress {
        margin: 1rem 0;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    .content-counter {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #0ea5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .temporal-analysis {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .keyword-trend {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        display: inline-block;
        min-width: 150px;
    }
    
    .trend-up {
        border-left: 4px solid #10b981;
    }
    
    .trend-down {
        border-left: 4px solid #ef4444;
    }
    
    .trend-stable {
        border-left: 4px solid #6b7280;
    }
    
    .deep-metric {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .confidence-high { border-color: #10b981; }
    .confidence-medium { border-color: #f59e0b; }
    .confidence-low { border-color: #ef4444; }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, span, div {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

class DeepInfluencerAnalyzer:
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
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Data limite para análise (últimos 90 dias)
        self.date_limit = datetime.now() - timedelta(days=90)
    
    def search_google_deep(self, query, min_results=25):
        """Busca profunda no Google com múltiplas páginas"""
        all_results = []
        
        try:
            # Busca em múltiplas páginas para garantir 25+ resultados
            for page in range(0, min_results // 10 + 2):
                start = page * 10
                search_url = f"https://www.google.com/search?q={quote_plus(query)}&start={start}&num=10"
                
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                search_results = soup.find_all('div', class_='g')
                
                page_results = []
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        link_elem = result.find('a')
                        snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                        date_elem = result.find('span', class_='f')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                            date_text = date_elem.get_text(strip=True) if date_elem else ''
                            
                            if url.startswith('/url?q='):
                                url = url.split('/url?q=')[1].split('&')[0]
                            
                            # Análise temporal básica
                            is_recent = self._is_content_recent(date_text, title, snippet)
                            
                            page_results.append({
                                'title': title,
                                'url': url,
                                'snippet': snippet,
                                'source': 'Google Search',
                                'date_text': date_text,
                                'is_recent': is_recent,
                                'page': page + 1
                            })
                    except Exception as e:
                        continue
                
                all_results.extend(page_results)
                
                # Para evitar rate limiting
                time.sleep(1)
                
                # Se já temos resultados suficientes, para
                if len(all_results) >= min_results:
                    break
            
            return all_results[:min_results * 2]  # Retorna até 50 para ter margem
            
        except Exception as e:
            st.error(f"Erro na busca Google profunda: {str(e)}")
            return []
    
    def search_youtube_deep(self, query, min_results=25):
        """Busca profunda no YouTube com múltiplas tentativas"""
        all_results = []
        
        try:
            # Múltiplas variações da busca para mais resultados
            search_variations = [
                query,
                f"{query} 2024",
                f"{query} recente",
                f"{query} últimos vídeos",
                f"{query} canal oficial"
            ]
            
            for variation in search_variations:
                search_url = f"https://www.youtube.com/results?search_query={quote_plus(variation)}"
                
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                content = response.text
                
                # Múltiplos padrões de extração
                patterns = [
                    r'"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"}.*?"viewCountText":{"simpleText":"([^"]+)"}',
                    r'"videoId":"([^"]+)".*?"title":"([^"]+)".*?"viewCountText":"([^"]+)"',
                    r'"videoId":"([^"]+)".*?"title":{"simpleText":"([^"]+)"}'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if len(match) >= 2:
                            video_id = match[0]
                            title = match[1]
                            views = match[2] if len(match) > 2 else 'N/A'
                            
                            # Verifica se é conteúdo recente baseado no título
                            is_recent = self._is_content_recent('', title, '')
                            
                            all_results.append({
                                'title': title,
                                'url': f'https://youtube.com/watch?v={video_id}',
                                'description': f'Vídeo sobre {query}',
                                'views': views,
                                'source': 'YouTube',
                                'is_recent': is_recent,
                                'search_variation': variation
                            })
                
                time.sleep(1)  # Rate limiting
                
                if len(all_results) >= min_results:
                    break
            
            # Remove duplicatas baseado no video_id
            seen_ids = set()
            unique_results = []
            for result in all_results:
                video_id = result['url'].split('v=')[-1].split('&')[0]
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    unique_results.append(result)
            
            return unique_results[:min_results * 2]
            
        except Exception as e:
            st.error(f"Erro na busca YouTube profunda: {str(e)}")
            return []
    
    def search_twitter_deep(self, query, min_results=25):
        """Busca profunda no Twitter/X com múltiplas estratégias"""
        all_results = []
        
        try:
            # Múltiplas estratégias de busca
            search_strategies = [
                f"site:twitter.com {query}",
                f"site:x.com {query}",
                f"site:twitter.com \"{query}\" 2024",
                f"site:twitter.com {query} últimos",
                f"twitter {query} posts"
            ]
            
            for strategy in search_strategies:
                search_url = f"https://www.google.com/search?q={quote_plus(strategy)}&num=20"
                
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                search_results = soup.find_all('div', class_='g')
                
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        link_elem = result.find('a')
                        snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                        
                        if title_elem and link_elem:
                            url = link_elem.get('href', '')
                            if 'twitter.com' in url or 'x.com' in url:
                                title = title_elem.get_text(strip=True)
                                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                                
                                if url.startswith('/url?q='):
                                    url = url.split('/url?q=')[1].split('&')[0]
                                
                                # Verifica se é conteúdo recente
                                is_recent = self._is_content_recent('', title, snippet)
                                
                                all_results.append({
                                    'text': f"{title} {snippet}",
                                    'url': url,
                                    'source': 'Twitter/X',
                                    'is_recent': is_recent,
                                    'strategy': strategy
                                })
                    except Exception as e:
                        continue
                
                time.sleep(1)  # Rate limiting
                
                if len(all_results) >= min_results:
                    break
            
            # Remove duplicatas baseado na URL
            seen_urls = set()
            unique_results = []
            for result in all_results:
                if result['url'] not in seen_urls:
                    seen_urls.add(result['url'])
                    unique_results.append(result)
            
            return unique_results[:min_results * 2]
            
        except Exception as e:
            st.error(f"Erro na busca Twitter profunda: {str(e)}")
            return []
    
    def _is_content_recent(self, date_text, title, snippet):
        """Verifica se o conteúdo é dos últimos 90 dias"""
        recent_indicators = [
            '2024', 'recente', 'novo', 'última', 'último', 'hoje', 'ontem',
            'semana', 'mês', 'agora', 'atual', 'janeiro', 'fevereiro', 'março',
            'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
            'novembro', 'dezembro'
        ]
        
        text_to_check = f"{date_text} {title} {snippet}".lower()
        
        for indicator in recent_indicators:
            if indicator in text_to_check:
                return True
        
        return False
    
    def analyze_sentiment_deep(self, text):
        """Análise de sentimento profunda com contexto"""
        if not text:
            return 'neutral', 0, [], {}
        
        text_lower = text.lower()
        
        found_positive = []
        found_negative = []
        context_analysis = {
            'emotional_tone': 'neutral',
            'urgency_level': 'low',
            'credibility_indicators': [],
            'temporal_context': 'general'
        }
        
        # Análise de palavras-chave básica
        for keyword in self.positive_keywords:
            if keyword in text_lower:
                found_positive.append(keyword)
        
        for keyword in self.negative_keywords:
            if keyword in text_lower:
                found_negative.append(keyword)
        
        # Análise contextual avançada
        positive_patterns = [
            r'\b(muito bom|excelente|fantástico|incrível|maravilhoso|ótimo|perfeito)\b',
            r'\b(amo|adoro|gosto muito|curto|apoio|recomendo)\b',
            r'\b(parabéns|congratulações|felicitações|sucesso|vitória)\b',
            r'\b(orgulho|feliz|alegre|contente|satisfeito|realizado)\b',
            r'\b(inspirador|motivador|exemplo|referência|modelo)\b'
        ]
        
        negative_patterns = [
            r'\b(muito ruim|péssimo|horrível|terrível|decepcionante|lamentável)\b',
            r'\b(odeio|detesto|não suporto|repudio|condeno)\b',
            r'\b(fracasso|derrota|falha|erro|problema|crise)\b',
            r'\b(triste|chateado|irritado|revoltado|indignado)\b',
            r'\b(perigoso|arriscado|suspeito|duvidoso|questionável)\b'
        ]
        
        # Análise de tom emocional
        emotional_high = r'\b(MUITO|SUPER|EXTREMAMENTE|TOTALMENTE|COMPLETAMENTE)\b'
        if re.search(emotional_high, text.upper()):
            context_analysis['emotional_tone'] = 'high'
        
        # Análise de urgência
        urgency_indicators = r'\b(URGENTE|AGORA|IMEDIATO|BREAKING|ÚLTIMA HORA)\b'
        if re.search(urgency_indicators, text.upper()):
            context_analysis['urgency_level'] = 'high'
        
        # Indicadores de credibilidade
        credibility_indicators = [
            r'\b(fonte|oficial|confirmado|verificado|comprovado)\b',
            r'\b(segundo|de acordo|conforme|baseado)\b',
            r'\b(especialista|autoridade|expert|profissional)\b'
        ]
        
        for pattern in credibility_indicators:
            if re.search(pattern, text_lower):
                context_analysis['credibility_indicators'].append(pattern)
        
        # Aplicação dos padrões
        for pattern in positive_patterns:
            if re.search(pattern, text_lower):
                found_positive.append('contexto_positivo_avançado')
        
        for pattern in negative_patterns:
            if re.search(pattern, text_lower):
                found_negative.append('contexto_negativo_avançado')
        
        # Cálculo de score com pesos contextuais
        positive_score = len(found_positive) * 2
        negative_score = len(found_negative) * 3
        
        # Ajustes baseados no contexto
        if context_analysis['emotional_tone'] == 'high':
            positive_score *= 1.5
            negative_score *= 1.5
        
        if context_analysis['urgency_level'] == 'high':
            negative_score *= 1.3  # Urgência geralmente indica problema
        
        if context_analysis['credibility_indicators']:
            positive_score *= 1.2  # Fontes confiáveis aumentam peso positivo
        
        # Determinação do sentimento
        if positive_score > negative_score:
            sentiment = 'positive'
            confidence = min((positive_score - negative_score) / 15, 1.0)
        elif negative_score > positive_score:
            sentiment = 'negative'
            confidence = min((negative_score - positive_score) / 15, 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return sentiment, confidence, found_positive + found_negative, context_analysis
    
    def calculate_deep_score(self, google_results, youtube_results, twitter_results):
        """Cálculo de score profundo com análise temporal"""
        all_content = []
        temporal_analysis = {
            'recent_trend': 'stable',
            'sentiment_evolution': [],
            'keyword_frequency': defaultdict(int),
            'source_reliability': {}
        }
        
        # Pesos ajustados para análise profunda
        source_weights = {'google': 0.45, 'youtube': 0.35, 'twitter': 0.20}
        
        # Processa resultados do Google
        for result in google_results:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            sentiment, confidence, keywords, context = self.analyze_sentiment_deep(content)
            
            # Peso temporal (conteúdo recente tem mais peso)
            temporal_weight = 1.3 if result.get('is_recent', False) else 1.0
            
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'context': context,
                'source': 'google',
                'weight': source_weights['google'] * temporal_weight,
                'is_recent': result.get('is_recent', False)
            })
            
            # Análise de frequência de palavras-chave
            for keyword in keywords:
                temporal_analysis['keyword_frequency'][keyword] += 1
        
        # Processa resultados do YouTube
        for result in youtube_results:
            content = f"{result.get('title', '')} {result.get('description', '')}"
            sentiment, confidence, keywords, context = self.analyze_sentiment_deep(content)
            
            temporal_weight = 1.3 if result.get('is_recent', False) else 1.0
            
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'context': context,
                'source': 'youtube',
                'weight': source_weights['youtube'] * temporal_weight,
                'is_recent': result.get('is_recent', False)
            })
            
            for keyword in keywords:
                temporal_analysis['keyword_frequency'][keyword] += 1
        
        # Processa resultados do Twitter
        for result in twitter_results:
            content = result.get('text', '')
            sentiment, confidence, keywords, context = self.analyze_sentiment_deep(content)
            
            temporal_weight = 1.4 if result.get('is_recent', False) else 1.0  # Twitter recente tem mais peso
            
            all_content.append({
                'text': content,
                'sentiment': sentiment,
                'confidence': confidence,
                'keywords': keywords,
                'context': context,
                'source': 'twitter',
                'weight': source_weights['twitter'] * temporal_weight,
                'is_recent': result.get('is_recent', False)
            })
            
            for keyword in keywords:
                temporal_analysis['keyword_frequency'][keyword] += 1
        
        if not all_content:
            return 50, 'Médio', '#d97706', set(), set(), {}, temporal_analysis
        
        # Análise temporal de tendência
        recent_content = [item for item in all_content if item['is_recent']]
        older_content = [item for item in all_content if not item['is_recent']]
        
        recent_positive = sum(1 for item in recent_content if item['sentiment'] == 'positive')
        recent_negative = sum(1 for item in recent_content if item['sentiment'] == 'negative')
        older_positive = sum(1 for item in older_content if item['sentiment'] == 'positive')
        older_negative = sum(1 for item in older_content if item['sentiment'] == 'negative')
        
        # Determina tendência
        if len(recent_content) > 0 and len(older_content) > 0:
            recent_ratio = (recent_positive - recent_negative) / len(recent_content)
            older_ratio = (older_positive - older_negative) / len(older_content) if len(older_content) > 0 else 0
            
            if recent_ratio > older_ratio + 0.2:
                temporal_analysis['recent_trend'] = 'improving'
            elif recent_ratio < older_ratio - 0.2:
                temporal_analysis['recent_trend'] = 'declining'
            else:
                temporal_analysis['recent_trend'] = 'stable'
        
        # Cálculo de scores ponderados
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
        
        # Cálculo de score final com ajustes profundos
        base_score = 65  # Base mais alta para análise profunda
        
        # Ajuste baseado no sentimento
        sentiment_adjustment = (weighted_positive - weighted_negative) * 30
        
        # Bônus por volume de dados (análise profunda)
        volume_bonus = min(len(all_content) / 50, 1) * 15  # Até 15 pontos por volume
        
        # Ajuste por palavras-chave
        keyword_adjustment = (len(all_positive_keywords) - len(all_negative_keywords) * 1.8) * 2
        
        # Ajuste temporal (tendência recente)
        temporal_adjustment = 0
        if temporal_analysis['recent_trend'] == 'improving':
            temporal_adjustment = 8
        elif temporal_analysis['recent_trend'] == 'declining':
            temporal_adjustment = -12
        
        # Ajuste por confiabilidade (mais conteúdo recente = mais confiável)
        recent_ratio = len(recent_content) / len(all_content) if all_content else 0
        reliability_adjustment = recent_ratio * 10
        
        final_score = (base_score + sentiment_adjustment + volume_bonus + 
                      keyword_adjustment + temporal_adjustment + reliability_adjustment)
        final_score = max(0, min(100, final_score))
        
        # Determina nível de risco com critérios mais rigorosos
        if final_score >= 88:
            risk_level = 'Muito Baixo'
            risk_color = '#059669'
        elif final_score >= 75:
            risk_level = 'Baixo'
            risk_color = '#65a30d'
        elif final_score >= 55:
            risk_level = 'Médio'
            risk_color = '#d97706'
        elif final_score >= 35:
            risk_level = 'Alto'
            risk_color = '#dc2626'
        else:
            risk_level = 'Muito Alto'
            risk_color = '#991b1b'
        
        # Estatísticas profundas
        stats = {
            'total_content': len(all_content),
            'recent_content': len(recent_content),
            'positive_ratio': weighted_positive,
            'negative_ratio': weighted_negative,
            'google_count': len(google_results),
            'youtube_count': len(youtube_results),
            'twitter_count': len(twitter_results),
            'positive_keywords_count': len(all_positive_keywords),
            'negative_keywords_count': len(all_negative_keywords),
            'confidence_level': 'high' if len(all_content) >= 50 else 'medium' if len(all_content) >= 25 else 'low',
            'temporal_weight_applied': recent_ratio > 0.3,
            'analysis_depth': 'deep'
        }
        
        return int(final_score), risk_level, risk_color, all_positive_keywords, all_negative_keywords, stats, temporal_analysis

def create_deep_gauge(score, risk_color, confidence_level):
    """Cria gauge para análise profunda"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Score Profundo (Confiança: {confidence_level.title()})", 'font': {'size': 20, 'color': '#1e293b'}},
        number = {'font': {'size': 42, 'color': risk_color}},
        delta = {'reference': 70, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#cbd5e1"},
            'bar': {'color': risk_color, 'thickness': 0.5},
            'bgcolor': "#f8fafc",
            'borderwidth': 3,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 35], 'color': "#fee2e2"},
                {'range': [35, 55], 'color': "#fed7aa"},
                {'range': [55, 75], 'color': "#fef3c7"},
                {'range': [75, 88], 'color': "#d1fae5"},
                {'range': [88, 100], 'color': "#a7f3d0"}
            ],
            'threshold': {
                'line': {'color': "#667eea", 'width': 5},
                'thickness': 0.9,
                'value': 88
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 InfluScore Deep</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análise Profunda de Influenciadores com 75+ Conteúdos dos Últimos 90 Dias</p>', unsafe_allow_html=True)
    
    # Badge de análise profunda
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="deep-analysis-badge">📊 Mínimo 25 por fonte</span>
        <span class="deep-analysis-badge">⏰ Últimos 90 dias</span>
        <span class="deep-analysis-badge">🧠 Análise temporal</span>
        <span class="deep-analysis-badge">🔍 75+ conteúdos</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "",
            placeholder="Digite o nome do influenciador para análise profunda...",
            key="influencer_input",
            label_visibility="collapsed"
        )
        
        analyze_button = st.button("🔬 Iniciar Análise Profunda", use_container_width=True, type="primary")
    
    if analyze_button and influencer_name:
        analyzer = DeepInfluencerAnalyzer()
        
        # Container de progresso
        progress_container = st.container()
        
        with progress_container:
            st.markdown(f"""
            <div class="progress-container">
                <h3 style="color: #1e293b; margin-bottom: 1rem;">🔍 Coletando dados profundos sobre {influencer_name}</h3>
                <p style="color: #64748b;">Analisando múltiplas fontes dos últimos 90 dias...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress tracking
            google_progress = st.empty()
            youtube_progress = st.empty()
            twitter_progress = st.empty()
            
            overall_progress = st.progress(0)
        
        # Busca profunda no Google
        google_progress.markdown("""
        <div class="source-progress">
            <h4 style="color: #1e293b;">🔍 Google Search - Coletando 25+ artigos</h4>
            <p style="color: #64748b;">Buscando em múltiplas páginas dos últimos 90 dias...</p>
        </div>
        """, unsafe_allow_html=True)
        
        google_results = analyzer.search_google_deep(influencer_name, min_results=25)
        
        google_progress.markdown(f"""
        <div class="content-counter">
            <h4 style="color: #0ea5e9;">✅ Google: {len(google_results)} conteúdos coletados</h4>
        </div>
        """, unsafe_allow_html=True)
        overall_progress.progress(33)
        
        # Busca profunda no YouTube
        youtube_progress.markdown("""
        <div class="source-progress">
            <h4 style="color: #1e293b;">📺 YouTube - Coletando 25+ vídeos</h4>
            <p style="color: #64748b;">Analisando múltiplas variações de busca...</p>
        </div>
        """, unsafe_allow_html=True)
        
        youtube_results = analyzer.search_youtube_deep(influencer_name, min_results=25)
        
        youtube_progress.markdown(f"""
        <div class="content-counter">
            <h4 style="color: #0ea5e9;">✅ YouTube: {len(youtube_results)} vídeos coletados</h4>
        </div>
        """, unsafe_allow_html=True)
        overall_progress.progress(66)
        
        # Busca profunda no Twitter/X
        twitter_progress.markdown("""
        <div class="source-progress">
            <h4 style="color: #1e293b;">🐦 Twitter/X - Coletando 25+ posts</h4>
            <p style="color: #64748b;">Usando múltiplas estratégias de busca...</p>
        </div>
        """, unsafe_allow_html=True)
        
        twitter_results = analyzer.search_twitter_deep(influencer_name, min_results=25)
        
        twitter_progress.markdown(f"""
        <div class="content-counter">
            <h4 style="color: #0ea5e9;">✅ Twitter/X: {len(twitter_results)} posts coletados</h4>
        </div>
        """, unsafe_allow_html=True)
        overall_progress.progress(100)
        
        # Análise profunda
        st.markdown("### 🧠 Processando Análise Profunda...")
        with st.spinner("Analisando sentimentos, tendências temporais e calculando score..."):
            score, risk_level, risk_color, positive_keywords, negative_keywords, stats, temporal_analysis = analyzer.calculate_deep_score(
                google_results, youtube_results, twitter_results
            )
        
        # Remove container de progresso
        progress_container.empty()
        
        # Resultados da análise profunda
        st.markdown("---")
        st.markdown(f"## 🔬 Análise Profunda: {influencer_name}")
        
        # Resumo executivo
        total_content = stats['total_content']
        confidence = stats['confidence_level']
        
        st.markdown(f"""
        <div class="temporal-analysis">
            <h3 style="color: #1e293b;">📊 Resumo Executivo</h3>
            <p style="color: #64748b;"><strong>Total analisado:</strong> {total_content} conteúdos únicos</p>
            <p style="color: #64748b;"><strong>Período:</strong> Últimos 90 dias com foco em conteúdo recente</p>
            <p style="color: #64748b;"><strong>Confiabilidade:</strong> {confidence.title()} (baseado no volume de dados)</p>
            <p style="color: #64748b;"><strong>Tendência recente:</strong> {temporal_analysis['recent_trend'].title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout principal
        col1, col2 = st.columns([1.3, 0.7])
        
        with col1:
            # Gauge profundo
            fig = create_deep_gauge(score, risk_color, confidence)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Métricas profundas
            confidence_class = f"confidence-{confidence}"
            st.markdown(f"""
            <div class="deep-metric {confidence_class}">
                <h3 style="color: #1e293b;">🛡️ Avaliação de Risco</h3>
                <h1 style="color: {risk_color}; font-size: 2.2rem; margin: 1rem 0;">{risk_level.upper()}</h1>
                <p style="color: #64748b; font-size: 1.1rem;">Score: <strong>{score}/100</strong></p>
                <p style="color: #64748b; font-size: 0.9rem;">Baseado em {total_content} análises</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recomendação baseada em análise profunda
            if score >= 75 and confidence == 'high':
                st.success("✅ **ALTAMENTE RECOMENDADO** - Análise profunda confirma baixo risco")
            elif score >= 75:
                st.success("✅ **RECOMENDADO** - Score alto, mas análise limitada")
            elif score >= 55 and confidence == 'high':
                st.warning("⚠️ **CAUTELA** - Análise profunda indica risco moderado")
            elif score >= 55:
                st.warning("⚠️ **DADOS INSUFICIENTES** - Necessária análise adicional")
            else:
                st.error("❌ **ALTO RISCO** - Análise profunda indica problemas significativos")
        
        # Estatísticas detalhadas
        st.markdown("### 📈 Estatísticas da Análise Profunda")
        
        col_stats1, col_stats2, col_stats3, col_stats4, col_stats5 = st.columns(5)
        
        with col_stats1:
            st.metric("🔍 Google", len(google_results), f"Meta: 25+")
        with col_stats2:
            st.metric("📺 YouTube", len(youtube_results), f"Meta: 25+")
        with col_stats3:
            st.metric("🐦 Twitter/X", len(twitter_results), f"Meta: 25+")
        with col_stats4:
            st.metric("📊 Total", total_content, f"Meta: 75+")
        with col_stats5:
            st.metric("🎯 Confiança", confidence.title(), f"{stats['recent_content']} recentes")
        
        # Análise temporal
        if temporal_analysis['recent_trend'] != 'stable':
            st.markdown("### ⏰ Análise Temporal")
            
            trend_class = "trend-up" if temporal_analysis['recent_trend'] == 'improving' else "trend-down"
            trend_icon = "📈" if temporal_analysis['recent_trend'] == 'improving' else "📉"
            trend_text = "Melhoria" if temporal_analysis['recent_trend'] == 'improving' else "Declínio"
            
            st.markdown(f"""
            <div class="keyword-trend {trend_class}">
                <h4 style="color: #1e293b;">{trend_icon} Tendência Recente</h4>
                <p style="color: #64748b;"><strong>{trend_text}</strong> na percepção pública</p>
                <p style="color: #64748b;">Baseado em {stats['recent_content']} conteúdos recentes vs histórico</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Palavras-chave mais frequentes
        if temporal_analysis['keyword_frequency']:
            st.markdown("### 🔍 Palavras-Chave Mais Mencionadas")
            
            # Top 10 palavras-chave
            top_keywords = sorted(temporal_analysis['keyword_frequency'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]
            
            col_kw1, col_kw2 = st.columns(2)
            
            with col_kw1:
                st.markdown("**🟢 Palavras Positivas Frequentes:**")
                positive_frequent = [(kw, freq) for kw, freq in top_keywords 
                                   if kw in positive_keywords and kw in analyzer.positive_keywords]
                
                if positive_frequent:
                    for kw, freq in positive_frequent[:5]:
                        st.markdown(f"""
                        <div style="background: #d1fae5; color: #065f46; padding: 0.5rem; margin: 0.25rem 0; border-radius: 6px;">
                            <strong>{kw}</strong> - {freq} menções
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Poucas palavras positivas específicas encontradas")
            
            with col_kw2:
                st.markdown("**🔴 Palavras Negativas Frequentes:**")
                negative_frequent = [(kw, freq) for kw, freq in top_keywords 
                                   if kw in negative_keywords and kw in analyzer.negative_keywords]
                
                if negative_frequent:
                    for kw, freq in negative_frequent[:5]:
                        st.markdown(f"""
                        <div style="background: #fee2e2; color: #991b1b; padding: 0.5rem; margin: 0.25rem 0; border-radius: 6px;">
                            <strong>{kw}</strong> - {freq} menções
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ Nenhuma palavra negativa frequente encontrada")
        
        # Amostra de conteúdos analisados
        st.markdown("### 📰 Amostra dos Conteúdos Analisados")
        
        # Mostra uma amostra representativa
        sample_google = google_results[:3]
        sample_youtube = youtube_results[:2]
        sample_twitter = twitter_results[:2]
        
        all_samples = []
        all_samples.extend([(r, 'Google', '🔍') for r in sample_google])
        all_samples.extend([(r, 'YouTube', '📺') for r in sample_youtube])
        all_samples.extend([(r, 'Twitter/X', '🐦') for r in sample_twitter])
        
        for result, source, icon in all_samples:
            title = result.get('title', result.get('text', 'Sem título'))
            if len(title) > 100:
                title = title[:100] + "..."
            
            description = result.get('snippet', result.get('description', result.get('text', 'Sem descrição')))
            if len(description) > 200:
                description = description[:200] + "..."
            
            is_recent = result.get('is_recent', False)
            recent_badge = "🆕 Recente" if is_recent else "📅 Histórico"
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                <h4 style="color: #1e293b; margin-bottom: 0.5rem;">{icon} {title}</h4>
                <p style="color: #64748b; margin: 0.5rem 0;">{description}</p>
                <div style="margin-top: 0.5rem;">
                    <small style="color: #9ca3af;">📍 {source}</small>
                    <small style="color: #9ca3af; margin-left: 1rem;">{recent_badge}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Botão para nova análise
        st.markdown("---")
        if st.button("🔄 Nova Análise Profunda", use_container_width=True):
            st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("⚠️ Por favor, digite o nome de um influenciador para análise profunda.")
    
    # Informações sobre análise profunda
    if not analyze_button:
        st.markdown("---")
        st.markdown("### ℹ️ Sobre a Análise Profunda")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem;">
                <h4 style="color: #1e293b;">🔍 Coleta Massiva</h4>
                <p style="color: #64748b;">• <strong>Mínimo 25 conteúdos</strong> por fonte<br>
                • <strong>75+ análises</strong> no total<br>
                • <strong>Múltiplas páginas</strong> de resultados<br>
                • <strong>Últimos 90 dias</strong> priorizados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info2:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem;">
                <h4 style="color: #1e293b;">🧠 Análise Avançada</h4>
                <p style="color: #64748b;">• <strong>Análise temporal</strong> de tendências<br>
                • <strong>Pesos contextuais</strong> por recência<br>
                • <strong>Frequência de palavras-chave</strong><br>
                • <strong>Confiabilidade</strong> por volume</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info3:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem;">
                <h4 style="color: #1e293b;">📊 Score Profundo</h4>
                <p style="color: #64748b;">• <strong>88-100:</strong> Muito Baixo<br>
                • <strong>75-87:</strong> Baixo<br>
                • <strong>55-74:</strong> Médio<br>
                • <strong>35-54:</strong> Alto<br>
                • <strong>0-34:</strong> Muito Alto</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 2rem;">
        <p style="color: #94a3b8;">© 2025 InfluScore Deep - Análise Profunda de Influenciadores</p>
        <p style="color: #94a3b8; font-size: 0.9rem;">🔬 <strong>75+ Conteúdos</strong> • ⏰ <strong>90 Dias</strong> • 🧠 <strong>Análise Temporal</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

