# ⚖️ CourtVision AI — Commercial Courts Intelligence Platform

An AI-powered legal research engine for commercial courts built with **Django**, **LangGraph**, **FAISS**, and **Groq API**.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Django 4.2 |
| AI Orchestration | LangGraph (state machine workflows) |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| LLM | Groq API — LLaMA 3 (8B, 70B) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Frontend | Bootstrap 5 + Custom Design System |
| Auth | Django built-in + Custom UserProfile |

---

## ✨ Features

### 🔐 User Authentication
- Register/Login with role-based profiles (Judge, Lawyer, Clerk, Researcher, Admin)
- Bar number, court affiliation, and contact info storage
- Session-based authentication with secure logout

### 📁 Document Management
- Upload PDF, TXT, DOC, DOCX files (up to 10MB)
- Drag-and-drop file upload interface
- Document metadata: case number, court name, filing date, document type
- Download original files

### 🤖 AI Document Analysis (LangGraph Pipeline)
1. **Text Extraction** — pdfplumber / PyPDF2 for PDFs
2. **Vector Indexing** — FAISS index with sentence-transformer embeddings
3. **Summarization Node** — Structured legal summary via Groq/LLaMA 3
4. **Key Findings Node** — JSON-structured legal findings extraction
5. **Query Node** — Retrieval-augmented answers using FAISS + LLM

### 🔍 Research Interface
- Natural language legal queries against uploaded documents
- FAISS semantic search retrieves relevant passages
- LangGraph routes query through context retrieval → LLM answer
- Query history per document and globally
- Suggested query prompts for common legal research needs

---

## 🚀 Quick Start

### 1. Clone / Extract the project
```bash
cd court_research
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your-secure-secret-key-here
DEBUG=True
GROQ_API_KEY=your-groq-api-key-here    # Get from console.groq.com
```

> **Get your free Groq API key at:** https://console.groq.com

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
court_research/
├── court_research/          # Django project config
│   ├── settings.py          # All settings + FAISS path config
│   └── urls.py              # Root URL routing
│
├── authentication/          # User auth app
│   ├── models.py            # UserProfile (role, bar number, affiliation)
│   ├── views.py             # Login, register, logout, profile
│   └── forms.py             # Auth forms with validation
│
├── documents/               # Document management app
│   ├── models.py            # Document + ResearchQuery models
│   ├── views.py             # Upload, list, detail, delete, status poll
│   └── forms.py             # Document upload form
│
├── research/                # AI research app
│   ├── ai_engine.py         # ⭐ Core AI engine:
│   │                        #    - Text extraction (pdfplumber/PyPDF2)
│   │                        #    - FAISS vector store creation/search
│   │                        #    - LangGraph workflow nodes
│   │                        #    - Groq API integration
│   └── views.py             # Research interface + query submission
│
├── templates/               # All HTML templates
│   ├── base.html            # Navy/gold design system base
│   ├── authentication/      # Login, register pages
│   ├── documents/           # List, upload, detail, delete templates
│   └── research/            # Query interface, history
│
├── media/                   # Uploaded files (auto-created)
├── vector_stores/           # FAISS indexes (auto-created)
└── requirements.txt
```

---

## 🧠 LangGraph AI Pipeline

```
Document Upload
     │
     ▼
[Text Extraction] ──── pdfplumber / PyPDF2 / plain text
     │
     ▼
[FAISS Indexing] ────── sentence-transformers embeddings
     │                  stored per-document in vector_stores/
     ▼
[LangGraph Workflow]
     │
     ├──► [summarize node] ─── Groq LLaMA 3 → structured legal summary
     │
     └──► [extract_findings node] ─── Groq → JSON key findings
               │
               └── if query present:
                   [answer_query node] ─── FAISS retrieval + Groq → answer
```

---

## 🔑 Default Demo Account

After setup, a default admin account is available:
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ Change this immediately in production!

---

## 🌐 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Redirects to documents list |
| `/auth/login/` | Login page |
| `/auth/register/` | Registration page |
| `/documents/` | Document library |
| `/documents/upload/` | Upload new document |
| `/documents/<id>/` | Document detail + AI summary |
| `/research/document/<id>/` | Research query interface |
| `/research/history/` | All research history |
| `/admin/` | Django admin panel |

---

## ⚙️ Configuration

### Groq Models
In `research/ai_engine.py`, change the model in `call_groq()`:
```python
model="llama3-8b-8192"      # Fast, efficient
model="llama3-70b-8192"     # More powerful (if available on your plan)
model="mixtral-8x7b-32768"  # Long context
```

### FAISS Chunk Settings
Adjust in `research/ai_engine.py`:
```python
chunk_size=1000    # Words per chunk
overlap=200        # Word overlap between chunks
top_k=5           # Number of chunks to retrieve per query
```

---

## 📝 License

Built for commercial court legal research. For production use, ensure compliance with your jurisdiction's data privacy regulations (DPDP Act in India, GDPR in EU, etc.) when handling case documents.
