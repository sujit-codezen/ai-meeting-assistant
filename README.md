# AI Meeting Assistant

An AI-powered meeting intelligence platform that transforms conversations into searchable knowledge, decisions, tasks, and automated workflows.

## Features

- **Meeting Recording Upload** - Support for MP3, WAV, M4A, MP4, WebM
- **AI Transcription** - Automatic speech-to-text using faster-whisper
- **Speaker Diarization** - Identify and label different speakers
- **AI Analysis** - Extract summaries, action items, and decisions using Ollama
- **Semantic Search** - RAG-powered search across all meetings using ChromaDB
- **Sentiment Analysis** - Understand meeting tone and mood
- **Task Management** - Track and manage action items
- **Analytics Dashboard** - Meeting trends and insights

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Backend | Django 6.1, Django REST Framework |
| Database | PostgreSQL 16 |
| Cache/Queue | Redis 8, Celery 5 |
| STT | faster-whisper |
| LLM | Ollama (Llama 3.2) |
| Embeddings | sentence-transformers (nomic-embed-text) |
| Vector DB | ChromaDB |

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone and start
docker-compose up

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

### Local Development

#### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 16
- Redis 8
- Ollama

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Start Redis and Celery
redis-server
celery -A config worker -l info

# Start Django
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Ollama Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2

# Start server
ollama serve
```

## Project Structure

```
ai_meeting/
├── backend/
│   ├── apps/           # Django apps
│   │   ├── accounts/   # User authentication
│   │   ├── meetings/   # Meeting management
│   │   ├── transcripts/# Transcript storage
│   │   ├── action_items/# Task extraction
│   │   ├── decisions/  # Decision tracking
│   │   ├── summaries/  # AI summaries
│   │   ├── ai/         # AI endpoints
│   │   ├── analytics/  # Dashboard stats
│   │   └── notifications/# User notifications
│   ├── ai/             # AI prompts and modules
│   ├── workers/        # Celery tasks
│   └── config/         # Django settings
├── frontend/
│   └── src/
│       ├── app/        # Next.js pages
│       ├── components/ # React components
│       └── lib/        # API client, auth, utils
└── docker-compose.yml
```

## API Endpoints

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

## Environment Variables

```bash
# Backend
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_meeting
REDIS_URL=redis://localhost:6379/0
OLLAMA_BASE_URL=http://localhost:11434
WHISPER_MODEL=base
HUGGINGFACE_TOKEN=your-token
CHROMADB_PATH=./chromadb_data
```

## License

MIT
