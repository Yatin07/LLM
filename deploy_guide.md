# Deployment Guide - HackRx LLM API

## 🚀 Quick Deployment Options

### Option 1: Render (Recommended - Free Tier)
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `hackrx-llm-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn hackrx_api:app`
   - **Plan**: Free

### Option 2: Railway (Recommended - Free Tier)
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy

### Option 3: Heroku (Free Tier Discontinued)
1. Install Heroku CLI
2. Run commands:
```bash
heroku create hackrx-llm-api
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 4: Vercel (Serverless)
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure as Python project
4. Deploy

## 📋 Pre-Deployment Checklist

### ✅ Files Ready
- [x] `hackrx_api.py` - Main API
- [x] `requirements.txt` - Dependencies
- [x] `Procfile` - Heroku/Render
- [x] `runtime.txt` - Python version
- [x] `app.py` - Alternative entry point

### ✅ Code Ready
- [x] All tests passing
- [x] Response format correct
- [x] Error handling robust
- [x] Authentication working

## 🎯 Deployment Steps

### Step 1: Choose Platform
**Recommended**: Render.com (easiest, free tier available)

### Step 2: Prepare Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 3: Deploy to Render

1. **Create Account**: Sign up at [render.com](https://render.com)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service**:
   - **Name**: `hackrx-llm-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn hackrx_api:app`
   - **Plan**: Free

4. **Environment Variables** (Optional):
   - `API_TOKEN`: `8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21`

5. **Deploy**: Click "Create Web Service"

### Step 4: Get Your URL
After deployment, you'll get a URL like:
```
https://hackrx-llm-api.onrender.com
```

Your API endpoint will be:
```
https://hackrx-llm-api.onrender.com/api/v1/hackrx/run
```

## 🧪 Test Deployment

### Test Health Endpoint
```bash
curl https://your-app-name.onrender.com/api/v1/health
```

### Test Main Endpoint
```bash
curl -X POST https://your-app-name.onrender.com/api/v1/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 🎯 Submit to HackRx

### Final Submission URL
Once deployed, your submission URL will be:
```
https://your-app-name.onrender.com/api/v1/hackrx/run
```

### Submission Steps
1. Go to HackRx competition page
2. Click "Submit"
3. Enter your webhook URL: `https://your-app-name.onrender.com/api/v1/hackrx/run`
4. Add description: "Flask + FAISS + Sentence Transformers + LLM"
5. Click "Run" to test

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check `requirements.txt` is complete
   - Ensure Python version in `runtime.txt`

2. **App Crashes**:
   - Check logs in deployment platform
   - Verify `gunicorn hackrx_api:app` command

3. **Timeout Issues**:
   - Render free tier has 30s timeout
   - Consider upgrading to paid plan

4. **Memory Issues**:
   - Model loading might be slow
   - Consider model optimization

### Debug Commands
```bash
# Check if app runs locally
python hackrx_api.py

# Test with curl
curl http://localhost:8000/api/v1/health

# Check requirements
pip install -r requirements.txt
```

## 🚀 Success Indicators

✅ **Deployment Successful** when:
- Build completes without errors
- Health endpoint returns 200
- Main API endpoint responds correctly
- HTTPS is enabled automatically

✅ **Ready for Submission** when:
- All tests pass on deployed URL
- Response format matches specification
- Authentication works
- Performance under 30 seconds

## 🎯 Next Steps

1. **Deploy** to chosen platform
2. **Test** the deployed URL
3. **Submit** to HackRx competition
4. **Monitor** performance and logs

**Your system is ready for deployment!** 🚀 