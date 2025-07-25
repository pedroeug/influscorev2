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
