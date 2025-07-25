import streamlit as st
import requests
import json
import time
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import defaultdict
import re
import subprocess
import os
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Configuração da página
st.set_page_config(
    page_title="InfluScore Real - Busca Verdadeira", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed"
)

# CSS (resumido aqui)
st.markdown(
    """
    <style>
        /* … estilos omitidos para brevidade … */
    </style>
    """,
    unsafe_allow_html=True,
)

class RealSearchAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            "sucesso", "família", "caridade", "educação", "conquista",
            "prêmio", "reconhecimento", "inovação", "inspiração", "liderança",
            "amor", "felicidade", "vitória", "crescimento", "desenvolvimento",
            # … restante da lista …
        ]
        self.negative_keywords = [
            "roubo", "casino", "preso", "escândalo",
            # … restante da lista …
        ]
        # Configurações de API para buscas reais
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    def _google_scrape(self, query, max_results=25):
        """Raspa resultados simples do Google."""
        try:
            url = "https://r.jina.ai/https://www.google.com/search"
            params = {"q": query}
            resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for g in soup.select("div.g"):
                title = g.find("h3")
                if not title:
                    continue
                link = g.find("a", href=True)
                snippet = g.find("span", class_="aCOpRe")
                results.append(
                    {
                        "title": title.get_text(strip=True),
                        "snippet": snippet.get_text(strip=True) if snippet else "",
                        "url": link["href"] if link else "",
                        "source": "Google (scrape)",
                    }
                )
                if len(results) >= max_results:
                    break
            return results
        except Exception as e:
            st.error(f"Erro na raspagem do Google: {e}")
            return []

    def _twitter_scrape(self, query, max_results=25):
        """Obtém posts do Twitter via busca no Google."""
        return self._google_scrape(f"site:twitter.com {query}", max_results)

    def search_web_real(self, query, max_results=25):
        """Busca no Google usando API ou raspagem quando não houver chave."""
        st.info(f"🔍 Fazendo busca no Google para: {query}")

        if self.google_api_key and self.google_cx:
            results = []
            start = 1
            while len(results) < max_results:
                params = {
                    "key": self.google_api_key,
                    "cx": self.google_cx,
                    "q": query,
                    "num": min(10, max_results - len(results)),
                    "start": start,
                }
                try:
                    response = requests.get(
                        "https://www.googleapis.com/customsearch/v1",
                        params=params,
                        timeout=10,
                    )
                    response.raise_for_status()
                    for item in response.json().get("items", []):
                        results.append(
                            {
                                "title": item.get("title"),
                                "snippet": item.get("snippet"),
                                "url": item.get("link"),
                                "source": "Google API",
                            }
                        )
                        if len(results) >= max_results:
                            break
                    if not response.json().get("items"):
                        break
                except Exception as e:
                    st.error(f"Erro na busca Google API: {e}")
                    break

                start += 10

            st.success(f"✅ Coletados {len(results)} resultados do Google API")
            return results

        st.info("Sem chaves de API. Usando raspagem simples do Google.")
        return self._google_scrape(query, max_results)
