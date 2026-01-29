# Electronics Learning AI Platform

An agentic, PDF-grounded electronics learning platform inspired by ElectronicsLearningAI.

Students learn digital electronics through:

- An AI tutor that answers **only** from your PDFs
- A modern dashboard (XP, levels, streaks, progress)
- PDF-based study section (“Ask AI about this PDF”)
- Practice quizzes auto-generated from PDFs
- Circuit builder + simulator with AI explanations
- Agentic AI orchestration (Crio AI + Gemini 2.0 Flash + Vector DB)

All learning content comes from PDFs stored in the `kb/` folder.

---

## 1. Project Overview

### Core Principles

1. **PDF-only AI (Closed Book)**  
   - AI answers strictly from your uploaded PDFs in `kb/`.
   - If a topic is not present in the PDFs, AI must say:  
     > “This topic is not covered in your uploaded study material.”

2. **Agentic RAG Architecture**
   - **Crio AI**: Agent/orchestrator.
   - **Vector DB**: Stores PDF embeddings for semantic search.
   - **Gemini 2.0 Flash**: Reasoning + answer generation.
   - Multiple specialized agents:
     - Query Understanding
     - Retrieval
     - Reasoning / Tutor
     - Guardrail
     - Circuit Analysis

3. **Modern Learning UX**
   - Dashboard UI (XP, level, streak, charts).
   - Study section with PDFs, search, bookmarks, “Ask AI about this PDF”.
   - RAG-based AI chat.
   - Quizzes.
   - Circuit builder + simulator with AI explanations.

---

## 2. Features

### 2.1 Dashboard

- Greeting (e.g., “Good Afternoon, User”).
- Level, XP, streaks.
- Course progress by topic/category.
- Performance charts (quiz scores, XP over time).
- Recent activity (chats, quizzes, circuits).
- Achievements and badges.

### 2.2 Study / PDF Learning

- PDFs organized by category:
  - Logic Gates  
  - Flip-Flops  
  - Counters  
  - Microprocessors  
  - (Extendable)
- For each PDF:
  - Title, description, category, last opened, progress.
  - “Open PDF” viewer.
  - Search within a PDF (chunk-based).
  - Bookmark topics (store PDF page/section).
  - **“Ask AI about this PDF”**:
    - Sends question + `pdf_id` + page/section to backend.

### 2.3 AI Tutor (RAG Chat)

- Chat UI similar to modern AI apps.
- RAG pipeline:
  - Understand question.
  - Retrieve relevant PDF chunks.
  - Answer strictly from PDFs.
  - If content missing → refuse with a clear message.
- AI can:
  - Explain concepts (“Explain JK flip-flop”).
  - Solve numerical problems (within PDF context).
  - Reference material:
    - “Based on *Flip-Flops and Related Devices*, page 12…”

### 2.4 Practice Quizzes

- Quiz catalog:
  - Beginner / Intermediate / Advanced.
  - Filters by topic (Logic Gates, Flip-Flops, etc.).
- Questions:
  - Generated from PDF content (Gemini).
  - Grounded: each question linked to source chunk.
- Features:
  - Scores, retakes, XP gain.
  - Explanations referencing PDFs.

### 2.5 Circuit Lab (Circuit Maker)

- Drag & drop components:
  - Inputs: switches, clock.
  - Logic gates: AND, OR, NOT, NAND, NOR, XOR, XNOR.
  - Simple flip-flops and basic ICs (later).
  - Outputs: LEDs, probes.
- Canvas:
  - Connect wires, move components, zoom/pan.
- Simulation:
  - Run/Stop simulation.
  - Show gate output states / truth tables.
- AI integration:
  - “Explain this circuit” → AI reads circuit JSON + simulation results.
  - “Why is this output LOW here?” → analysis based on your circuit + fundamentals from PDFs.

---

## 3. Tech Stack

### Frontend

- **Framework**: Next.js (React, App Router).
- **Styling**: Tailwind CSS.
- **UI Library**: shadcn/ui.
- **Charts**: Recharts or Chart.js.
- **State Management**: Zustand.
- **Data Fetching**: React Query / TanStack Query.

### Backend

- **API**: FastAPI (Python).
- **Auth**: JWT-based authentication (Student / Admin roles).
- **Database**: PostgreSQL (via SQLAlchemy + Alembic).
- **Vector Database**:
  - Local dev: Chroma.
  - Production: Qdrant or Pinecone (configurable).

### AI & Agents

- **LLM**: Gemini 2.0 Flash (Google AI API).
- **Embeddings**: Gemini embedding model.
- **Orchestration**: Crio AI (multi-agent system).
- **Tools**:
  - PDF chunk retrieval.
  - Circuit simulation.
  - Quiz generation.

### Circuit Simulation

- **Frontend**: React-based node-editor (e.g., React Flow or custom canvas).
- **Backend**: Lightweight digital-logic simulator in Python (gates, flip-flops).

---

## 4. Project Structure

Recommended monorepo layout:

```text
.
├─ apps/
│  ├─ web/                 # Next.js frontend
│  └─ api/                 # FastAPI backend
├─ kb/                     # Knowledge base PDFs (Digital Electronics)
│  ├─ logic-gates/
│  ├─ flip-flops/
│  ├─ counters/
│  ├─ microprocessors/
│  └─ ...
├─ infra/                  # Deployment configs (Docker, CI/CD, etc.)
└─ README.md
```

### `apps/web` (Frontend)

```text
apps/web
├─ app/
│  ├─ (dashboard)/         # /dashboard
│  ├─ (auth)/              # /login, /register
│  ├─ study/               # /study
│  ├─ chat/                # /chat
│  ├─ quizzes/             # /quizzes
│  ├─ circuit-lab/         # /circuit-lab
│  └─ api/                 # optional Next.js API routes
├─ components/             # shared UI components
├─ lib/                    # helpers
├─ store/                  # Zustand stores
├─ public/
└─ tailwind.config.ts
```

### `apps/api` (Backend)

```text
apps/api
├─ src/
│  ├─ main.py              # FastAPI entrypoint
│  ├─ config.py
│  ├─ auth/                # JWT logic, dependencies
│  ├─ models/              # SQLAlchemy models
│  ├─ db/                  # session, migrations
│  ├─ routers/             # API routes (users, chat, quizzes, circuit, pdfs)
│  ├─ schemas/             # Pydantic DTOs
│  ├─ services/
│  │  ├─ rag/              # retrieval + answer generation
│  │  ├─ quiz/             # quiz generation and scoring
│  │  ├─ circuit/          # circuit simulation
│  │  └─ user/             # gamification logic
│  ├─ ai/
│  │  ├─ crio_agent.py     # Crio AI orchestrator
│  │  ├─ gemini_client.py  # Gemini API wrapper
│  │  ├─ vector_store.py   # Vector DB abstraction
│  │  └─ prompts.py        # prompt templates
│  └─ ingest/
│     ├─ pdf_loader.py     # read PDFs from kb/
│     ├─ chunker.py        # split into semantic chunks
│     └─ ingest_pdfs.py    # CLI for ingestion
└─ tests/
```

---

## 5. Data Model (High-Level)

Key relational tables:

- **users**
  - `id`, `name`, `email`, `password_hash`
  - `role` (`student`, `admin`)
  - `xp`, `level`, `streak`, `last_active_at`

- **pdfs**
  - `id`, `file_path`, `title`, `category`
  - `uploaded_by`, `uploaded_at`

- **pdf_chunks**
  - `id`, `pdf_id`, `chunk_index`
  - `content`, `page_number`, `section`, `topic`

- **chat_sessions**
  - `id`, `user_id`, `type` (`study`, `quiz`, `circuit`)
  - `created_at`

- **chat_messages**
  - `id`, `session_id`, `sender` (`user`, `ai`)
  - `content`, `metadata`, `created_at`

- **quizzes**
  - `id`, `title`, `difficulty`, `topic`, `pdf_id` (optional)

- **quiz_questions**
  - `id`, `quiz_id`
  - `question`, `options`, `correct_answer`, `source_chunk_id`

- **quiz_attempts**
  - `id`, `user_id`, `quiz_id`, `score`, `attempted_at`

- **circuit_projects**
  - `id`, `user_id`, `name`, `saved_state_json`
  - `created_at`, `updated_at`

- **achievements**, **xp_logs**
  - For gamification data.

Vector DB (Chroma / Qdrant / Pinecone) stores:

```json
{
  "id": "chunk-uuid",
  "embedding": [0.123, ...],
  "metadata": {
    "pdf_id": "flip-flops-123",
    "pdf_name": "Flip-Flops and Related Devices",
    "category": "Flip-Flops",
    "topic": "JK Flip-Flop",
    "page": 12,
    "chunk_index": 5
  },
  "content": "JK flip-flop is a refinement of the SR flip-flop where..."
}
```

---

## 6. PDF → Vector DB Pipeline

All source PDFs are placed in the `kb/` directory.

### Steps

1. **Discover PDFs**
   - Recursively scan `kb/` and subfolders.
   - Use folder name as category (e.g. `kb/flip-flops` → category = `Flip-Flops`).

2. **Parse PDFs**
   - Use a Python library (e.g., `pdfplumber`, `pymupdf`) to extract clean text.
   - Remove headers/footers where possible.

3. **Chunking**
   - Split text into semantic chunks (not fixed pages).
   - Aim for ~300–800 tokens per chunk.
   - Use headings, paragraphs, bullet lists as boundaries.

4. **Embeddings**
   - Use Gemini embedding model.
   - Create embeddings for each chunk.

5. **Store in Vector DB**
   - Upsert into Chroma/Qdrant with metadata described above.

6. **Rebuild or Update**
   - When PDFs change, re-ingest that file.
   - Keep `pdf_chunks` and vector DB in sync.

Ingestion CLI example:

```bash
cd apps/api
python -m src.ingest.ingest_pdfs --kb-dir ../../kb
```

---

## 7. Agentic RAG Architecture

### 7.1 Agents

1. **Query Understanding Agent**
   - Input: user message + page/route context.
   - Output: intent:
     - `concept_explanation`
     - `pdf_reference_question`
     - `numerical_problem`
     - `circuit_doubt`
     - `quiz_generation`
     - `out_of_syllabus`.

2. **Retrieval Agent**
   - Uses intent + context (e.g., current PDF or category).
   - Queries vector DB (top-k).
   - Filters by PDF/topic if necessary.
   - Returns chunks + relevance scores.

3. **Reasoning Agent (Gemini 2.0 Flash)**
   - Prompt template:

     **SYSTEM:**

     You are an electronics tutor for digital electronics.  
     Answer ONLY using the provided context from the user's study material.  
     If the context is insufficient, say: "This topic is not covered in your uploaded study material."

     **CONTEXT:**  
     `<<retrieved PDF chunks with metadata>>`

     **QUESTION:**  
     `<<user question>>`

   - Produces clear explanations and, when helpful, references the PDF name and page.

4. **Guardrail Agent**
   - Verifies that:
     - Answer is grounded in retrieved chunks.
   - If not enough matching context:
     - Returns the safe refusal output.

5. **Circuit Agent**
   - Receives circuit JSON + user question.
   - Runs circuit simulation backend tool.
   - Uses Gemini to explain behavior based on results and relevant PDF chunks.

### 7.2 Crio AI Orchestrator

- Central orchestrator that:
  - Decides which agents/tools to call.
  - Manages multi-step workflows (e.g., query → retrieve → reason → guardrail).
  - Logs tool calls and responses.

---

## 8. API Overview

### Auth

- `POST /auth/register` – register user.
- `POST /auth/login` – login, returns JWT.
- `GET /auth/me` – current user info.

### PDFs / Study

- `GET /pdfs` – list PDFs (filter by category).
- `GET /pdfs/{pdf_id}` – get PDF metadata.
- `GET /pdfs/{pdf_id}/search?q=` – search within a PDF.
- `POST /admin/pdfs` – upload PDF (admin).
- `POST /admin/pdfs/{pdf_id}/ingest` – re-ingest a PDF.

### Chat / AI Tutor

- `POST /chat/sessions` – create a chat session.
- `GET /chat/sessions/{id}` – get session + messages.
- `POST /chat/sessions/{id}/messages`
  - Body:  
    ```json
    {
      "message": "Explain JK flip-flop",
      "context": {
        "pdf_id": "flip-flops-123",
        "page": 12,
        "mode": "study"
      }
    }
    ```

### Quizzes

- `GET /quizzes` – list quizzes.
- `GET /quizzes/{id}` – quiz detail.
- `POST /quizzes/{id}/attempts` – submit answers.
- `GET /quizzes/{id}/attempts/{attempt_id}` – attempt result.

Admin-only:

- `POST /admin/quizzes/generate`
  - Input: topic, difficulty, PDF IDs.

### Circuit

- `POST /circuit/simulate`
  - Input: circuit JSON.
  - Output: signals/outputs.

- `POST /circuit/explain`
  - Input: circuit JSON + question.
  - Output: AI explanation (simulation + PDFs).

---

## 9. Environment & Configuration

### Backend `.env` (example)

```bash
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/electronics_ai
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256

VECTOR_DB_PROVIDER=chroma
VECTOR_DB_URL=http://localhost:8001

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=gemini-2.0-flash
GEMINI_EMBED_MODEL_NAME=gemini-embedding-model

KB_DIR=../../kb
ENV=development
```

### Frontend `.env.local` (example)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## 10. Getting Started (Development)

1. **Clone & install dependencies**

   ```bash
   # Frontend
   cd apps/web
   pnpm install  # or npm/yarn

   # Backend
   cd ../api
   pip install -r requirements.txt
   ```

2. **Create `.env` files**
   - `apps/api/.env`
   - `apps/web/.env.local`

3. **Run Postgres + Vector DB** (e.g., Docker Compose)

   ```bash
   docker compose up -d
   ```

4. **Run database migrations**

   ```bash
   cd apps/api
   alembic upgrade head
   ```

5. **Run backend**

   ```bash
   cd apps/api
   uvicorn src.main:app --reload --port 8000
   ```

6. **Run frontend**

   ```bash
   cd apps/web
   pnpm dev --port 3000
   ```

7. **Ingest PDFs**

   - Place your digital electronics PDFs in `kb/` (under appropriate subfolders).
   - Then run:

     ```bash
     cd apps/api
     python -m src.ingest.ingest_pdfs --kb-dir ../../kb
     ```

---

## 11. Roadmap

Suggested implementation order:

1. **MVP 1 – RAG Chat**
   - FastAPI backend + DB.
   - PDF ingestion pipeline + Vector DB.
   - Gemini 2.0 Flash integration.
   - Simple chat UI that answers only from PDFs.

2. **MVP 2 – Dashboard + Study Section**
   - User authentication.
   - Dashboard (XP, level, streak, recent activity).
   - Study page with PDF browsing, PDF viewer, “Ask AI” integration.

3. **MVP 3 – Quizzes**
   - Manual quiz creation + scoring.
   - Add AI-powered quiz generation from PDFs.

4. **MVP 4 – Circuit Lab**
   - Circuit builder UI.
   - Basic digital logic simulator.
   - Circuit agent + AI explanations.

5. **Polish & Production**
   - Role-based admin panel.
   - Better UI/UX, analytics.
   - Deployment, monitoring, logging.

---

## 12. No-Hallucination Policy

- All AI responses:
  - Use **only** the PDF chunks passed in `CONTEXT`.
  - Are subject to a guardrail check.
- If the PDF data is insufficient or unrelated:
  - AI must answer:  
    > “This topic is not covered in your uploaded study material.”
- No external web search or external knowledge sources in live mode.

---

This README describes the full architecture and plan for the Electronics Learning AI Platform.  
You can extend it as the implementation evolves.
