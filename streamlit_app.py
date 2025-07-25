import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
try:
    from snscrape.modules.twitter import TwitterSearchScraper
except ImportError:
    from snscrape.modules.twitter import TwitterSearchScraper
from youtubesearchpython import VideosSearch

# Definição de stopwords em Português
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

# Funções auxiliares
def extract_keywords(text, num_keywords=5):
    words = [w for w in ''.join([c.lower() if c.isalpha() else ' ' for c in text]).split()
             if w not in STOPWORDS and len(w) > 3]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_items[:num_keywords]]

def score_result(text, query):
    q_words = [w.lower() for w in query.split() if len(w) > 0]
    if not q_words:
        return 0
    text_lower = text.lower()
    count = sum(1 for w in q_words if w in text_lower)
    return round((count / len(q_words)) * 100, 2)

# Scraping Google Search sem API
def search_google(query, num_results=30):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }
    params = {'q': query, 'hl': 'pt', 'num': num_results}
    resp = requests.get('https://www.google.com/search', headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    blocks = soup.find_all('div', class_='g')
    for block in blocks:
        if len(results) >= num_results:
            break
        try:
            a = block.find('a')
            link = a['href']
            title_tag = a.find('h3')
            title = title_tag.text.strip() if title_tag else ''
            snippet_div = block.find('div', class_='IsZvec')
            snippet = snippet_div.get_text(separator=' ').strip() if snippet_div else ''
            text = f"{title} {snippet}"
            keywords = extract_keywords(text)
            score = score_result(text, query)
            results.append({
                'source': 'google',
                'url': link,
                'title': title,
                'snippet': snippet,
                'keywords': keywords,
                'score': score
            })
            time.sleep(random.uniform(0.5, 1.5))
        except Exception:
            continue
    return results

# Scraping Twitter via snscrape
def search_twitter(query, num_results=30):
    results = []
    for i, tweet in enumerate(TwitterSearchScraper(query).get_items()):
        if i >= num_results:
            break
        text = tweet.content
        keywords = extract_keywords(text)
        score = score_result(text, query)
        url = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        results.append({
            'source': 'twitter',
            'url': url,
            'title': '',
            'snippet': text,
            'keywords': keywords,
            'score': score
        })
    return results

# Scraping YouTube via youtubesearchpython
def search_youtube(query, num_results=30):
    results = []
    try:
        vs = VideosSearch(query, limit=num_results)
        for video in vs.result().get('result', []):
            title = video.get('title', '')
            link = video.get('link', '')
            ds = video.get('descriptionSnippet')
            snippet = ' '.join([d.get('text', '') for d in ds]) if ds else ''
            text = f"{title} {snippet}"
            keywords = extract_keywords(text)
            score = score_result(text, query)
            results.append({
                'source': 'youtube',
                'url': link,
                'title': title,
                'snippet': snippet,
                'keywords': keywords,
                'score': score
            })
    except Exception:
        pass
    return results

# Interface Streamlit
def main():
    st.title('Buscador Real: Google, Twitter e YouTube')
    query = st.text_input('Termo de busca (mínimo 3 caracteres):')
    if st.button('Pesquisar'):
        if not query or len(query) < 3:
            st.warning('Informe um termo válido (mínimo 3 caracteres)')
            return

        with st.spinner('Pesquisando Google...'):
            google_res = search_google(query)
        with st.spinner('Pesquisando Twitter...'):
            twitter_res = search_twitter(query)
        with st.spinner('Pesquisando YouTube...'):
            youtube_res = search_youtube(query)

        total = len(google_res) + len(twitter_res) + len(youtube_res)
        if total < 30:
            st.error(f'Resultados insuficientes: {total}')

        df_g = pd.DataFrame(google_res)
        df_t = pd.DataFrame(twitter_res)
        df_y = pd.DataFrame(youtube_res)

        st.subheader('Resultados Google')
        st.dataframe(df_g)
        st.download_button('Baixar CSV Google', df_g.to_csv(index=False).encode('utf-8'), 'google.csv', 'text/csv')

        st.subheader('Resultados Twitter')
        st.dataframe(df_t)
        st.download_button('Baixar CSV Twitter', df_t.to_csv(index=False).encode('utf-8'), 'twitter.csv', 'text/csv')

        st.subheader('Resultados YouTube')
        st.dataframe(df_y)
        st.download_button('Baixar CSV YouTube', df_y.to_csv(index=False).encode('utf-8'), 'youtube.csv', 'text/csv')

if __name__ == '__main__':
    main()
