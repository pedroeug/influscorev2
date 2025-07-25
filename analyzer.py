"""
Módulo de análise avançada para o InfluScore
Contém lógica de busca e análise de influenciadores
"""

import re


class AdvancedInfluencerAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            # Palavras relacionadas a sucesso e conquistas
            "sucesso",
            "conquista",
            "vitória",
            "prêmio",
            "reconhecimento",
            "liderança",
            "inovação",
            "inspiração",
            "motivação",
            "crescimento",
            "desenvolvimento",
            # Palavras relacionadas a valores familiares e sociais
            "família",
            "amor",
            "felicidade",
            "união",
            "harmonia",
            "paz",
            "solidariedade",
            "generosidade",
            "bondade",
            "compaixão",
            # Palavras relacionadas a responsabilidade social
            "caridade",
            "educação",
            "ensino",
            "aprendizado",
            "conhecimento",
            "ajuda",
            "apoio",
            "suporte",
            "colaboração",
            "parceria",
            # Palavras relacionadas a ética e transparência
            "ética",
            "transparência",
            "honestidade",
            "integridade",
            "responsabilidade",
            "confiança",
            "verdade",
            "sinceridade",
            "autenticidade",
            # Palavras relacionadas a impacto positivo
            "transformação",
            "mudança positiva",
            "impacto social",
            "benefício",
            "melhoria",
            "progresso",
            "evolução",
            "avanço",
        ]

        self.negative_keywords = [
            # Palavras relacionadas a crimes e problemas legais
            "roubo",
            "furto",
            "crime",
            "prisão",
            "preso",
            "condenação",
            "processo",
            "investigação",
            "acusação",
            "denúncia",
            "fraude",
            "golpe",
            "estelionato",
            # Palavras relacionadas a vícios e comportamentos prejudiciais
            "casino",
            "apostas",
            "vício",
            "drogas",
            "entorpecentes",
            "álcool",
            "dependência",
            "abuso",
            "excesso",
            # Palavras relacionadas a violência e agressão
            "violência",
            "agressão",
            "briga",
            "conflito",
            "discussão",
            "confusão",
            "pancadaria",
            "luta",
            "confronto",
            "hostilidade",
            # Palavras relacionadas a escândalos e polêmicas
            "escândalo",
            "polêmica",
            "controversia",
            "problema",
            "crise",
            "confusão",
            "bagunça",
            "tumulto",
            "alvoroço",
            # Palavras relacionadas a corrupção e desonestidade
            "corrupção",
            "suborno",
            "propina",
            "lavagem",
            "sonegação",
            "mentira",
            "falsidade",
            "enganação",
            "trapaça",
            # Palavras relacionadas a discriminação e preconceito
            "racismo",
            "preconceito",
            "discriminação",
            "intolerância",
            "machismo",
            "homofobia",
            "xenofobia",
        ]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    def search_google_news(self, query, max_results=10):
        """Busca notícias no Google (simulação melhorada)"""
        try:
            # Em produção, usar Google Custom Search API ou News API
            # Aqui simulamos com dados mais realistas

            base_results = [
                {
                    "title": f"{query} anuncia novo projeto social",
                    "url": f'https://g1.globo.com/entretenimento/{query.lower().replace(" ", "-")}-projeto-social',
                    "snippet": f"{query} lança iniciativa para ajudar comunidades carentes através da educação.",
                    "source": "G1",
                    "date": "2 dias atrás",
                    "sentiment": "positive",
                },
                {
                    "title": f"{query} se pronuncia sobre polêmica recente",
                    "url": f'https://folha.uol.com.br/celebridades/{query.lower().replace(" ", "-")}-polemica',
                    "snippet": f"{query} esclarece mal-entendido e pede desculpas aos fãs.",
                    "source": "Folha de S.Paulo",
                    "date": "1 semana atrás",
                    "sentiment": "neutral",
                },
                {
                    "title": f"{query} conquista prêmio de influenciador do ano",
                    "url": f'https://extra.globo.com/tv-e-lazer/{query.lower().replace(" ", "-")}-premio',
                    "snippet": f"{query} é reconhecido pelo impacto positivo nas redes sociais.",
                    "source": "Extra",
                    "date": "3 semanas atrás",
                    "sentiment": "positive",
                },
                {
                    "title": f"{query} fala sobre saúde mental",
                    "url": f'https://veja.abril.com.br/entretenimento/{query.lower().replace(" ", "-")}-saude-mental',
                    "snippet": f"{query} compartilha experiência pessoal para conscientizar seguidores.",
                    "source": "Veja",
                    "date": "1 mês atrás",
                    "sentiment": "positive",
                },
            ]

            return base_results[:max_results]

        except Exception as e:
            print(f"Erro na busca Google: {str(e)}")
            return []

    def search_youtube_videos(self, query, max_results=8):
        """Busca vídeos no YouTube (simulação melhorada)"""
        try:
            base_results = [
                {
                    "title": f"{query} - RESPONDENDO HATERS E FALANDO A VERDADE",
                    "url": f"https://youtube.com/watch?v=abc123",
                    "description": f"{query} responde críticas e esclarece polêmicas recentes",
                    "views": "2.1M visualizações",
                    "likes": "180K",
                    "date": "3 dias atrás",
                    "duration": "15:42",
                    "sentiment": "neutral",
                },
                {
                    "title": f"{query} - NOVO PROJETO QUE VAI MUDAR TUDO!",
                    "url": f"https://youtube.com/watch?v=def456",
                    "description": f"{query} anuncia projeto inovador para educação",
                    "views": "1.8M visualizações",
                    "likes": "220K",
                    "date": "1 semana atrás",
                    "duration": "12:30",
                    "sentiment": "positive",
                },
                {
                    "title": f"{query} - FAMÍLIA EM PRIMEIRO LUGAR",
                    "url": f"https://youtube.com/watch?v=ghi789",
                    "description": f"{query} fala sobre a importância da família",
                    "views": "1.5M visualizações",
                    "likes": "195K",
                    "date": "2 semanas atrás",
                    "duration": "18:15",
                    "sentiment": "positive",
                },
                {
                    "title": f"{query} - REAGINDO AOS COMENTÁRIOS",
                    "url": f"https://youtube.com/watch?v=jkl012",
                    "description": f"{query} reage aos comentários dos seguidores",
                    "views": "980K visualizações",
                    "likes": "85K",
                    "date": "3 semanas atrás",
                    "duration": "22:08",
                    "sentiment": "neutral",
                },
            ]

            return base_results[:max_results]

        except Exception as e:
            print(f"Erro na busca YouTube: {str(e)}")
            return []

    def search_twitter_posts(self, query, max_results=10):
        """Busca posts no Twitter/X (simulação melhorada)"""
        try:
            base_results = [
                {
                    "text": f'{query}: "Gratidão por mais um dia ao lado da minha família! ❤️ #família #gratidão"',
                    "url": f"https://twitter.com/user/status/123",
                    "likes": 25000,
                    "retweets": 5500,
                    "replies": 1200,
                    "date": "2 horas atrás",
                    "sentiment": "positive",
                },
                {
                    "text": f'{query}: "Novo projeto educacional chegando! Vamos transformar vidas através do conhecimento 📚✨"',
                    "url": f"https://twitter.com/user/status/456",
                    "likes": 18000,
                    "retweets": 4200,
                    "replies": 890,
                    "date": "1 dia atrás",
                    "sentiment": "positive",
                },
                {
                    "text": f'{query}: "Peço desculpas pelo mal-entendido. Sempre busco aprender e melhorar 🙏"',
                    "url": f"https://twitter.com/user/status/789",
                    "likes": 12000,
                    "retweets": 2800,
                    "replies": 1500,
                    "date": "3 dias atrás",
                    "sentiment": "neutral",
                },
                {
                    "text": f'{query}: "Obrigado pelo carinho de vocês! Juntos somos mais fortes 💪❤️"',
                    "url": f"https://twitter.com/user/status/101",
                    "likes": 22000,
                    "retweets": 3900,
                    "replies": 750,
                    "date": "5 dias atrás",
                    "sentiment": "positive",
                },
            ]

            return base_results[:max_results]

        except Exception as e:
            print(f"Erro na busca Twitter: {str(e)}")
            return []

    def analyze_text_sentiment(self, text):
        """Análise de sentimento mais sofisticada"""
        if not text:
            return "neutral", 0, []

        text_lower = text.lower()

        # Encontra palavras-chave específicas
        found_positive = []
        found_negative = []

        for keyword in self.positive_keywords:
            if keyword in text_lower:
                found_positive.append(keyword)

        for keyword in self.negative_keywords:
            if keyword in text_lower:
                found_negative.append(keyword)

        # Calcula score de sentimento
        positive_score = len(found_positive) * 2
        negative_score = len(found_negative) * 3  # Palavras negativas têm peso maior

        # Análise contextual adicional
        positive_patterns = [
            r"\b(muito bom|excelente|fantástico|incrível|maravilhoso)\b",
            r"\b(amo|adoro|gosto muito|curto)\b",
            r"\b(parabéns|congratulações|felicitações)\b",
            r"\b(sucesso|vitória|conquista|achievement)\b",
        ]

        negative_patterns = [
            r"\b(muito ruim|péssimo|horrível|terrível)\b",
            r"\b(odeio|detesto|não suporto)\b",
            r"\b(fracasso|derrota|falha|erro)\b",
            r"\b(problema|crise|confusão|bagunça)\b",
        ]

        for pattern in positive_patterns:
            if re.search(pattern, text_lower):
                positive_score += 1

        for pattern in negative_patterns:
            if re.search(pattern, text_lower):
                negative_score += 2

        # Determina sentimento final
        if positive_score > negative_score:
            sentiment = "positive"
            confidence = min((positive_score - negative_score) / 10, 1.0)
        elif negative_score > positive_score:
            sentiment = "negative"
            confidence = min((negative_score - positive_score) / 10, 1.0)
        else:
            sentiment = "neutral"
            confidence = 0.5

        return sentiment, confidence, found_positive + found_negative

    def calculate_advanced_score(self, google_results, youtube_results, twitter_results):
        """Cálculo de score mais avançado e preciso"""
        all_content = []
        source_weights = {"google": 0.4, "youtube": 0.35, "twitter": 0.25}

        # Processa resultados do Google
        for result in google_results:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            sentiment, confidence, keywords = self.analyze_text_sentiment(content)
            all_content.append(
                {
                    "text": content,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "keywords": keywords,
                    "source": "google",
                    "weight": source_weights["google"],
                }
            )

        # Processa resultados do YouTube
        for result in youtube_results:
            content = f"{result.get('title', '')} {result.get('description', '')}"
            sentiment, confidence, keywords = self.analyze_text_sentiment(content)
            all_content.append(
                {
                    "text": content,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "keywords": keywords,
                    "source": "youtube",
                    "weight": source_weights["youtube"],
                }
            )

        # Processa resultados do Twitter
        for result in twitter_results:
            content = result.get("text", "")
            sentiment, confidence, keywords = self.analyze_text_sentiment(content)
            all_content.append(
                {
                    "text": content,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "keywords": keywords,
                    "source": "twitter",
                    "weight": source_weights["twitter"],
                }
            )

        if not all_content:
            return 50, "Médio", "#f59e0b", set(), set(), {}

        # Calcula scores ponderados
        weighted_positive = 0
        weighted_negative = 0
        weighted_neutral = 0
        total_weight = 0

        all_positive_keywords = set()
        all_negative_keywords = set()

        for item in all_content:
            weight = item["weight"]
            confidence = item["confidence"]

            if item["sentiment"] == "positive":
                weighted_positive += weight * confidence
            elif item["sentiment"] == "negative":
                weighted_negative += weight * confidence
            else:
                weighted_neutral += weight * confidence

            total_weight += weight

            # Coleta palavras-chave
            for keyword in item["keywords"]:
                if keyword in self.positive_keywords:
                    all_positive_keywords.add(keyword)
                elif keyword in self.negative_keywords:
                    all_negative_keywords.add(keyword)

        # Normaliza scores
        if total_weight > 0:
            weighted_positive /= total_weight
            weighted_negative /= total_weight
            weighted_neutral /= total_weight

        # Calcula score final (0-100)
        base_score = 50  # Score neutro

        # Ajusta baseado no sentimento
        sentiment_adjustment = (weighted_positive - weighted_negative) * 30

        # Ajusta baseado na quantidade de conteúdo
        content_bonus = min(len(all_content) / 20, 1) * 10

        # Ajusta baseado nas palavras-chave
        keyword_adjustment = (len(all_positive_keywords) - len(all_negative_keywords) * 1.5) * 2

        final_score = base_score + sentiment_adjustment + content_bonus + keyword_adjustment
        final_score = max(0, min(100, final_score))

        # Determina nível de risco
        if final_score >= 85:
            risk_level = "Muito Baixo"
            risk_color = "#10b981"
        elif final_score >= 70:
            risk_level = "Baixo"
            risk_color = "#84cc16"
        elif final_score >= 50:
            risk_level = "Médio"
            risk_color = "#f59e0b"
        elif final_score >= 30:
            risk_level = "Alto"
            risk_color = "#f97316"
        else:
            risk_level = "Muito Alto"
            risk_color = "#ef4444"

        # Estatísticas detalhadas
        stats = {
            "total_content": len(all_content),
            "positive_ratio": weighted_positive,
            "negative_ratio": weighted_negative,
            "neutral_ratio": weighted_neutral,
            "google_count": len(google_results),
            "youtube_count": len(youtube_results),
            "twitter_count": len(twitter_results),
            "positive_keywords_count": len(all_positive_keywords),
            "negative_keywords_count": len(all_negative_keywords),
        }

        return int(final_score), risk_level, risk_color, all_positive_keywords, all_negative_keywords, stats
