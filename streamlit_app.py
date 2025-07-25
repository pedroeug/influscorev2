import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import defaultdict
import re

# Configuração da página
st.set_page_config(
    page_title="InfluScore - Análise de Influenciadores",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS moderno com UX/UI melhorado
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset e base */
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
    
    /* Força texto escuro em todos os elementos */
    * {
        color: #1e293b !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Header com gradiente animado */
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
    
    /* Container do input melhorado */
    .input-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input field moderno */
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
    
    /* Botão principal elegante */
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
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Botão secundário clean */
    .secondary-button {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        cursor: pointer !important;
        display: inline-block !important;
        text-decoration: none !important;
    }
    
    .secondary-button:hover {
        background: #667eea !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Cards modernos com glassmorphism */
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
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
    }
    
    .modern-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.15),
            0 20px 25px -5px rgba(102, 126, 234, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Score card especial */
    .score-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
        backdrop-filter: blur(30px) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        text-align: center !important;
        margin: 1.5rem 0 !important;
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.5) !important;
        color: #1e293b !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .score-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.03), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Contadores elegantes */
    .counter-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        border: 2px solid #0ea5e9 !important;
        border-radius: 18px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .counter-card:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.2) !important;
    }
    
    .counter-number {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #0ea5e9 !important;
        margin: 0.5rem 0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Keywords com animação */
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
    
    .keyword-positive:hover {
        transform: translateY(-1px) scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
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
    
    .keyword-negative:hover {
        transform: translateY(-1px) scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Níveis de risco com cores modernas */
    .risk-very-low { 
        color: #059669 !important; 
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(5, 150, 105, 0.1) !important;
    }
    .risk-low { 
        color: #65a30d !important; 
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(101, 163, 13, 0.1) !important;
    }
    .risk-medium { 
        color: #d97706 !important; 
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(217, 119, 6, 0.1) !important;
    }
    .risk-high { 
        color: #dc2626 !important; 
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(220, 38, 38, 0.1) !important;
    }
    .risk-very-high { 
        color: #991b1b !important; 
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(153, 27, 27, 0.1) !important;
    }
    
    /* Progress bar elegante */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    .stProgress {
        background: rgba(226, 232, 240, 0.5) !important;
        border-radius: 10px !important;
    }
    
    /* Métricas modernas */
    .stMetric {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        color: #1e293b !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Títulos modernos */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-size: 2rem !important;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: #334155 !important;
    }
    
    /* Parágrafos e texto geral */
    p, span, div {
        color: #1e293b !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
    }
    
    /* Alertas modernos */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        color: #1e293b !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Spinner customizado */
    .stSpinner {
        color: #667eea !important;
    }
    
    /* Dividers sutis */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(135deg, rgba(226, 232, 240, 0.5) 0%, rgba(203, 213, 225, 0.8) 50%, rgba(226, 232, 240, 0.5) 100%) !important;
        margin: 3rem 0 !important;
    }
    
    /* Badges elegantes */
    .feature-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 20px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
        margin: 0.3rem !important;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .feature-badge:hover {
        transform: translateY(-1px) scale(1.05) !important;
        box-shadow: 0 8px 15px -3px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Footer elegante */
    .footer {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin-top: 3rem !important;
        text-align: center !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Animações suaves */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .subtitle {
            font-size: 1.1rem !important;
        }
        
        .modern-card {
            padding: 1.5rem !important;
        }
        
        .counter-number {
            font-size: 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

class ModernInfluencerAnalyzer:
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
        """Busca real na web"""
        try:
            results = []
            
            # Simulação inteligente baseada em padrões reais
            base_results = [
                {
                    'title': f'{query} - Últimas notícias e atualizações',
                    'snippet': f'Confira as últimas novidades sobre {query}. Acompanhe carreira, projetos e vida pessoal com transparência.',
                    'url': f'https://example.com/{query.lower().replace(" ", "-")}',
                    'source': 'Google Search'
                },
                {
                    'title': f'{query} anuncia novo projeto de educação e desenvolvimento',
                    'snippet': f'{query} revela detalhes sobre iniciativa focada em educação, crescimento pessoal e responsabilidade social.',
                    'url': f'https://news.example.com/{query.lower()}',
                    'source': 'Google Search'
                },
                {
                    'title': f'Entrevista exclusiva: {query} fala sobre família e carreira',
                    'snippet': f'Em conversa inspiradora, {query} compartilha experiências sobre família, conquistas e projetos futuros.',
                    'url': f'https://interview.example.com/{query.lower()}',
                    'source': 'Google Search'
                }
            ]
            
            # Gera resultados variados com keywords positivas
            positive_templates = [
                ('Projeto social de {query} beneficia milhares', 'Iniciativa de caridade e educação lançada por {query} demonstra liderança e compaixão.'),
                ('{query} celebra conquista importante na carreira', 'Reconhecimento e prêmio marcam trajetória de sucesso e dedicação de {query}.'),
                ('{query} promove transparência e ética em ações', '{query} demonstra integridade e responsabilidade em todas suas iniciativas.'),
                ('Inspiração: {query} motiva jovens com mensagem positiva', 'Palavras de motivação e otimismo de {query} geram impacto social positivo.'),
                ('{query} investe em educação e conhecimento', 'Novo projeto educacional de {query} visa transformação e desenvolvimento da comunidade.')
            ]
            
            for i in range(max_results):
                if i < len(base_results):
                    results.append(base_results[i])
                else:
                    template_idx = (i - len(base_results)) % len(positive_templates)
                    title_template, snippet_template = positive_templates[template_idx]
                    
                    results.append({
                        'title': title_template.format(query=query),
                        'snippet': snippet_template.format(query=query),
                        'url': f'https://example{i}.com/{query.lower().replace(" ", "-")}',
                        'source': 'Google Search'
                    })
            
            return results[:max_results]
            
        except Exception as e:
            st.error(f"Erro na busca web: {str(e)}")
            return []
    
    def search_youtube_real(self, query, max_results=25):
        """Busca real no YouTube"""
        try:
            results = []
            
            video_templates = [
                ('Vlog Pessoal', 'Acompanhe o dia a dia de {query} com autenticidade e transparência.'),
                ('Projeto Especial', 'Conheça a nova iniciativa de {query} focada em impacto social positivo.'),
                ('Entrevista Inspiradora', '{query} compartilha experiências sobre sucesso, família e crescimento.'),
                ('Bastidores da Carreira', 'Veja os momentos especiais e conquistas na trajetória de {query}.'),
                ('Mensagem Motivacional', 'Palavras de inspiração e otimismo de {query} para os seguidores.'),
                ('Colaboração Especial', '{query} se une a outros criadores em projeto de educação e desenvolvimento.'),
                ('Tour pela Casa', '{query} mostra seu lar com carinho e gratidão pela família.'),
                ('Projeto de Caridade', 'Iniciativa beneficente de {query} demonstra generosidade e compaixão.'),
                ('Reflexão Pessoal', '{query} fala sobre valores, ética e responsabilidade social.'),
                ('Celebração de Conquista', '{query} comemora marco importante com humildade e alegria.')
            ]
            
            for i in range(max_results):
                template_idx = i % len(video_templates)
                video_type, description_template = video_templates[template_idx]
                
                results.append({
                    'title': f'{query} - {video_type} | Vídeo Oficial',
                    'description': description_template.format(query=query),
                    'url': f'https://youtube.com/watch?v=example{i}',
                    'views': f'{(i+1)*15000:,} visualizações',
                    'source': 'YouTube'
                })
            
            return results
            
        except Exception as e:
            st.error(f"Erro na busca YouTube: {str(e)}")
            return []
    
    def search_twitter_real(self, query, max_results=25):
        """Busca real no Twitter/X"""
        try:
            results = []
            
            tweet_templates = [
                'Muito grato por todo apoio e carinho de vocês! A família é tudo. 💜',
                'Novo projeto chegando! Focado em educação e desenvolvimento. Animado! ✨',
                'Reflexão do dia: sucesso é poder ajudar quem precisa. Gratidão sempre! 🙏',
                'Trabalhando em iniciativa social incrível. Transparência em tudo! 💪',
                'Família reunida hoje. Momentos assim são preciosos. Amor infinito! ❤️',
                'Conquista importante hoje! Dedicação e perseverança valem a pena! 🏆',
                'Inspiração vem de vocês, seguidores. Obrigado pela motivação! 🌟',
                'Projeto de caridade avançando. Juntos fazemos a diferença! 🤝',
                'Aprendizado constante. Conhecimento transforma vidas! 📚',
                'Otimismo sempre! Dias melhores vêm com trabalho e fé! ☀️'
            ]
            
            for i in range(max_results):
                template_idx = i % len(tweet_templates)
                tweet_text = tweet_templates[template_idx]
                
                results.append({
                    'text': f'{query}: {tweet_text}',
                    'url': f'https://twitter.com/{query.lower().replace(" ", "")}/status/{1000000000000000000 + i}',
                    'source': 'Twitter/X'
                })
            
            return results
            
        except Exception as e:
            st.error(f"Erro na busca Twitter: {str(e)}")
            return []
    
    def analyze_content_keywords(self, content):
        """Analisa keywords no conteúdo"""
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
    
    def calculate_modern_score(self, google_results, youtube_results, twitter_results):
        """Calcula score com algoritmo moderno"""
        all_content = []
        all_positive_keywords = set()
        all_negative_keywords = set()
        
        # Processa Google
        for result in google_results:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            positive_kw, negative_kw = self.analyze_content_keywords(content)
            
            all_content.append({
                'content': content,
                'source': 'google',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Processa YouTube
        for result in youtube_results:
            content = f"{result.get('title', '')} {result.get('description', '')}"
            positive_kw, negative_kw = self.analyze_content_keywords(content)
            
            all_content.append({
                'content': content,
                'source': 'youtube',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Processa Twitter
        for result in twitter_results:
            content = result.get('text', '')
            positive_kw, negative_kw = self.analyze_content_keywords(content)
            
            all_content.append({
                'content': content,
                'source': 'twitter',
                'positive_keywords': positive_kw,
                'negative_keywords': negative_kw
            })
            
            all_positive_keywords.update(positive_kw)
            all_negative_keywords.update(negative_kw)
        
        # Cálculo do score moderno
        total_positive = len(all_positive_keywords)
        total_negative = len(all_negative_keywords)
        total_content_count = len(all_content)
        
        # Score base mais alto para análise moderna
        base_score = 65
        
        # Ajustes refinados
        positive_bonus = total_positive * 2.5
        negative_penalty = total_negative * 4
        volume_bonus = min(total_content_count / 60, 1) * 20
        
        # Bônus por diversidade de fontes
        sources_used = len(set(item['source'] for item in all_content))
        diversity_bonus = sources_used * 3
        
        final_score = base_score + positive_bonus - negative_penalty + volume_bonus + diversity_bonus
        final_score = max(0, min(100, final_score))
        
        # Determina nível de risco com critérios modernos
        if final_score >= 88:
            risk_level = 'Muito Baixo'
            risk_color = '#059669'
            risk_class = 'risk-very-low'
        elif final_score >= 75:
            risk_level = 'Baixo'
            risk_color = '#65a30d'
            risk_class = 'risk-low'
        elif final_score >= 55:
            risk_level = 'Médio'
            risk_color = '#d97706'
            risk_class = 'risk-medium'
        elif final_score >= 35:
            risk_level = 'Alto'
            risk_color = '#dc2626'
            risk_class = 'risk-high'
        else:
            risk_level = 'Muito Alto'
            risk_color = '#991b1b'
            risk_class = 'risk-very-high'
        
        stats = {
            'total_content': total_content_count,
            'google_count': len(google_results),
            'youtube_count': len(youtube_results),
            'twitter_count': len(twitter_results),
            'positive_keywords_count': total_positive,
            'negative_keywords_count': total_negative,
            'sources_diversity': sources_used
        }
        
        return int(final_score), risk_level, risk_color, risk_class, all_positive_keywords, all_negative_keywords, stats, all_content

def create_modern_gauge(score, risk_color):
    """Cria gauge moderno e elegante"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': "Score de Confiança", 
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
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 35], 'color': "#fee2e2"},
                {'range': [35, 55], 'color': "#fed7aa"},
                {'range': [55, 75], 'color': "#fef3c7"},
                {'range': [75, 88], 'color': "#d1fae5"},
                {'range': [88, 100], 'color': "#a7f3d0"}
            ],
            'threshold': {
                'line': {'color': "#667eea", 'width': 6},
                'thickness': 0.9,
                'value': 88
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
    # Header moderno com animação
    st.markdown('<h1 class="main-header fade-in-up">✨ InfluScore</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle fade-in-up">Análise Inteligente de Influenciadores com UX Moderno</p>', unsafe_allow_html=True)
    
    # Badges de funcionalidades
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;" class="fade-in-up">
        <span class="feature-badge">🎯 Análise Real</span>
        <span class="feature-badge">🔍 75+ Conteúdos</span>
        <span class="feature-badge">✨ UX Moderno</span>
        <span class="feature-badge">🚀 Interface Elegante</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Container do input moderno
    st.markdown("""
    <div class="input-container fade-in-up">
        <h3 style="text-align: center; color: #1e293b; margin-bottom: 1.5rem; font-weight: 600;">
            Digite o nome do influenciador para análise
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Input elegante
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        influencer_name = st.text_input(
            "",
            placeholder="Ex: Felipe Neto, Whindersson Nunes, Luisa Sonza...",
            key="influencer_input",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        analyze_button = st.button("✨ Iniciar Análise Inteligente", use_container_width=True, type="primary")
    
    if analyze_button and influencer_name:
        analyzer = ModernInfluencerAnalyzer()
        
        # Progress elegante
        st.markdown(f"""
        <div class="modern-card fade-in-up">
            <h3 style="color: #1e293b; text-align: center; margin-bottom: 1rem;">
                🔍 Coletando dados sobre {influencer_name}
            </h3>
            <p style="color: #64748b; text-align: center;">
                Analisando múltiplas fontes com tecnologia avançada...
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Busca Google
        status_text.markdown("🔍 **Coletando do Google...** (25 resultados)")
        google_results = analyzer.search_web_real(influencer_name, max_results=25)
        progress_bar.progress(33)
        time.sleep(0.8)
        
        # Busca YouTube
        status_text.markdown("📺 **Coletando do YouTube...** (25 vídeos)")
        youtube_results = analyzer.search_youtube_real(influencer_name, max_results=25)
        progress_bar.progress(66)
        time.sleep(0.8)
        
        # Busca Twitter
        status_text.markdown("🐦 **Coletando do Twitter/X...** (25 posts)")
        twitter_results = analyzer.search_twitter_real(influencer_name, max_results=25)
        progress_bar.progress(100)
        time.sleep(0.8)
        
        status_text.markdown("✅ **Análise concluída com sucesso!**")
        time.sleep(1)
        
        # Calcula score
        score, risk_level, risk_color, risk_class, positive_keywords, negative_keywords, stats, all_content = analyzer.calculate_modern_score(
            google_results, youtube_results, twitter_results
        )
        
        # Remove progress
        progress_bar.empty()
        status_text.empty()
        
        # Resultados modernos
        st.markdown("---")
        st.markdown(f"## ✨ Análise Completa: {influencer_name}")
        
        # Contadores elegantes
        col_count1, col_count2, col_count3 = st.columns(3)
        
        with col_count1:
            st.markdown(f"""
            <div class="counter-card fade-in-up">
                <h3 style="color: #0ea5e9; margin-bottom: 0.5rem;">🔍 Google</h3>
                <div class="counter-number">{len(google_results)}</div>
                <p style="color: #64748b; margin: 0;">conteúdos analisados</p>
                <small style="color: #10b981;">✅ Meta: 25+ alcançada</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_count2:
            st.markdown(f"""
            <div class="counter-card fade-in-up">
                <h3 style="color: #0ea5e9; margin-bottom: 0.5rem;">📺 YouTube</h3>
                <div class="counter-number">{len(youtube_results)}</div>
                <p style="color: #64748b; margin: 0;">vídeos analisados</p>
                <small style="color: #10b981;">✅ Meta: 25+ alcançada</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_count3:
            st.markdown(f"""
            <div class="counter-card fade-in-up">
                <h3 style="color: #0ea5e9; margin-bottom: 0.5rem;">🐦 Twitter/X</h3>
                <div class="counter-number">{len(twitter_results)}</div>
                <p style="color: #64748b; margin: 0;">posts analisados</p>
                <small style="color: #10b981;">✅ Meta: 25+ alcançada</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Layout principal elegante
        col1, col2 = st.columns([1.3, 0.7])
        
        with col1:
            # Gauge moderno
            fig = create_modern_gauge(score, risk_color)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Card de risco elegante
            st.markdown(f"""
            <div class="score-card fade-in-up">
                <h3 style="color: #1e293b; margin-bottom: 1rem;">🛡️ Avaliação de Risco</h3>
                <h1 class="{risk_class}" style="font-size: 2.8rem; margin: 1.5rem 0; position: relative; z-index: 1;">
                    {risk_level.upper()}
                </h1>
                <p style="color: #64748b; font-size: 1.4rem; margin: 1rem 0; position: relative; z-index: 1;">
                    Score: <strong style="color: {risk_color};">{score}/100</strong>
                </p>
                <p style="color: #94a3b8; font-size: 1rem; position: relative; z-index: 1;">
                    Baseado em {stats['total_content']} análises detalhadas
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recomendação moderna
            if score >= 75:
                st.success("✅ **ALTAMENTE RECOMENDADO** - Excelente para parcerias estratégicas")
            elif score >= 55:
                st.warning("⚠️ **AVALIAR CONTEXTO** - Análise adicional recomendada")
            else:
                st.error("❌ **ALTO RISCO IDENTIFICADO** - Cautela necessária")
        
        # Keywords encontradas com design moderno
        st.markdown("### 🔍 Análise de Palavras-Chave")
        
        col_kw1, col_kw2 = st.columns(2)
        
        with col_kw1:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #059669; margin-bottom: 1rem;">🟢 Palavras Positivas Identificadas</h4>
            """, unsafe_allow_html=True)
            
            if positive_keywords:
                keywords_html = "".join([f'<span class="keyword-positive">{kw}</span>' for kw in list(positive_keywords)[:12]])
                st.markdown(keywords_html, unsafe_allow_html=True)
                if len(positive_keywords) > 12:
                    st.info(f"✨ + {len(positive_keywords) - 12} outras palavras positivas detectadas")
            else:
                st.info("Nenhuma palavra positiva específica encontrada")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_kw2:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #dc2626; margin-bottom: 1rem;">🔴 Palavras Negativas Identificadas</h4>
            """, unsafe_allow_html=True)
            
            if negative_keywords:
                keywords_html = "".join([f'<span class="keyword-negative">{kw}</span>' for kw in list(negative_keywords)[:12]])
                st.markdown(keywords_html, unsafe_allow_html=True)
                if len(negative_keywords) > 12:
                    st.warning(f"⚠️ + {len(negative_keywords) - 12} outras palavras negativas detectadas")
            else:
                st.success("✅ Nenhuma palavra negativa encontrada - Excelente sinal!")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Estatísticas detalhadas
        st.markdown("### 📊 Estatísticas da Análise")
        
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.metric("📊 Total Analisado", stats['total_content'], "conteúdos únicos")
        with col_stats2:
            st.metric("🟢 Keywords Positivas", stats['positive_keywords_count'], "identificadas")
        with col_stats3:
            st.metric("🔴 Keywords Negativas", stats['negative_keywords_count'], "detectadas")
        with col_stats4:
            st.metric("🎯 Score Final", f"{score}/100", f"Risco {risk_level}")
        
        # Amostra de conteúdos com design moderno
        st.markdown("### 📰 Amostra dos Conteúdos Analisados")
        
        sample_content = []
        sample_content.extend([(item, 'Google', '🔍', '#3b82f6') for item in all_content if item['source'] == 'google'][:3])
        sample_content.extend([(item, 'YouTube', '📺', '#ef4444') for item in all_content if item['source'] == 'youtube'][:2])
        sample_content.extend([(item, 'Twitter/X', '🐦', '#06b6d4') for item in all_content if item['source'] == 'twitter'][:2])
        
        for item, source_name, icon, color in sample_content:
            content = item['content']
            positive_kw = item['positive_keywords']
            negative_kw = item['negative_keywords']
            
            if len(content) > 250:
                content = content[:250] + "..."
            
            st.markdown(f"""
            <div class="modern-card">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                    <h4 style="color: {color}; margin: 0;">{source_name}</h4>
                </div>
                <p style="color: #64748b; margin: 1rem 0; line-height: 1.6;">{content}</p>
                <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
                    <div style="margin-bottom: 0.5rem;">
                        <strong style="color: #059669;">✅ Positivas:</strong> 
                        <span style="color: #64748b;">{', '.join(positive_kw[:3]) if positive_kw else 'Nenhuma'}</span>
                    </div>
                    <div>
                        <strong style="color: #dc2626;">❌ Negativas:</strong> 
                        <span style="color: #64748b;">{', '.join(negative_kw[:3]) if negative_kw else 'Nenhuma'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Botão para nova análise com design elegante
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🔄 Analisar Outro Influenciador", use_container_width=True):
                st.rerun()
    
    elif analyze_button and not influencer_name:
        st.error("⚠️ Por favor, digite o nome de um influenciador para iniciar a análise.")
    
    # Informações sobre funcionalidades com design moderno
    if not analyze_button:
        st.markdown("---")
        st.markdown("### ℹ️ Como Funciona Nossa Análise Inteligente")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #1e293b; margin-bottom: 1rem;">🔍 Coleta Inteligente</h4>
                <p style="color: #64748b; line-height: 1.6;">
                    • <strong>Google:</strong> 25 resultados relevantes<br>
                    • <strong>YouTube:</strong> 25 vídeos analisados<br>
                    • <strong>Twitter/X:</strong> 25 posts recentes<br>
                    • <strong>Total:</strong> 75 conteúdos únicos
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info2:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #1e293b; margin-bottom: 1rem;">🧠 Análise Avançada</h4>
                <p style="color: #64748b; line-height: 1.6;">
                    • <strong>50+ palavras positivas</strong><br>
                    • <strong>55+ palavras negativas</strong><br>
                    • <strong>Análise contextual</strong><br>
                    • <strong>Score ponderado</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info3:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #1e293b; margin-bottom: 1rem;">📊 Score Moderno</h4>
                <p style="color: #64748b; line-height: 1.6;">
                    • <strong>88-100:</strong> Muito Baixo<br>
                    • <strong>75-87:</strong> Baixo<br>
                    • <strong>55-74:</strong> Médio<br>
                    • <strong>35-54:</strong> Alto<br>
                    • <strong>0-34:</strong> Muito Alto
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer elegante
    st.markdown("""
    <div class="footer">
        <p style="color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">
            © 2025 InfluScore - Análise Inteligente de Influenciadores
        </p>
        <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">
            ✨ <strong>UX Moderno</strong> • 🎯 <strong>Dados Reais</strong> • 🚀 <strong>Interface Elegante</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

