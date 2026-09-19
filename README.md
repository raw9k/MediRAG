# 🩺 MediRAG --- Medical Question Answering with Retrieval-Augmented Generation

```{=html}
<p align="center">
```
**A production-oriented medical RAG application built with FastAPI,
FAISS, Hugging Face embeddings, and Groq LLMs.**

```{=html}
</p>
```
```{=html}
<p align="center">
```
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-0467DF)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM_Inference-F55036)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple)
![Tests](https://img.shields.io/badge/Tests-Pytest-green)

```{=html}
</p>
```

------------------------------------------------------------------------

## ✨ Overview

**MediRAG** is a medical question-answering system that combines
**retrieval-augmented generation (RAG)** with a curated medical
knowledge source.

Instead of asking an LLM to answer a medical question entirely from its
pretrained knowledge, MediRAG first searches a local vector database
built from **The Gale Encyclopedia of Medicine, Second Edition**,
retrieves relevant passages, and then provides those passages to the LLM
as grounded context.

The goal is to make the system:

-   🔎 **Retrieval-grounded** --- answers are generated from retrieved
    medical passages.
-   🧠 **Conversational** --- follow-up questions can use conversation
    history.
-   🛡️ **Safety-aware** --- the system avoids diagnosis and unsupported
    medical claims.
-   📚 **Source-aware** --- answers expose the encyclopedia pages used
    for retrieval.
-   🚀 **API-first** --- the complete application is exposed through
    FastAPI.
-   🐳 **Portable** --- the application and vector index can run inside
    Docker.
-   🧪 **Testable** --- ingestion, retrieval, rewriting, API behavior,
    and evaluation are covered by automated tests.

> **Medical disclaimer:** MediRAG is an educational information system.
> It is not a substitute for professional medical advice, diagnosis, or
> treatment.

------------------------------------------------------------------------

# 🎯 Why RAG?

A conventional LLM workflow looks like:

``` text
User Question
      │
      ▼
    LLM
      │
      ▼
   Answer
```

This creates an important problem for medical applications: the model's
response is not necessarily tied to a specific knowledge source.

MediRAG introduces a retrieval layer:

``` text
                  ┌─────────────────────┐
                  │    Medical Source   │
                  │  Gale Encyclopedia  │
                  └──────────┬──────────┘
                             │
                       PDF ingestion
                             │
                             ▼
                    ┌─────────────────┐
                    │ Chunking +      │
                    │ Embeddings      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      FAISS      │
                    │  Vector Index   │
                    └────────┬────────┘
                             │
                             │ similarity search
                             ▼
User ──► Question ──► Retrieval ──► Context ──► Groq LLM
                                               │
                                               ▼
                                      Grounded Answer
                                               │
                                               ▼
                                      Sources + Disclaimer
```

The central design principle is:

> **Retrieve first, generate second.**

------------------------------------------------------------------------

# 🧠 System Architecture

``` mermaid
flowchart TD
    U[👤 User] --> UI[🌐 Web Chat Interface]

    UI --> API[⚡ FastAPI /ask]

    API --> INTENT[🎯 Intent Detection]
    INTENT -->|Greeting| GREET[💬 Greeting Response]
    INTENT -->|Medical Query| REWRITE[🔄 Query Rewriter]

    REWRITE --> EMB[🧩 Sentence Transformer]
    EMB --> FAISS[(🗂️ FAISS Vector Store)]

    FAISS --> RET[📄 Retrieved Documents]
    RET --> CTX[📚 Context Builder]

    CTX --> LLM[🤖 Groq LLM<br/>GPT-OSS-20B]

    LLM --> SAFE[🛡️ Safety + Grounding Rules]
    SAFE --> RESP[💬 Answer + Sources]

    RESP --> UI
```

------------------------------------------------------------------------

# 🔬 RAG Pipeline

MediRAG processes a question through several stages.

## 1. Question

Example:

> What are the symptoms of diabetes?

## 2. Query Understanding

The system first checks whether the input is a simple greeting.

For conversational questions, the query rewriter can use previous user
messages to resolve references such as:

> What about type 2?

into a retrieval-friendly query such as:

> What about type 2 diabetes?

## 3. Embedding

The query is converted into a dense vector using:

``` text
sentence-transformers/all-MiniLM-L6-v2
```

Embedding dimension:

``` text
384
```

## 4. Similarity Search

FAISS searches the medical knowledge base for semantically similar
chunks.

The retrieval layer:

-   retrieves multiple candidates
-   applies a similarity-distance threshold
-   removes duplicate pages
-   returns a limited number of relevant documents

## 5. Context Construction

Retrieved passages are formatted with source identifiers and
human-readable page numbers:

``` text
SOURCE 1
Page: 437
----------------------------------------
Symptoms of diabetes can develop suddenly...
```

## 6. Generation

The retrieved context is passed to:

``` text
Groq
└── openai/gpt-oss-20b
```

The model is explicitly instructed to:

-   use only supplied medical context
-   avoid diagnosis
-   avoid unsupported medical claims
-   avoid prescribing treatment beyond the supplied context
-   acknowledge insufficient context
-   recommend professional medical care for potentially serious symptoms

## 7. Response

The final response contains:

``` text
Answer
+
Medical disclaimer
+
Retrieved source pages
```

------------------------------------------------------------------------

# 📚 Knowledge Base

The current knowledge source is:

**The Gale Encyclopedia of Medicine, Second Edition**

The ingestion pipeline processes:

``` text
759 pages
      ↓
7,079 chunks
```

The generated FAISS store contains:

``` text
vectorstore/
├── index.faiss
└── index.pkl
```

The source PDF is used during index construction but is not required by
the running RAG application once the vector index has been created.

------------------------------------------------------------------------

# 🧩 Project Structure

``` text
MediRAG/
│
├── app/
│   ├── api/
│   │   └── main.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── frontend/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   └── test_pipeline.py
│   │
│   ├── llm/
│   │   └── groq.py
│   │
│   ├── rag/
│   │   ├── pipeline.py
│   │   ├── intent.py
│   │   └── query_rewriter.py
│   │
│   └── vectorstore/
│       ├── build_index.py
│       ├── faiss_store.py
│       └── test_retrieval.py
│
├── data/
│   └── raw/
│       └── The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf
│
├── evaluation/
│   └── test_cases.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_api.py
│   ├── test_query_rewriter.py
│   └── test_evaluation.py
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

------------------------------------------------------------------------

# 🛠️ Tech Stack

  Layer                Technology                 Purpose
  -------------------- -------------------------- ---------------------------------
  Language             Python 3.11                Application development
  API                  FastAPI                    REST API
  Server               Uvicorn                    ASGI application server
  PDF ingestion        PyPDFLoader                Medical document loading
  Chunking             LangChain text splitters   Document segmentation
  Embeddings           all-MiniLM-L6-v2           Semantic representation
  Vector database      FAISS                      Similarity search
  LLM                  Groq / GPT-OSS-20B         Response generation
  Validation           Pydantic                   API request/response validation
  Frontend             HTML/CSS/JavaScript        Chat interface
  Markdown rendering   Marked                     Rich assistant responses
  Sanitization         DOMPurify                  Safe rendered HTML
  Testing              Pytest                     Automated validation
  Packaging            Docker                     Reproducible deployment
  Deployment           Render                     Cloud hosting

------------------------------------------------------------------------

# 🔄 Conversational Query Rewriting

MediRAG supports simple conversational references.

For example:

``` text
User:
What are the symptoms of diabetes?

MediRAG:
...

User:
What about type 2?
```

A naive vector search would receive:

``` text
What about type 2?
```

which contains very little medical context.

MediRAG uses conversation history to produce a more useful retrieval
query:

``` text
What about type 2 diabetes?
```

The rewritten query is used for retrieval, while the original user
question is preserved for final answer generation.

This separation is important:

``` text
Conversation
     │
     ▼
Query Rewriting
     │
     ▼
Retrieval Query
     │
     ▼
Relevant Context
     │
     ▼
Original Question + Context
     │
     ▼
LLM
```

------------------------------------------------------------------------

# 🎯 Retrieval Strategy

The retrieval layer does more than simply take the first `k` FAISS
results.

Current strategy:

``` text
Question
   │
   ▼
Retrieve candidate documents
   │
   ▼
Similarity-distance threshold
   │
   ▼
Remove duplicate pages
   │
   ▼
Return up to k documents
```

The current default configuration uses:

``` text
k = 3
candidate_k = max(k × 3, 10)
score_threshold = 0.85
```

FAISS similarity distance is interpreted so that **lower distance
indicates greater similarity**.

The page-level deduplication prevents several nearly identical chunks
from the same page from consuming the entire retrieval budget.

------------------------------------------------------------------------

# 🛡️ Medical Safety Design

Medical question answering requires a different approach from a general
chatbot.

MediRAG includes several safeguards.

### Grounding

The LLM is instructed to use only the retrieved context.

### No diagnosis

The system does not diagnose the user.

### No unsupported treatment recommendations

The system does not invent treatments or medications outside the
retrieved material.

### Insufficient context handling

When retrieval does not provide enough information, the system returns:

``` text
The available medical context does not provide enough
information to answer this question.
```

### Serious symptoms

Potentially serious symptoms are handled conservatively and the user is
directed toward professional medical care rather than receiving a
diagnosis.

### Sources

Retrieved pages are returned with the answer so the user can understand
where the information came from.

------------------------------------------------------------------------

# 🌐 API

MediRAG exposes a FastAPI interface.

## `GET /`

Returns the main MediRAG chat interface.

## `GET /chat`

Alias for the chat interface.

## `GET /docs`

Opens the interactive Swagger UI.

## `GET /health`

Health check endpoint.

Example response:

``` json
{
  "status": "healthy"
}
```

## `POST /ask`

Main RAG endpoint.

Example request:

``` json
{
  "question": "What are the symptoms of diabetes?",
  "history": []
}
```

Example response structure:

``` json
{
  "answer": "....",
  "sources": [
    "The Gale Encyclopedia of Medicine — Page 437",
    "The Gale Encyclopedia of Medicine — Page 436"
  ]
}
```

The API also accepts conversation history:

``` json
{
  "question": "What about type 2?",
  "history": [
    {
      "role": "user",
      "content": "What are the symptoms of diabetes?"
    },
    {
      "role": "assistant",
      "content": "..."
    }
  ]
}
```

------------------------------------------------------------------------

# 💻 Running Locally

## 1. Clone the repository

``` bash
git clone <your-repository-url>
cd MediRAG
```

## 2. Create an environment

``` bash
conda create -n medibot python=3.11
conda activate medibot
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

``` text
.env
```

with:

``` env
GROQ_API_KEY=your_groq_api_key
```

Never commit `.env` to Git.

## 5. Build the vector store

If the FAISS index needs to be regenerated:

``` bash
python -m app.vectorstore.build_index
```

This creates:

``` text
vectorstore/
├── index.faiss
└── index.pkl
```

## 6. Start the API

``` bash
uvicorn app.api.main:app --reload
```

Open:

``` text
http://127.0.0.1:8000/
```

Swagger:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🐳 Docker

MediRAG is containerized so the application can run with the same core
environment across development and deployment.

## Build

``` bash
docker build -t meditrag .
```

## Run

``` bash
docker run --env-file .env -p 8000:10000 meditrag
```

Then open:

``` text
http://localhost:8000/
```

The container contains:

``` text
Python runtime
      +
Python dependencies
      +
MediRAG application
      +
FAISS index
```

The original medical PDF is excluded from the Docker build because it is
not required at runtime after vector-store construction.

------------------------------------------------------------------------

# ☁️ Deployment Architecture

The intended deployment workflow is:

``` mermaid
flowchart LR
    DEV[💻 Local Development] --> GIT[GitHub]
    GIT --> RENDER[☁️ Render]
    RENDER --> DOCKER[🐳 Docker Build]
    DOCKER --> APP[🚀 MediRAG Service]

    APP --> FAISS[(FAISS)]
    APP --> GROQ[Groq API]
```

Deployment flow:

``` text
Code change
    ↓
git add
    ↓
git commit
    ↓
git push
    ↓
GitHub
    ↓
Render detects change
    ↓
Docker image rebuild
    ↓
Container starts
    ↓
MediRAG available online
```

The Groq API key should be configured as a deployment environment
variable rather than stored in source code.

------------------------------------------------------------------------

# 🧪 Testing

The project uses `pytest` for automated validation.

The test suite covers areas including:

``` text
                 ┌──────────────────────┐
                 │     Test Suite       │
                 └──────────┬───────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
  Ingestion             Retrieval              API
       │                    │                    │
       ▼                    ▼                    ▼
  Query Rewriting      Evaluation          Safety Checks
```

Run all tests:

``` bash
python -m pytest -v
```

The project has been validated with the RAG pipeline, retrieval
behavior, API validation, conversational query rewriting, and
safety-oriented cases.

------------------------------------------------------------------------

# 📊 Evaluation & Retrieval Notes

The evaluation suite is designed around realistic question-answering
scenarios rather than simply checking whether an API returns HTTP 200.

Examples include:

-   medical questions with relevant context
-   greetings
-   conversational follow-ups
-   insufficient-context questions
-   safety-sensitive questions
-   source-return behavior
-   retrieval relevance

An important engineering lesson from the retrieval evaluation was that
**not every medical topic is equally well represented by the current
vector search configuration**.

For example, some diabetes queries retrieved highly relevant pages,
while some asthma queries produced weak semantic matches.

Rather than artificially treating weak retrieval as a successful answer,
those cases are treated as a retrieval-quality limitation to improve in
future iterations.

This distinction matters in RAG systems:

``` text
Good generation
      ≠
Good RAG

Good RAG
      =
Good retrieval
+
Good context construction
+
Grounded generation
```

------------------------------------------------------------------------

# ⚡ Performance Considerations

MediRAG separates expensive initialization from per-request operations
where practical.

The application loads the embedding model and FAISS store for reuse
rather than rebuilding them for every request.

Conceptually:

``` text
Application Startup
        │
        ├── Load embedding model
        └── Load FAISS index
                 │
                 ▼
          Ready for requests
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Query 1   Query 2   Query 3
       │         │         │
       └─────────┼─────────┘
                 ▼
          Reused resources
```

This avoids repeatedly loading large ML resources during normal request
handling.

------------------------------------------------------------------------

# 🎨 Frontend Features

The web interface is designed as a dedicated medical AI chat experience
rather than a raw API wrapper.

Current UX features include:

-   🩺 MediRAG branding
-   💬 Chat-based interface
-   ✨ Welcome state
-   💡 Suggested medical questions
-   ⌨️ Enter-to-send interaction
-   ↩️ Shift+Enter for multiline input
-   ⏳ Loading animation
-   📚 Retrieved source cards
-   📋 Copy-answer interaction
-   🧹 Clear conversation
-   🌙 Dark/light theme
-   📱 Responsive mobile layout
-   🔗 Direct Swagger/API Docs button
-   🔄 Conversation history

------------------------------------------------------------------------

# 🧱 Design Decisions

## Why FAISS?

FAISS provides efficient local vector similarity search without
requiring an external vector database.

For a single-document medical knowledge base, it keeps the architecture
lightweight:

``` text
PDF
 ↓
Embeddings
 ↓
FAISS
 ↓
FastAPI
```

## Why local embeddings?

`all-MiniLM-L6-v2` provides compact 384-dimensional embeddings suitable
for semantic retrieval while keeping the application relatively
lightweight.

## Why Groq?

Groq provides fast LLM inference through an OpenAI-compatible API
interface.

The application therefore keeps LLM interaction isolated inside:

``` text
app/llm/groq.py
```

which makes the generation layer easier to replace later.

## Why FastAPI?

FastAPI provides:

-   typed request/response models
-   automatic OpenAPI generation
-   Swagger UI
-   validation
-   lightweight ASGI serving

This also makes the same backend useful for both the web interface and
external clients.

------------------------------------------------------------------------

# 🔐 Security & Privacy Notes

The project follows several basic security practices:

-   API keys are stored in environment variables.
-   `.env` is excluded from Git.
-   Secrets are not embedded in frontend JavaScript.
-   Retrieved model context is separated from application secrets.
-   Render deployment should use environment variables for production
    secrets.
-   User input is validated through Pydantic models.
-   Rendered Markdown is sanitized on the frontend using DOMPurify.

MediRAG should not be used as a substitute for professional medical
care.

------------------------------------------------------------------------

# 🚧 Current Limitations

MediRAG is intentionally an evolving RAG system.

Current limitations include:

### Retrieval quality

Semantic retrieval quality varies across medical topics. Some topics are
represented more effectively than others.

### Single primary knowledge source

The current knowledge base is based on one medical encyclopedia.

### No medical knowledge verification layer

The system does not independently verify retrieved claims against
multiple medical sources.

### No clinical decision support

The application is designed for educational information retrieval, not
clinical diagnosis or treatment decisions.

### Fixed retrieval configuration

The current retrieval layer uses a fixed similarity threshold and
retrieval budget. Future work could investigate adaptive retrieval.

------------------------------------------------------------------------

# 🚀 Future Improvements

Potential next iterations include:

## Retrieval

-   Hybrid BM25 + vector search
-   Cross-encoder reranking
-   Query expansion
-   Adaptive retrieval thresholds
-   Metadata-aware filtering
-   Better chunking strategies
-   Parent-document retrieval

## RAG

-   Context compression
-   Multi-query retrieval
-   Retrieval confidence scoring
-   Citation-aware generation
-   Answer faithfulness evaluation

## Evaluation

-   Retrieval Recall@K
-   Precision@K
-   MRR
-   nDCG
-   Answer faithfulness
-   Context relevance
-   Answer relevance
-   Automated RAG evaluation

## Medical safety

-   More granular safety intent detection
-   Emergency symptom routing
-   Stronger unsupported-claim detection
-   Source confidence indicators
-   Human-reviewed evaluation sets

## Infrastructure

-   CI/CD with GitHub Actions
-   Container image optimization
-   Persistent external vector storage
-   Observability and structured logging
-   Rate limiting
-   Authentication
-   Production monitoring

------------------------------------------------------------------------

# 🗺️ Development Roadmap

``` text
                    MediRAG Roadmap

                    ┌──────────────┐
                    │ PDF Ingestion│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Chunking    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Embeddings  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    FAISS     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ RAG Pipeline │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Safety       Rewriting       Sources
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Frontend   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Docker    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Render    │
                    └──────────────┘
```

------------------------------------------------------------------------

# 💡 What This Project Demonstrates

MediRAG is more than a chatbot UI. It demonstrates an end-to-end machine
learning engineering workflow:

``` text
📄 Data
 ↓
🔪 Processing
 ↓
🧩 Embeddings
 ↓
🗂️ Vector Search
 ↓
🔎 Retrieval
 ↓
🧠 Query Rewriting
 ↓
📚 Context Construction
 ↓
🤖 LLM Generation
 ↓
🛡️ Safety Controls
 ↓
⚡ API
 ↓
🌐 Frontend
 ↓
🐳 Docker
 ↓
☁️ Deployment
 ↓
🧪 Testing
```

This makes the project a practical demonstration of:

**RAG + NLP + Vector Search + LLMs + API Engineering + Frontend
Development + Docker + Cloud Deployment + Testing**

------------------------------------------------------------------------

# 📜 License & Source Attribution

The application code is a personal engineering project.

The medical knowledge base is derived from **The Gale Encyclopedia of
Medicine, Second Edition**. The source material is used as the knowledge
source for the RAG pipeline; users should ensure that their use and
redistribution of source material complies with the applicable copyright
and licensing terms.

------------------------------------------------------------------------

# 👨‍💻 Author

**Rounak Kumar**

Integrated MSc. Quantitative Economics & Data Science\
BIT Mesra


------------------------------------------------------------------------

```{=html}
<p align="center">
```
### 🩺 MediRAG

**Retrieve → Ground → Generate → Cite**

```{=html}
</p>
```
