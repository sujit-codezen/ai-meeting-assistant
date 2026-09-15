# 🧠 AI Meeting Assistant

An AI-powered meeting intelligence platform that transforms conversations into searchable knowledge, decisions, tasks, and automated workflows.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat&logo=django&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=flat&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🎙️ **Meeting Recording** | Upload MP3, WAV, M4A, MP4, WebM recordings |
| 📝 **AI Transcription** | Automatic speech-to-text using faster-whisper |
| 👥 **Speaker Diarization** | Identify and label different speakers |
| 🧠 **AI Analysis** | Extract summaries, action items, decisions using Ollama |
| 🔍 **Semantic Search** | RAG-powered search across all meetings |
| 📊 **Sentiment Analysis** | Understand meeting tone and mood |
| ✅ **Task Management** | Track and manage action items |
| 📈 **Analytics Dashboard** | Meeting trends and insights |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Meeting Assistant                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   Frontend   │      │   Backend    │      │ Database │ │
│  │   Next.js    │──────│   Django     │──────│PostgreSQL│ │
│  │   React 19   │      │   DRF        │      │  Redis   │ │
│  │   Tailwind   │      │   Celery     │      │ ChromaDB │ │
│  └──────────────┘      └──────┬───────┘      └──────────┘ │
│                               │                            │
│                    ┌──────────┴──────────┐                 │
│                    │     AI Pipeline     │                 │
│                    ├─────────────────────┤                 │
│                    │  faster-whisper     │                 │
│                    │  Ollama (Llama 3.2) │                 │
│                    │  sentence-transformers│               │
│                    │  ChromaDB           │                 │
│                    └─────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Ollama (for AI features)

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/sujit-codezen/ai-meeting-assistant.git
cd ai-meeting-assistant

# Start all services
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/
# Admin Panel: http://localhost:8000/admin/
```

### Option 2: Local Development

```bash
# Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend Setup (new terminal)
cd frontend
npm install
npm run dev

# Start Celery Worker (new terminal)
cd backend
celery -A config worker -l info --pool=solo

# Start Ollama (new terminal)
ollama pull llama3.2
ollama serve
```

### Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

---

## 📁 Project Structure

```
ai-meeting-assistant/
├── backend/                    # Django backend
│   ├── apps/                  # Django applications
│   │   ├── accounts/          # User authentication
│   │   ├── meetings/          # Meeting management
│   │   ├── transcripts/       # Transcript storage
│   │   ├── action_items/      # Task extraction
│   │   ├── decisions/         # Decision tracking
│   │   ├── summaries/         # AI summaries
│   │   ├── ai/               # AI endpoints
│   │   ├── analytics/         # Dashboard stats
│   │   └── notifications/     # User notifications
│   ├── ai/                    # AI modules
│   │   ├── prompts/           # LLM prompts
│   │   └── rag/              # RAG pipeline
│   ├── workers/               # Celery tasks
│   └── config/                # Django settings
├── frontend/                  # Next.js frontend
│   └── src/
│       ├── app/              # Pages (11 routes)
│       ├── components/       # React components
│       └── lib/              # API client, auth, utils
├── docker-compose.yml         # Docker orchestration
└── README.md
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register/` | POST | Register new user |
| `/api/v1/auth/login/` | POST | Login |
| `/api/v1/meetings/` | GET/POST | List/create meetings |
| `/api/v1/meetings/{id}/process/` | POST | Start AI processing |
| `/api/v1/tasks/` | GET | List action items |
| `/api/v1/tasks/{id}/update_status/` | PATCH | Update task status |
| `/api/v1/analytics/dashboard/` | GET | Dashboard stats |
| `/api/v1/ai/qa/` | POST | Ask questions about meetings |
| `/api/v1/ai/search/` | POST | Semantic search |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 16, React 19, Tailwind CSS 4 | Modern web interface |
| **Backend** | Django 6.1, Django REST Framework | REST API |
| **Database** | PostgreSQL 16 | Data storage |
| **Cache/Queue** | Redis 8, Celery 5 | Task processing |
| **STT** | faster-whisper | Speech-to-text |
| **LLM** | Ollama (Llama 3.2) | Text analysis |
| **Embeddings** | sentence-transformers | Semantic search |
| **Vector DB** | ChromaDB | RAG storage |

---

## 📸 Screenshots

### Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  Dashboard                                              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Meetings │ │  Tasks   │ │Decisions │ │ Overdue  │   │
│  │    42    │ │   128    │ │    67    │ │    3     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│  Recent Meetings              │  Quick Actions           │
│  ─────────────────           │  ─────────────           │
│  Product Meeting     45min   │  📤 Upload Meeting       │
│  Engineering Sync    32min   │  ✅ View Tasks           │
│  Marketing Meeting   51min   │  🔍 Search Meetings      │
└─────────────────────────────────────────────────────────┘
```

### Meeting Detail
```
┌─────────────────────────────────────────────────────────┐
│  Product Launch Meeting                    [Completed]  │
├─────────────────────────────────────────────────────────┤
│  Transcript │ Summary │ Action Items │ Decisions │ Q&A  │
├─────────────────────────────────────────────────────────┤
│  [0:00] Commentator 1: Let's discuss the product...    │
│  [0:05] Commentator 2: I don't think backend is...     │
│  [0:10] Commentator 1: Okay, let's move it to Monday   │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 How It Works

1. **Upload Recording** → Drag & drop MP3/WAV/M4A/MP4
2. **AI Transcription** → faster-whisper converts speech to text
3. **Speaker Detection** → Identifies different speakers
4. **AI Analysis** → Ollama extracts:
   - Executive summary
   - Key points
   - Action items with owners & deadlines
   - Decisions made
   - Sentiment analysis
5. **Semantic Embeddings** → ChromaDB enables RAG search
6. **Ask Questions** → Query your meetings with AI

---

## 🔧 Environment Variables

```bash
# Backend
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_meeting
REDIS_URL=redis://localhost:6379/0
OLLAMA_BASE_URL=http://localhost:11434
WHISPER_MODEL=medium
CHROMADB_PATH=./chromadb_data
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Sujit** - [GitHub](https://github.com/sujit-codezen) | [LinkedIn](https://linkedin.com/in/sujit-codezen)

---

## 🙏 Acknowledgments

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Fast transcription
- [Ollama](https://ollama.com/) - Local LLM inference
- [sentence-transformers](https://www.sbert.net/) - Embeddings
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Django](https://www.djangoproject.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework
