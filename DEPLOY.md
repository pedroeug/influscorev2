# 🚀 Deploy Rápido - InfluScore Streamlit

## ⚡ Streamlit Cloud (30 segundos)

### 1. **Preparação**
- ✅ Fork este repositório no GitHub
- ✅ Certifique-se que `streamlit_app.py` está na raiz

### 2. **Deploy**
1. Acesse: [share.streamlit.io](https://share.streamlit.io)
2. Clique em "New app"
3. Conecte sua conta GitHub
4. Selecione: `seu-usuario/InfluScore-Streamlit`
5. **Main file path:** `streamlit_app.py`
6. Clique em "Deploy!"

### 3. **Pronto!** 🎉
Sua aplicação estará disponível em:
`https://seu-usuario-influscore-streamlit-streamlit-app-abc123.streamlit.app`

---

## 🐳 Docker (1 minuto)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/InfluScore-Streamlit.git
cd InfluScore-Streamlit

# Build da imagem
docker build -t influscore .

# Execute o container
docker run -p 8501:8501 influscore
```

Acesse: `http://localhost:8501`

---

## 🌐 Heroku (2 minutos)

### 1. **Preparação**
```bash
# Instale Heroku CLI
# Faça login: heroku login
```

### 2. **Deploy**
```bash
# Clone e configure
git clone https://github.com/seu-usuario/InfluScore-Streamlit.git
cd InfluScore-Streamlit

# Crie Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create seu-app-name
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## 🚄 Railway (1 minuto)

### 1. **Conecte GitHub**
- Acesse: [railway.app](https://railway.app)
- Conecte sua conta GitHub
- Selecione o repositório

### 2. **Configure**
- **Start Command:** `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
- **Port:** `8501`

### 3. **Deploy Automático** ✅

---

## ☁️ Google Cloud Run (3 minutos)

```bash
# Instale gcloud CLI
# Configure: gcloud auth login

# Build e deploy
gcloud run deploy influscore \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📱 Vercel (2 minutos)

### 1. **Instale Vercel CLI**
```bash
npm i -g vercel
```

### 2. **Configure**
Crie `vercel.json`:
```json
{
  "builds": [
    {
      "src": "streamlit_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "streamlit_app.py"
    }
  ]
}
```

### 3. **Deploy**
```bash
vercel --prod
```

---

## 🔧 Troubleshooting

### **Erro de Dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Erro de Porta**
Adicione ao final do `streamlit_app.py`:
```python
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8501))
    st._config.set_option("server.port", port)
    main()
```

### **Erro de Memória**
Adicione ao `requirements.txt`:
```
streamlit==1.28.1
--find-links https://download.pytorch.org/whl/cpu/torch_stable.html
```

---

## 🎯 **Recomendação**

**Para iniciantes:** Use **Streamlit Cloud** ⚡
**Para produção:** Use **Railway** ou **Google Cloud Run** 🚀
**Para desenvolvimento:** Use **Docker** local 🐳

---

## 📞 **Suporte**

- 🐛 **Issues:** [GitHub Issues](https://github.com/seu-usuario/InfluScore-Streamlit/issues)
- 💬 **Discord:** [Link do Discord]
- 📧 **Email:** suporte@influscore.com

---

⚡ **Deploy em menos de 1 minuto!** ⚡

