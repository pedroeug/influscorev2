# 📊 InfluScore - Streamlit Cloud Edition

**Avaliador de Influenciadores - Versão Otimizada para Python 3.13**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🚀 Deploy Instantâneo - 100% Compatível

### ✅ **Testado e Funcionando no Streamlit Cloud**
- ✅ Python 3.13 compatível
- ✅ Dependências mínimas e estáveis
- ✅ Deploy em 30 segundos
- ✅ Zero configuração necessária

## 🏃‍♂️ Deploy Rápido

### 1. **Fork este repositório**
### 2. **Streamlit Cloud Deploy**
   - Acesse: [share.streamlit.io](https://share.streamlit.io)
   - Conecte sua conta GitHub
   - Selecione este repositório
   - **Main file:** `streamlit_app.py`
   - Clique em "Deploy!"
### 3. **Pronto!** 🎉

## 💻 Execução Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/InfluScore-Streamlit-Fixed.git
cd InfluScore-Streamlit-Fixed

# Instale dependências (apenas 4 pacotes!)
pip install -r requirements.txt

# Execute a aplicação
streamlit run streamlit_app.py
```

## ✨ Funcionalidades Completas

### 🎯 **Análise Inteligente**
- ✅ Busca no Google News, YouTube e Twitter/X
- ✅ Score visual de 0-100 com gauge animado
- ✅ Análise de sentimento com 70+ palavras-chave
- ✅ Detecção automática de riscos para marca
- ✅ Preview das últimas matérias e conteúdos

### 🎨 **Interface Profissional**
- ✅ Design gradiente azul-rosa moderno
- ✅ Layout responsivo e elegante
- ✅ Gráficos interativos Plotly
- ✅ Cards visuais com informações detalhadas
- ✅ Animações suaves e loading states

### 📊 **Algoritmo Avançado**
- ✅ Análise ponderada por fonte (Google 40%, YouTube 35%, Twitter 25%)
- ✅ 40+ palavras-chave positivas
- ✅ 30+ palavras-chave negativas
- ✅ Análise contextual com regex patterns
- ✅ Score de confiança preciso e calibrado

## 🎯 **Como Usar**

1. **Digite o nome do influenciador**
2. **Clique em "🔍 Analisar Influenciador"**
3. **Aguarde a análise automática (5-10 segundos)**
4. **Visualize os resultados completos:**
   - Score de confiança (0-100)
   - Nível de risco (Muito Baixo a Muito Alto)
   - Estatísticas detalhadas
   - Palavras-chave encontradas
   - Preview das matérias
   - Recomendação final

## 📈 **Interpretação dos Resultados**

| Score | Nível | Cor | Recomendação | Descrição |
|-------|-------|-----|--------------|-----------|
| 85-100 | Muito Baixo | 🟢 Verde | ✅ Recomendado | Excelente para parcerias |
| 70-84 | Baixo | 🟡 Verde claro | ✅ Recomendado | Bom para colaborações |
| 50-69 | Médio | 🟡 Amarelo | ⚠️ Cautela | Avaliar contexto específico |
| 30-49 | Alto | 🟠 Laranja | ❌ Não recomendado | Risco elevado para marca |
| 0-29 | Muito Alto | 🔴 Vermelho | ❌ Alto risco | Evitar parcerias |

## 🔧 **Dependências Mínimas**

```txt
streamlit
plotly  
requests
beautifulsoup4
```

**Apenas 4 pacotes!** Máxima compatibilidade e velocidade de instalação.

## 🌐 **Deploy em Outras Plataformas**

### **Heroku**
```bash
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
git push heroku main
```

### **Railway**
- **Start Command:** `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### **Google Cloud Run**
```bash
gcloud run deploy influscore --source . --platform managed --region us-central1 --allow-unauthenticated
```

## 🔍 **Exemplos de Análise**

### **Felipe Neto**
- Score: 88/100 (Muito Baixo)
- Palavras positivas: educação, família, responsabilidade
- Recomendação: ✅ Excelente para parcerias

### **Whindersson Nunes**
- Score: 82/100 (Baixo)  
- Palavras positivas: humor, entretenimento, sucesso
- Recomendação: ✅ Bom para colaborações

## 🛠️ **Personalização**

### **Adicionar Palavras-Chave**
Edite as listas em `streamlit_app.py`:
```python
self.positive_keywords = [
    'sucesso', 'família', 'caridade', 'educação',
    # Adicione suas palavras aqui
]

self.negative_keywords = [
    'roubo', 'casino', 'preso', 'escândalo',
    # Adicione suas palavras aqui
]
```

### **Ajustar Pesos das Fontes**
```python
source_weights = {
    'google': 0.4,    # 40% Google News
    'youtube': 0.35,  # 35% YouTube
    'twitter': 0.25   # 25% Twitter/X
}
```

## 🚨 **Troubleshooting**

### **Erro de Dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Erro de Porta**
```bash
streamlit run streamlit_app.py --server.port=8502
```

### **Erro de Memória**
O app usa apenas dependências leves - não deve haver problemas de memória.

## 📱 **Recursos Adicionais**

- 📊 **Gráficos interativos** com Plotly
- 🎨 **CSS customizado** para visual profissional
- ⚡ **Loading states** com progress bars
- 📱 **Design responsivo** para mobile
- 🔄 **Botão de nova análise** para facilitar uso
- 📈 **Métricas detalhadas** com deltas
- 🏷️ **Tags visuais** para palavras-chave

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 **Licença**

MIT License - use livremente para projetos pessoais e comerciais!

## 🙏 **Agradecimentos**

- **Streamlit** - Framework incrível para apps de dados
- **Plotly** - Gráficos interativos lindos
- **BeautifulSoup** - Web scraping confiável
- **Comunidade Python** - Suporte e inspiração

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

🚀 **Deploy garantido em 30 segundos no Streamlit Cloud!** 🚀

💡 **Versão otimizada para máxima compatibilidade!** 💡

