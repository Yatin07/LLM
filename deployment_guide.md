# 🚀 Deployment Guide

## Deploy Your LLM Document Processing System to the Cloud

### 🌐 **Option 1: Render.com (Recommended)**

1. **Create Render Account**: Go to https://render.com
2. **Connect GitHub**: Connect your repository
3. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
   - Environment Variables:
     ```
     API_TOKEN=your-secure-token-here
     MODEL_NAME=gpt2
     PORT=10000
     ```

4. **Deploy**: Click "Create Web Service"
5. **Access**: Your app will be live at `https://your-app-name.onrender.com`

### 🚁 **Option 2: Fly.io**

1. **Install Fly CLI**: https://fly.io/docs/getting-started/installing-flyctl/
2. **Login**: `fly auth login`
3. **Initialize**: `fly launch`
4. **Configure fly.toml**:
   ```toml
   [env]
     PORT = "8080"
     API_TOKEN = "your-secure-token"
     MODEL_NAME = "gpt2"
   ```
5. **Deploy**: `fly deploy`

### 🛸 **Option 3: Koyeb**

1. **Create Account**: https://www.koyeb.com
2. **Connect GitHub**
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn main:app --bind 0.0.0.0:$PORT`
   - Environment Variables: Same as Render

### 🐳 **Option 4: Docker + Any Cloud**

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
```

Build and deploy:
```bash
docker build -t llm-processor .
docker run -p 8000:8000 llm-processor
```

### 🔐 **Security for Production**

1. **Change API Token**:
   ```bash
   # Generate secure token
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set Environment Variables**:
   ```
   API_TOKEN=your-super-secure-token
   FLASK_ENV=production
   MODEL_NAME=gpt2  # or larger model if available
   ```

3. **HTTPS**: All platforms provide HTTPS automatically

### 📊 **Post-Deployment Testing**

```bash
# Replace with your deployed URL
DEPLOYED_URL="https://your-app.onrender.com"

# Test health
curl ${DEPLOYED_URL}/health

# Test upload (with your secure token)
curl -X POST \
  -H "Authorization: Bearer your-secure-token" \
  -F "file=@document.pdf" \
  ${DEPLOYED_URL}/upload

# Test query
curl -X POST \
  -H "Authorization: Bearer your-secure-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "insurance coverage question"}' \
  ${DEPLOYED_URL}/query
```

### 💡 **Tips for Production**

1. **Model Choice**:
   - CPU: Use `gpt2` (smaller, faster)
   - GPU: Use `microsoft/DialoGPT-medium` or larger

2. **Scaling**:
   - Enable auto-scaling on your platform
   - Consider caching for frequent queries

3. **Monitoring**:
   - Check logs for errors
   - Monitor response times
   - Set up health check alerts

4. **Costs**:
   - Render: Free tier available
   - Fly.io: Free allowance
   - Koyeb: Free tier with limitations

Your app will be accessible worldwide once deployed! 🌍