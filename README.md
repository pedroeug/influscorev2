# 📊 InfluScore - Streamlit Edition

**Avaliador de Influenciadores com Interface Streamlit**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🚀 Deploy Instantâneo no Streamlit Cloud

### 1. **Fork este repositório**
### 2. **Conecte ao Streamlit Cloud**
   - Acesse: [share.streamlit.io](https://share.streamlit.io)
   - Conecte sua conta GitHub
   - Selecione este repositório
   - **Arquivo principal:** `streamlit_app.py`
### 3. **Deploy Automático** ✅

## 🏃‍♂️ Execução Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/InfluScore-Streamlit.git
cd InfluScore-Streamlit

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run streamlit_app.py
```

## ✨ Funcionalidades

### 🎯 **Análise Completa**
- ✅ Busca no Google, YouTube e Twitter/X
- ✅ Score visual de 0-100 com gauge animado
- ✅ Análise de sentimento avançada
- ✅ Detecção de palavras-chave de risco
- ✅ Preview das últimas matérias

### 🎨 **Interface Moderna**
- ✅ Design gradiente azul-rosa
- ✅ Layout responsivo
- ✅ Gráficos interativos Plotly
- ✅ Cards visuais elegantes
- ✅ Animações suaves

### 📊 **Algoritmo Inteligente**
- ✅ Análise ponderada por fonte
- ✅ 40+ palavras-chave positivas
- ✅ 30+ palavras-chave negativas
- ✅ Análise contextual avançada
- ✅ Score de confiança preciso

## 🎯 **Como Usar**

1. **Digite o nome do influenciador**
2. **Clique em "Analisar Influenciador"**
3. **Aguarde a análise automática**
4. **Visualize os resultados completos**

## 📈 **Níveis de Risco**

| Score | Nível | Cor | Recomendação |
|-------|-------|-----|--------------|
| 85-100 | Muito Baixo | 🟢 Verde | ✅ Recomendado |
| 70-84 | Baixo | 🟡 Verde claro | ✅ Recomendado |
| 50-69 | Médio | 🟡 Amarelo | ⚠️ Cautela |
| 30-49 | Alto | 🟠 Laranja | ❌ Não recomendado |
| 0-29 | Muito Alto | 🔴 Vermelho | ❌ Alto risco |

## 🔧 **Configuração**

### Variáveis de Ambiente (Opcional)
```bash
# .env
GOOGLE_API_KEY=sua-chave-google-api
YOUTUBE_API_KEY=sua-chave-youtube-api
TWITTER_BEARER_TOKEN=seu-token-twitter
```

### Personalização
- **Cores:** Edite `.streamlit/config.toml`
- **Palavras-chave:** Modifique `analyzer.py`
- **Layout:** Customize `streamlit_app.py`

## 🌐 **Deploy em Outras Plataformas**

### **Heroku**
```bash
# Adicione ao requirements.txt:
# gunicorn==20.1.0

# Crie Procfile:
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

### **Railway**
```bash
# Deploy automático via GitHub
# Comando: streamlit run streamlit_app.py --server.port=$PORT
```

### **Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
```

## 📱 **Screenshots**

### Interface Principal
![Interface](https://via.placeholder.com/800x400/6366f1/ffffff?text=InfluScore+Interface)

### Análise Completa
![Análise](https://via.placeholder.com/800x400/ec4899/ffffff?text=Análise+Detalhada)

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 **Licença**

MIT License - use livremente!

## 🙏 **Agradecimentos**

- **Streamlit** - Framework incrível
- **Plotly** - Gráficos interativos
- **Comunidade Python** - Suporte constante

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

🚀 **Deploy em 30 segundos no Streamlit Cloud!** 🚀

