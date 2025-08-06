# API Testing Examples

Here are examples of how to test the LLM Document Processing System API:

## 🚀 Server URLs

**Local Development**: `http://localhost:5000`  
**Production**: `https://your-app-name.render.com` (or your deployed URL)

## 🔐 Authentication

All endpoints except `/health` require Bearer token authentication:
```
Authorization: Bearer your-api-token-here
```

Default token for testing: `default-token-change-me`

---

## 🏥 Health Check

**GET** `/health`

```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "LLM Document Processing System", 
  "version": "1.0.0"
}
```

---

## 📊 Get System Statistics

**GET** `/stats`

```bash
curl -H "Authorization: Bearer default-token-change-me" \
     http://localhost:5000/stats
```

**Expected Response:**
```json
{
  "vector_store": {
    "total_chunks": 5,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384
  },
  "llm_model": {
    "model_name": "gpt2",
    "available": true,
    "device": "cpu"
  },
  "system_status": {
    "document_processor": "available",
    "text_processor": "available",
    "llm_processor": "available"
  }
}
```

---

## 📄 Upload Document

**POST** `/upload`

```bash
curl -X POST \
  -H "Authorization: Bearer default-token-change-me" \
  -F "file=@your-document.pdf" \
  http://localhost:5000/upload
```

**Expected Response:**
```json
{
  "message": "Document processed and indexed successfully",
  "filename": "your-document.pdf",
  "status": "indexed",
  "metadata": {
    "pages": 3,
    "method": "PyMuPDF"
  },
  "stats": {
    "words": 1250,
    "characters": 7500
  },
  "vector_store": {
    "chunks_added": 4,
    "total_chunks": 4,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
  }
}
```

---

## 🔍 Process Query

**POST** `/query`

```bash
curl -X POST \
  -H "Authorization: Bearer default-token-change-me" \
  -H "Content-Type: application/json" \
  -d '{"query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"}' \
  http://localhost:5000/query
```

**Expected Response:**
```json
{
  "decision": "Approved",
  "amount": "₹85,000",
  "justification": "Based on policy analysis, knee surgery is covered for eligible age group. Coverage includes Pune location. Policy active for sufficient duration.",
  "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
  "relevant_chunks": 3,
  "sources": [
    {
      "source": "policy.pdf",
      "chunk_id": 1, 
      "similarity_score": 0.742
    }
  ],
  "analysis_method": "LLM-based",
  "llm_model": "gpt2"
}
```

---

## 🧪 Testing with Python

Use the provided `test_api.py` script:

```bash
# Make sure the server is running first
python main.py

# In another terminal, run the tests
python test_api.py
```

---

## 🌐 Testing with Postman

1. **Import Environment**:
   - Base URL: `http://localhost:5000`
   - Token: `default-token-change-me`

2. **Create Collection** with these requests:
   - GET Health Check
   - GET Stats (with Bearer token)
   - POST Upload (with Bearer token + file)
   - POST Query (with Bearer token + JSON body)

---

## 🔧 Browser Testing

For simple GET endpoints, you can test directly in browser:

- Health: http://localhost:5000/health
- Stats: Need authentication (use curl or Postman)

---

## 📱 Sample Test Files

Create these files for testing uploads:

**sample_policy.txt:**
```
Health Insurance Policy

Coverage:
- Age: 18-65 years
- Knee surgery: ₹85,000
- Emergency: Day 1 coverage
- Location: Pan India including Pune

Exclusions:
- Cosmetic surgery
- Dental (except accidental)
```

**test_queries.json:**
```json
[
  "46-year-old male, knee surgery in Pune, 3-month-old policy",
  "Emergency heart surgery coverage",
  "Dental accident coverage",
  "Age eligibility requirements"
]
```