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
