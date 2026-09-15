# 🧠 AI Meeting Assistant

> Transform your meetings into actionable intelligence with AI-powered transcription, analysis, and semantic search.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## ✨ Why This Project?

Meetings generate valuable insights, but most of that information gets lost in recordings and scattered notes. **AI Meeting Assistant** solves this by automatically:

- 📝 Converting speech to accurate transcripts
- 🧠 Extracting key decisions and action items
- 🔍 Making all your meetings searchable with AI
- ✅ Tracking tasks with owners and deadlines

**Built for teams who want to focus on the conversation, not the note-taking.**

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🎙️ **Meeting Recording** | Upload MP3, WAV, M4A, MP4, WebM recordings |
| 📝 **AI Transcription** | Accurate speech-to-text with faster-whisper (medium model) |
| 👥 **Speaker Diarization** | Identify and label different speakers automatically |
| 🧠 **AI Analysis** | Extract summaries, action items, decisions using Ollama + Llama 3.2 |
| 🔍 **Semantic Search** | RAG-powered search across all your meetings |
| 📊 **Sentiment Analysis** | Understand meeting tone — positive, neutral, negative |
| ✅ **Task Management** | Track action items with owners, deadlines, and priority |
| 📈 **Analytics Dashboard** | Visualize meeting trends and team productivity |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI Meeting Assistant                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐ │
│   │   Frontend  │       │   Backend   │       │   Storage   │ │
│   │             │       │             │       │             │ │
│   │  Next.js 16 │──────▶│  Django 6.1 │──────▶│ PostgreSQL  │ │
│   │  React 19   │       │  DRF        │       │ Redis       │ │
│   │  Tailwind 4 │       │  Celery 5   │       │ ChromaDB    │ │
│   └─────────────┘       └──────┬──────┘       └─────────────┘ │
│                                │                               │
│                     ┌──────────▼──────────┐                    │
│                     │     AI Pipeline     │                    │
│                     ├─────────────────────┤                    │
│                     │  🔊 faster-whisper   │  Speech → Text    │
│                     │  🤖 Ollama + Llama  │  Text → Insights  │
│                     │  🧮 sentence-transformers │ Embeddings   │
│                     │  💾 ChromaDB         │  Vector Store     │
│                     └─────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Backend runtime |
| Node.js | 20+ | Frontend runtime |
| Docker | Latest | Containerization |
| Ollama | Latest | Local AI inference |

### Quick Start with Docker

```bash
# 1. Clone the repository
git clone https://github.com/sujit-codezen/ai-meeting-assistant.git
cd ai-meeting-assistant

# 2. Start all services
docker-compose up

# 3. Open in browser
open http://localhost:3000
```

### Local Development

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

# Celery Worker (new terminal)
cd backend
celery -A config worker -l info --pool=solo

# Ollama Setup (new terminal)
ollama pull llama3.2
ollama serve
```

### 🔑 Default Credentials

```
Username: admin
Password: admin123
```

---

## 📁 Project Structure

```
ai-meeting-assistant/
│
├── 📂 backend/                     # Django REST API
│   ├── 📂 apps/                   # 10 Django applications
│   │   ├── accounts/              # 🔐 User authentication
│   │   ├── meetings/              # 📅 Meeting management
│   │   ├── transcripts/           # 📝 Transcript storage
│   │   ├── participants/          # 👥 Speaker management
│   │   ├── action_items/          # ✅ Task extraction
│   │   ├── decisions/             # 🎯 Decision tracking
│   │   ├── summaries/             # 📄 AI summaries
│   │   ├── ai/                   # 🤖 AI endpoints
│   │   ├── analytics/             # 📊 Dashboard stats
│   │   └── notifications/         # 🔔 User notifications
│   ├── 📂 ai/                    # AI modules
│   │   ├── prompts/               # LLM prompt templates
│   │   └── rag/                  # RAG pipeline
│   ├── 📂 workers/               # Celery async tasks
│   └── 📂 config/                # Django settings
│
├── 📂 frontend/                   # Next.js Application
│   └── 📂 src/
│       ├── 📂 app/               # 11 page routes
│       ├── 📂 components/        # Reusable React components
│       └── 📂 lib/               # API client, auth, utils
│
├── 🐳 docker-compose.yml          # Docker orchestration
└── 📄 README.md
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register/` | `POST` | Create new account |
| `/api/v1/auth/login/` | `POST` | Authenticate user |
| `/api/v1/meetings/` | `GET` `POST` | List or create meetings |
| `/api/v1/meetings/{id}/` | `GET` | Get meeting details |
| `/api/v1/meetings/{id}/process/` | `POST` | Trigger AI processing |
| `/api/v1/tasks/` | `GET` | List action items |
| `/api/v1/tasks/{id}/update_status/` | `PATCH` | Update task status |
| `/api/v1/analytics/dashboard/` | `GET` | Dashboard statistics |
| `/api/v1/ai/qa/` | `POST` | Ask questions about meetings |
| `/api/v1/ai/search/` | `POST` | Semantic search across meetings |

---

## 🧪 How It Works

```
   📤 Upload           🔄 Process           📊 Results
      │                    │                    │
      ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│  Audio   │───────▶│ AI       │───────▶│ Insights │
│  File    │        │ Pipeline │        │ Dashboard│
└──────────┘        └──────────┘        └──────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
     ┌──────────┐  ┌──────────┐  ┌──────────┐
     │Whisper   │  │ Ollama   │  │ ChromaDB │
     │Transcribe│  │ Analyze  │  │ Embed    │
     └──────────┘  └──────────┘  └──────────┘
```

### Step-by-Step Process

| Step | Action | Result |
|------|--------|--------|
| 1️⃣ | Upload recording | MP3/WAV/M4A/MP4 stored |
| 2️⃣ | faster-whisper processes audio | Timestamped transcript |
| 3️⃣ | Speaker diarization | Speakers identified |
| 4️⃣ | Ollama analyzes content | Summary + Action items + Decisions |
| 5️⃣ | Embeddings generated | Enable semantic search |
| 6️⃣ | Query with AI | Ask questions, get answers |

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | Next.js 16 + React 19 | Modern SSR, great DX |
| **Styling** | Tailwind CSS 4 | Rapid UI development |
| **Backend** | Django 6.1 + DRF | Robust, scalable API |
| **Database** | PostgreSQL 16 | Reliable, feature-rich |
| **Cache** | Redis 8 | Fast caching + queue |
| **Queue** | Celery 5 | Async task processing |
| **STT** | faster-whisper | Fast, accurate transcription |
| **LLM** | Ollama + Llama 3.2 | Local AI inference |
| **Embeddings** | sentence-transformers | Semantic understanding |
| **Vector DB** | ChromaDB | RAG-powered search |
| **Container** | Docker Compose | One-command deployment |

---

## 📸 Screenshots

### Dashboard
```
┌──────────────────────────────────────────────────────────────┐
│  🧠 AI Meeting Assistant                              [User]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 📅       │ │ ✅       │ │ 🎯       │ │ ⚠️       │       │
│  │ Meetings │ │  Tasks   │ │Decisions │ │ Overdue  │       │
│  │    42    │ │   128    │ │    67    │ │    3     │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│  📋 Recent Meetings            │  ⚡ Quick Actions           │
│  ────────────────────         │  ────────────────           │
│  Product Meeting      45min   │  📤 Upload Meeting          │
│  Engineering Sync     32min   │  ✅ View Tasks              │
│  Marketing Meeting    51min   │  🔍 Search with AI          │
└──────────────────────────────────────────────────────────────┘
```

### Meeting Transcript View
```
┌──────────────────────────────────────────────────────────────┐
│  📅 Product Launch Meeting                      ✅ Completed │
├──────────────────────────────────────────────────────────────┤
│  Transcript │ Summary │ Action Items │ Decisions │ 💬 Q&A   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ⏱️ 0:00   Commentator 1                                      │
│  │ Let's discuss the product launch timeline.                │
│  │                                                            │
│  ⏱️ 0:05   Commentator 2                                      │
│  │ I don't think the backend is ready yet.                   │
│  │                                                            │
│  ⏱️ 0:10   Commentator 1                                      │
│  │ Okay, let's move it to Monday then.                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Sujit**

- GitHub: [@sujit-codezen](https://github.com/sujit-codezen)
- LinkedIn: [sujit-codezen](https://linkedin.com/in/sujit-codezen)

---

## 🗺️ Roadmap

- [x] AI-powered meeting transcription
- [x] Speaker diarization
- [x] Action item extraction
- [x] Decision tracking
- [x] Semantic search with RAG
- [x] Real-time meeting processing
- [x] Docker deployment
- [ ] Live meeting recording
- [ ] Calendar integration
- [ ] Email notifications for tasks
- [ ] Slack/Teams integration

---

## 📞 Support

If you have any questions or need help, feel free to reach out:

- **Email**: sujit@codezen.dev
- **GitHub Issues**: [Create an issue](https://github.com/sujit-codezen/ai-meeting-assistant/issues)

---

## 🙏 Acknowledgments

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — Fast & accurate transcription
- [Ollama](https://ollama.com/) — Local LLM inference made easy
- [sentence-transformers](https://www.sbert.net/) — State-of-the-art embeddings
- [ChromaDB](https://www.trychroma.com/) — Developer-friendly vector database
- [Django](https://www.djangoproject.com/) — The web framework for perfectionists
- [Next.js](https://nextjs.org/) — The React framework for production

---

<div align="center">

**⭐ If you found this project helpful, please give it a star on GitHub! ⭐**

[![GitHub](https://img.shields.io/github/stars/sujit-codezen/ai-meeting-assistant?style=social)](https://github.com/sujit-codezen/ai-meeting-assistant)

</div>
