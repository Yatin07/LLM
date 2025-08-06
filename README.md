# LLM Document Processing System

A system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp env.example .env
# Edit .env with your configuration
```

### 2. Run the Application

```bash
# Development mode
python main.py

# Production mode (using gunicorn)
gunicorn main:app --bind 0.0.0.0:5000
```

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Upload a document (requires Bearer token)
curl -X POST \
  -H "Authorization: Bearer your-api-token" \
  -F "file=@document.pdf" \
  http://localhost:5000/upload

# Query documents
curl -X POST \
  -H "Authorization: Bearer your-api-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"}' \
  http://localhost:5000/query
```

## Features

- ✅ PDF, Word, and text file processing
- ✅ Semantic search using vector embeddings  
- ✅ LLM-powered query understanding and response generation
- ✅ Open-source LLM integration (GPT-2, Mistral, Llama 2)
- ✅ Intelligent fallback to rule-based analysis
- ✅ RESTful API with Bearer token authentication
- ✅ Structured JSON responses with justifications
- ✅ Ready for deployment on Render, Fly.io, or Koyeb

## API Endpoints

### `GET /health`
Health check endpoint.

### `POST /upload`
Upload and index a document.
- **Headers**: `Authorization: Bearer <token>`
- **Body**: Form data with `file` field
- **Supported formats**: PDF, DOCX, TXT

### `POST /query`
Process a natural language query using LLM analysis.
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Body**: `{"query": "your natural language query"}`
- **Response**: 
```json
{
  "decision": "Approved",
  "amount": "₹85,000", 
  "justification": "LLM analysis indicates coverage based on policy terms...",
  "analysis_method": "LLM-based",
  "llm_model": "gpt2",
  "relevant_chunks": 3,
  "sources": [...]
}
```

### `GET /stats`
Get system statistics including vector store and LLM model information.
- **Headers**: `Authorization: Bearer <token>`

## Deployment

### Render.com
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn main:app`
4. Add environment variables

### Fly.io
1. Install Fly CLI
2. Run `fly launch`
3. Configure fly.toml
4. Deploy with `fly deploy`

## Architecture

- **Web Framework**: Flask with Bearer token authentication
- **PDF Processing**: PyMuPDF, pdfplumber, PyPDF2 (multi-fallback)
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (384-dim)
- **Vector Store**: FAISS IndexFlatIP with cosine similarity
- **LLM**: GPT-2, Mistral 7B, or Llama 2 via HuggingFace transformers
- **Fallback**: Rule-based analysis when LLM unavailable

## Configuration

See `env.example` for all available environment variables.