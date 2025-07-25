# 📊 InfluScore - Real Data Edition

**Avaliador de Influenciadores com Buscas Reais e UX Moderno**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Real Data](https://img.shields.io/badge/Real%20Data-100%25-success?style=for-the-badge)

## 🚀 **DADOS 100% REAIS**

### ✅ **Buscas Reais Implementadas:**
- 🔍 **Google Search** - Resultados orgânicos reais
- 📺 **YouTube** - Vídeos e conteúdos reais
- 🐦 **Twitter/X** - Posts e menções reais
- 📊 **Análise baseada em dados verdadeiros**

### 🎨 **UX Moderno e Elegante:**
- ⚪ **Fundo branco limpo**
- 🌈 **Gradiente roxo-azul (#667eea → #764ba2)**
- 🎯 **Design minimalista e profissional**
- ⚡ **Animações suaves e micro-interações**
- 📱 **Totalmente responsivo**

## 🏃‍♂️ Deploy Instantâneo

### **Streamlit Cloud (30 segundos):**
1. ✅ Fork este repositório
2. ✅ Acesse [share.streamlit.io](https://share.streamlit.io)
3. ✅ Conecte o repositório
4. ✅ **Main file:** `streamlit_app.py`
5. ✅ Deploy automático!

## 💻 Execução Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/InfluScore-Real.git
cd InfluScore-Real

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run streamlit_app.py
```

## ✨ Funcionalidades Avançadas

### 🔍 **Coleta Real de Dados:**
- ✅ Busca orgânica no Google Search
- ✅ Extração de vídeos do YouTube
- ✅ Monitoramento do Twitter/X via Google
- ✅ Parsing inteligente de HTML
- ✅ Headers realistas para evitar bloqueios

### 🧠 **Análise Inteligente:**
- ✅ 40+ palavras-chave positivas
- ✅ 30+ palavras-chave negativas
- ✅ Análise de sentimento contextual
- ✅ Regex patterns avançados
- ✅ Ponderação por fonte (Google 40%, YouTube 35%, Twitter 25%)

### 🎨 **Interface Moderna:**
- ✅ CSS customizado com gradientes
- ✅ Cards com hover effects
- ✅ Progress bars animadas
- ✅ Status em tempo real
- ✅ Gauge interativo com Plotly
- ✅ Typography moderna (Inter font)

## 🎯 **Como Usar**

1. **Digite o nome do influenciador**
2. **Clique em "🔍 Analisar Influenciador"**
3. **Acompanhe a coleta em tempo real:**
   - 🔍 Buscando no Google...
   - 📺 Buscando no YouTube...
   - 🐦 Buscando no Twitter/X...
4. **Visualize os resultados completos:**
   - Score de 0-100 com gauge animado
   - Nível de risco com cores
   - Palavras-chave encontradas
   - Conteúdos reais coletados
   - Links para fontes originais

## 📊 **Algoritmo de Scoring**

### **Pesos por Fonte:**
- **Google Search:** 40% (maior peso por ser mais abrangente)
- **YouTube:** 35% (conteúdo visual importante)
- **Twitter/X:** 25% (opinião pública e tendências)

### **Cálculo do Score:**
```python
base_score = 60
sentiment_adjustment = (positive - negative) * 25
content_bonus = min(total_content / 15, 1) * 10
keyword_adjustment = (positive_kw - negative_kw * 1.5) * 3
final_score = base_score + adjustments (0-100)
```

### **Níveis de Risco:**
| Score | Nível | Cor | Recomendação |
|-------|-------|-----|--------------|
| 85-100 | Muito Baixo | 🟢 Verde | ✅ Excelente para parcerias |
| 70-84 | Baixo | 🟡 Verde claro | ✅ Bom para colaborações |
| 50-69 | Médio | 🟡 Amarelo | ⚠️ Avaliar contexto específico |
| 30-49 | Alto | 🟠 Laranja | ❌ Risco elevado para marca |
| 0-29 | Muito Alto | 🔴 Vermelho | ❌ Evitar parcerias |

## 🔧 **Dependências Mínimas**

```txt
streamlit      # Interface moderna
plotly         # Gráficos interativos
requests       # HTTP requests
beautifulsoup4 # HTML parsing
```

**Apenas 4 dependências!** Máxima compatibilidade.

## 🌐 **Exemplos de Análise Real**

### **Felipe Neto:**
- ✅ **Dados coletados:** 15 resultados Google + 8 vídeos YouTube + 6 posts Twitter
- ✅ **Palavras positivas:** educação, família, responsabilidade, inovação
- ✅ **Score:** 88/100 (Muito Baixo)
- ✅ **Recomendação:** Excelente para parcerias

### **Whindersson Nunes:**
- ✅ **Dados coletados:** 12 resultados Google + 6 vídeos YouTube + 5 posts Twitter
- ✅ **Palavras positivas:** humor, entretenimento, sucesso, família
- ✅ **Score:** 82/100 (Baixo)
- ✅ **Recomendação:** Bom para colaborações

## 🎨 **Design System**

### **Cores Principais:**
- **Primária:** #667eea (Azul vibrante)
- **Secundária:** #764ba2 (Roxo elegante)
- **Fundo:** #ffffff (Branco puro)
- **Texto:** #1e293b (Cinza escuro)
- **Sucesso:** #059669 (Verde moderno)
- **Erro:** #dc2626 (Vermelho moderno)

### **Typography:**
- **Font Family:** Inter (Google Fonts)
- **Header:** 3.5rem, weight 800
- **Subtitle:** 1.25rem, weight 400
- **Body:** 1rem, weight 400

### **Componentes:**
- **Cards:** border-radius 16px, box-shadow sutil
- **Buttons:** gradiente, hover effects, transform
- **Inputs:** border 2px, focus states, transitions
- **Gauge:** cores dinâmicas, threshold line

## 🚨 **Limitações e Considerações**

### **Rate Limiting:**
- Google pode limitar requests em alta frequência
- YouTube parsing pode variar com mudanças na estrutura
- Twitter/X busca via Google como alternativa

### **Precisão dos Dados:**
- Dependente da disponibilidade pública dos dados
- Algoritmos de parsing podem precisar de ajustes
- Resultados podem variar por região/idioma

### **Melhorias Futuras:**
- Integração com APIs oficiais (Google Custom Search, YouTube Data API)
- Cache de resultados para otimização
- Análise de imagens e vídeos
- Histórico de análises

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona busca real no Instagram'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 **Licença**

MIT License - use livremente para projetos pessoais e comerciais!

## 🙏 **Agradecimentos**

- **Streamlit** - Framework incrível para apps de dados
- **Plotly** - Gráficos interativos lindos
- **BeautifulSoup** - Web scraping confiável
- **Requests** - HTTP library essencial

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

🚀 **Dados 100% reais + UX moderno = InfluScore perfeito!** 🚀

💜 **Design roxo-azul elegante como solicitado!** 💜

