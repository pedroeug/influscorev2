
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from youtubesearchpython import VideosSearch

# Stopwords em Português
STOPWORDS = set([
    'de','a','o','que','e','do','da','em','um','para','é','com','não','uma','os','no','se','na',
    'por','mais','as','dos','como','mas','foi','ao','ele','das','tem','à','seu','sua','ou','ser',
    'quando','muito','há','nos','já','está','eu','também','só','pelo','pela','até','isso','entre',
    'era','depois','sem','mesmo','aos','ter','seus','quem','nas','me','esse','eles','estão','você',
    'tinha','foram','essa','num','nem','suas','meu','às','minha','têm','numa','pelos','elas','havia',
    'seja','qual','será','nós','tenho','lhe','deles','essas','esses','pelas','este','fosse','dele',
    'tu','te','vocês','vos','lhes','meus','minhas','teu','tua','teus','tuas','nosso','nossa','nossos',
    'nossas','dela','delas','esta','estes','estas','aquele','aquela','aqueles','aquelas','isto','aquilo'
])

def extract_keywords(text, num_keywords=5):
    words = [w for w in ''.join([c.lower() if c.isalpha() else ' ' for c in text]).split()
             if w not in STOPWORDS and len(w) > 3]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_items[:num_keywords]]

def score_result(text, query):
    q_words = [w.lower() for w in query.split() if w]
    if not q_words:
        return 0
    count = sum(1 for w in q_words if w in text.lower())
    return round((count / len(q_words)) * 100, 2)

def search_google(query, num_results):
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'q': query, 'hl': 'pt', 'num': num_results}
    resp = requests.get('https://www.google.com/search', headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    blocks = soup.find_all('div', class_='g')
    for block in blocks:
        if len(results) >= num_results:
            break
        a = block.find('a')
        if not a or not a.get('href'):
            continue
        url = a['href']
        title = a.find('h3').get_text() if a.find('h3') else ''
        snippet_div = block.select_one('div.IsZvec')
        snippet = snippet_div.get_text(separator=' ') if snippet_div else ''
        text = f"{title} {snippet}"
        results.append({
            'url': url,
            'title': title,
            'snippet': snippet,
            'keywords': extract_keywords(text),
            'score': score_result(text, query)
        })
        time.sleep(random.uniform(0.5, 1.5))
    return results

def search_twitter(query, num_results):
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'f': 'tweets', 'q': query}
    resp = requests.get('https://nitter.net/search', headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    tweets = soup.find_all('div', class_='tweet-body')
    for tweet in tweets[:num_results]:
        snippet = tweet.get_text(separator=' ').strip()
        date_link = tweet.find_previous('a', class_='tweet-date')
        url = 'https://nitter.net' + date_link['href'] if date_link else ''
        results.append({
            'url': url,
            'title': '',
            'snippet': snippet,
            'keywords': extract_keywords(snippet),
            'score': score_result(snippet, query)
        })
    return results

def search_youtube(query, num_results):
    results = []
    vs = VideosSearch(query, limit=num_results)
    for video in vs.result().get('result', []):
        title = video.get('title','')
        url = video.get('link','')
        ds = video.get('descriptionSnippet') or []
        snippet = ' '.join([d.get('text','') for d in ds])
        text = f"{title} {snippet}"
        results.append({
            'url': url,
            'title': title,
            'snippet': snippet,
            'keywords': extract_keywords(text),
            'score': score_result(text, query)
        })
    return results

def main():
    st.set_page_config(page_title="Buscador Real", layout="wide")
    st.title("Buscador Real: Google, Twitter e YouTube")
    st.sidebar.header("Configurações")
    query = st.sidebar.text_input("Termo de busca", placeholder="Digite o termo", key="query")
    num_results = st.sidebar.slider("Resultados por fonte", 5, 100, 30, 5)
    if st.sidebar.button("Pesquisar"):
        if not query or len(query) < 3:
            st.sidebar.warning("Informe pelo menos 3 caracteres.")
        else:
            with st.spinner("Buscando..."):
                g_res = search_google(query, num_results)
                t_res = search_twitter(query, num_results)
                y_res = search_youtube(query, num_results)
            tabs = st.tabs(["Google", "Twitter", "YouTube"])
            with tabs[0]:
                st.subheader("Google")
                df = pd.DataFrame(g_res)
                st.dataframe(df, use_container_width=True)
                st.download_button("Baixar CSV Google", df.to_csv(index=False).encode('utf-8'), "google.csv", "text/csv")
            with tabs[1]:
                st.subheader("Twitter")
                df = pd.DataFrame(t_res)
                st.dataframe(df, use_container_width=True)
                st.download_button("Baixar CSV Twitter", df.to_csv(index=False).encode('utf-8'), "twitter.csv", "text/csv")
            with tabs[2]:
                st.subheader("YouTube")
                df = pd.DataFrame(y_res)
                st.dataframe(df, use_container_width=True)
                st.download_button("Baixar CSV YouTube", df.to_csv(index=False).encode('utf-8'), "youtube.csv", "text/csv")

if __name__ == "__main__":
    main()
