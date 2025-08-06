
# LLM Document Processing System

Build a system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

---

## 🚀 Objective

The system should take an input query like:

> **"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"**

It must then:

- Parse and structure the query to identify key details such as **age**, **procedure**, **location**, and **policy duration**.
- Search and retrieve relevant clauses or rules from the provided documents using **semantic understanding** rather than simple keyword matching.
- Evaluate the retrieved information to determine the correct decision, such as **approval status** or **payout amount**, based on the logic defined in the clauses.
- Return a structured JSON response containing:
  - `decision` (e.g., approved or rejected)
  - `amount` (if applicable)
  - `justification`, including mapping of each decision to the specific clause(s) it was based on.

---

## 📄 Requirements

- Input documents may include **PDFs**, **Word files**, or **emails**.
- The query processing and retrieval must work even if the query is **vague**, **incomplete**, or written in **plain English**.
- The system must be able to **explain its decision** by referencing the **exact clauses** used from the source documents.
- The output should be:
  - Consistent
  - Interpretable
  - Usable for downstream applications such as **claim processing** or **audit tracking**.

---

## 🔧 Architecture Overview

### 🏗 Hosting Platform

Use a **free PaaS** with automatic HTTPS:

- **Render** – one-click Git deploy, built-in SSL, free tier available.
- **Fly.io** – up to 3 free small VMs, low-latency global deployment.
- **Koyeb** – serverless, 512MB RAM & free PostgreSQL without a credit card.

🛑 _Note_: Heroku and Railway no longer offer free tiers.

### 🔍 Semantic Search (Vector Store)

- **FAISS** (Local, Open Source) – great for on-device, zero-cost use.
- **Pinecone** (Managed) – free tier supports ~100K vectors (1536-d), easy to use via API.

Choose:
- **FAISS** for full control and simplicity.
- **Pinecone** for hassle-free, hosted service.

### 🧠 LLM Model Choice

Use **open-source chat models** to avoid paid APIs:

- **Llama 2 (Meta)** – available via HuggingFace or local run.
- **Mistral 7B / Zephyr 7B** – high-quality Apache/MIT licensed models.

Run via:
```python
from transformers import pipeline
```
Use HuggingFace Inference API if local hardware is limited.

### 📄 PDF Ingestion & Embedding

- Use `PyMuPDF`, `pdfplumber`, or `PyPDF2` to extract text.
- Split text using `LangChain`’s `RecursiveCharacterTextSplitter`.
- Embed with `"sentence-transformers/all-MiniLM-L6-v2"` for fast inference (384-d vector).

Ingest once per PDF:
1. Extract text
2. Chunk and embed
3. Store in FAISS/Pinecone

At query time:
- Embed question
- Search nearest neighbors
- Pass relevant chunks to LLM

### 🚀 Deployment (Docker vs Simple)

Prefer **plain Python app deployment**:
- For **Render**, define `requirements.txt` + start command (e.g. `gunicorn main:app`).
- Avoid Docker unless necessary.

### 🔐 API Key Authentication

Secure API using Bearer token:

```python
auth = request.headers.get('Authorization')  # e.g. "Bearer XYZ"
if not auth or not auth.startswith("Bearer "):
    return "Unauthorized", 401

token = auth.split()[1]
if token != EXPECTED_TOKEN:
    return "Unauthorized", 401
```

---

## 💡 Sample Query

> **"46M, knee surgery, Pune, 3-month policy"**

### ✅ Sample Response (JSON)

```json
{
  "decision": "Approved",
  "amount": "₹85,000",
  "justification": "Clause 7.2 confirms knee surgery is covered under 3-month-old active policies. Location and age criteria matched."
}
```

---

## 🧠 Applications

- Insurance claim validation
- Legal document review
- HR policy checks
- Contract obligation detection

---

## 🧾 Sources & References

- [Render.com](https://render.com)
- [Fly.io](https://fly.io)
- [Koyeb.com](https://www.koyeb.com)
- [Pinecone.io](https://www.pinecone.io)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [LangChain Text Splitters](https://docs.langchain.com/docs/components/text-splitters/)
- [Sentence Transformers](https://www.sbert.net/)
