import os
import json
import time
import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def transcribe_meeting(self, meeting_id):
    from apps.meetings.models import Meeting
    from apps.transcripts.models import TranscriptSegment
    from apps.participants.models import Participant
    from apps.ai.models import AIProcessingLog

    meeting = Meeting.objects.get(id=meeting_id)
    meeting.status = 'processing'
    meeting.save()

    log = AIProcessingLog.objects.create(
        meeting_id=meeting_id,
        task_type='transcription',
        status='processing'
    )

    start_time = time.time()

    try:
        from faster_whisper import WhisperModel

        model_size = os.environ.get('WHISPER_MODEL', 'base')
        device = 'cpu'
        compute_type = 'int8'

        logger.info(f"Loading Whisper model: {model_size}")
        model = WhisperModel(model_size, device=device, compute_type=compute_type)

        logger.info(f"Transcribing: {meeting.recording.path}")
        segments_iter, info = model.transcribe(
            meeting.recording.path,
            beam_size=5,
            language='en',
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200,
            ),
        )

        logger.info(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

        # Process segments and assign speakers
        speaker_count = 0
        speakers = {}
        segment_count = 0

        for i, segment in enumerate(segments_iter):
            # Simple speaker assignment based on segment patterns
            # In production, use pyannote for proper diarization
            speaker_label = f"Speaker {((i // 5) % 3) + 1}"

            if speaker_label not in speakers:
                speaker_count += 1
                speakers[speaker_label] = f"Speaker {speaker_count}"

            TranscriptSegment.objects.create(
                meeting=meeting,
                speaker_label=speakers[speaker_label],
                text=segment.text.strip(),
                start_time=segment.start,
                end_time=segment.end,
                confidence=1.0 - abs(segment.avg_logprob) if hasattr(segment, 'avg_logprob') else 0.8,
                order=i
            )
            segment_count = i + 1

        # Create participants from detected speakers
        for label in speakers.values():
            Participant.objects.get_or_create(
                meeting=meeting,
                speaker_label=label,
                defaults={'name': label}
            )

        meeting.status = 'transcribed'
        meeting.save()

        log.status = 'completed'
        log.processing_time = time.time() - start_time
        log.completed_at = timezone.now()
        log.result = {'segments_count': segment_count, 'speakers': list(speakers.values())}
        log.save()

        logger.info(f"Transcription completed: {segment_count} segments, {len(speakers)} speakers")

        # Trigger analysis
        analyze_meeting.delay(meeting_id)

    except Exception as e:
        logger.error(f"Transcription failed for meeting {meeting_id}: {str(e)}")
        meeting.status = 'failed'
        meeting.save()
        log.status = 'failed'
        log.error_message = str(e)
        log.processing_time = time.time() - start_time
        log.save()
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def analyze_meeting(self, meeting_id):
    from apps.meetings.models import Meeting
    from apps.transcripts.models import TranscriptSegment
    from apps.summaries.models import MeetingSummary
    from apps.action_items.models import ActionItem
    from apps.decisions.models import Decision
    from apps.ai.models import AIProcessingLog

    meeting = Meeting.objects.get(id=meeting_id)
    segments = meeting.segments.all()

    if not segments.exists():
        logger.warning(f"No segments found for meeting {meeting_id}")
        return

    transcript = "\n".join([
        f"[{s.start_time:.1f}s] {s.speaker_label}: {s.text}"
        for s in segments
    ])

    log = AIProcessingLog.objects.create(
        meeting_id=meeting_id,
        task_type='summarization',
        status='processing'
    )

    start_time = time.time()

    try:
        import ollama

        ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        model_name = os.environ.get('OLLAMA_MODEL', 'llama3.2')

        # Check if Ollama is available
        try:
            ollama.list()
        except Exception:
            logger.warning("Ollama not available, using mock analysis")
            _create_mock_analysis(meeting)
            log.status = 'completed'
            log.processing_time = time.time() - start_time
            log.completed_at = timezone.now()
            log.save()
            meeting.status = 'analyzed'
            meeting.save()
            generate_embeddings.delay(meeting_id)
            return

        # Generate summary
        summary_response = ollama.chat(model=model_name, messages=[
            {'role': 'system', 'content': SUMMARY_PROMPT},
            {'role': 'user', 'content': transcript[:8000]}  # Limit for context window
        ])
        summary_content = summary_response['message']['content']

        # Parse JSON from response
        try:
            # Try to extract JSON from the response
            json_start = summary_content.find('{')
            json_end = summary_content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                summary_data = json.loads(summary_content[json_start:json_end])
            else:
                summary_data = json.loads(summary_content)
        except json.JSONDecodeError:
            summary_data = {
                'executive_summary': summary_content,
                'key_points': [],
                'sentiment': {'positive': 50, 'neutral': 40, 'negative': 10},
                'topics': [],
                'unresolved_issues': []
            }

        MeetingSummary.objects.update_or_create(
            meeting=meeting,
            defaults={
                'executive_summary': summary_data.get('executive_summary', ''),
                'key_points': summary_data.get('key_points', []),
                'sentiment': summary_data.get('sentiment', {}),
                'topics': summary_data.get('topics', []),
                'unresolved_issues': summary_data.get('unresolved_issues', []),
            }
        )

        # Extract action items
        actions_response = ollama.chat(model=model_name, messages=[
            {'role': 'system', 'content': ACTION_ITEMS_PROMPT},
            {'role': 'user', 'content': transcript[:8000]}
        ])
        actions_content = actions_response['message']['content']

        try:
            json_start = actions_content.find('[')
            json_end = actions_content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                actions_data = json.loads(actions_content[json_start:json_end])
            else:
                actions_data = json.loads(actions_content)
        except json.JSONDecodeError:
            actions_data = []

        for action in actions_data:
            if isinstance(action, dict):
                ActionItem.objects.create(
                    meeting=meeting,
                    task=action.get('task', action.get('description', '')),
                    assigned_to_name=action.get('assigned_to', action.get('owner', 'Unknown')),
                    deadline=action.get('deadline', ''),
                    priority=action.get('priority', 'medium'),
                    context=action.get('context', '')
                )

        # Extract decisions
        decisions_response = ollama.chat(model=model_name, messages=[
            {'role': 'system', 'content': DECISIONS_PROMPT},
            {'role': 'user', 'content': transcript[:8000]}
        ])
        decisions_content = decisions_response['message']['content']

        try:
            json_start = decisions_content.find('[')
            json_end = decisions_content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                decisions_data = json.loads(decisions_content[json_start:json_end])
            else:
                decisions_data = json.loads(decisions_content)
        except json.JSONDecodeError:
            decisions_data = []

        for decision in decisions_data:
            if isinstance(decision, dict):
                Decision.objects.create(
                    meeting=meeting,
                    title=decision.get('title', decision.get('decision', '')),
                    description=decision.get('description', decision.get('details', '')),
                    reason=decision.get('reason', ''),
                    status=decision.get('status', 'approved'),
                    context=decision.get('context', '')
                )

        meeting.status = 'analyzed'
        meeting.save()

        log.status = 'completed'
        log.processing_time = time.time() - start_time
        log.completed_at = timezone.now()
        log.result = {
            'summary_generated': True,
            'action_items_count': len(actions_data),
            'decisions_count': len(decisions_data)
        }
        log.save()

        logger.info(f"Analysis completed: {len(actions_data)} actions, {len(decisions_data)} decisions")

        # Generate embeddings for RAG
        generate_embeddings.delay(meeting_id)

    except Exception as e:
        logger.error(f"Analysis failed for meeting {meeting_id}: {str(e)}")
        meeting.status = 'failed'
        meeting.save()
        log.status = 'failed'
        log.error_message = str(e)
        log.processing_time = time.time() - start_time
        log.save()
        raise self.retry(exc=e, countdown=60)


def _create_mock_analysis(meeting):
    """Create mock analysis when Ollama is not available."""
    from apps.summaries.models import MeetingSummary
    from apps.action_items.models import ActionItem
    from apps.decisions.models import Decision

    MeetingSummary.objects.update_or_create(
        meeting=meeting,
        defaults={
            'executive_summary': 'Meeting analysis will be available once Ollama is configured and running.',
            'key_points': [
                'AI analysis requires Ollama to be running',
                'Configure OLLAMA_BASE_URL in your environment',
                'Pull a model with: ollama pull llama3.2'
            ],
            'sentiment': {'positive': 50, 'neutral': 40, 'negative': 10},
            'topics': ['Configuration Required'],
            'unresolved_issues': ['Ollama setup needed for full analysis']
        }
    )


@shared_task
def generate_embeddings(meeting_id):
    from apps.meetings.models import Meeting
    from apps.transcripts.models import TranscriptSegment
    from apps.ai.models import AIProcessingLog

    meeting = Meeting.objects.get(id=meeting_id)
    segments = meeting.segments.all()

    log = AIProcessingLog.objects.create(
        meeting_id=meeting_id,
        task_type='embedding_generation',
        status='processing'
    )

    start_time = time.time()

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer

        client = chromadb.PersistentClient(path="./chromadb_data")
        collection = client.get_or_create_collection(
            name="meeting_transcripts",
            metadata={"hnsw:space": "cosine"}
        )

        # Chunk transcript
        chunk_size = 5
        chunks = []
        for i in range(0, len(segments), chunk_size):
            group = segments[i:i + chunk_size]
            chunks.append({
                "text": " ".join([s.text for s in group]),
                "speaker": group[0].speaker_label,
                "timestamp": f"{group[0].start_time:.1f}s",
            })

        if chunks:
            model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5')
            embeddings = model.encode([c['text'] for c in chunks])

            # Remove old embeddings for this meeting
            try:
                old_docs = collection.get(where={"meeting_id": str(meeting_id)})
                if old_docs['ids']:
                    collection.delete(ids=old_docs['ids'])
            except Exception:
                pass

            collection.add(
                documents=[c['text'] for c in chunks],
                embeddings=embeddings.tolist(),
                ids=[f"meeting_{meeting_id}_chunk_{i}" for i in range(len(chunks))],
                metadatas=[{
                    "meeting_id": str(meeting_id),
                    "speaker": c['speaker'],
                    "timestamp": c['timestamp'],
                    "date": meeting.date.isoformat(),
                } for c in chunks]
            )

        meeting.status = 'completed'
        meeting.save()

        log.status = 'completed'
        log.processing_time = time.time() - start_time
        log.completed_at = timezone.now()
        log.save()

        logger.info(f"Embeddings generated: {len(chunks)} chunks")

    except Exception as e:
        logger.error(f"Embedding generation failed: {str(e)}")
        log.status = 'failed'
        log.error_message = str(e)
        log.processing_time = time.time() - start_time
        log.save()
        # Don't raise - embeddings are non-critical


# Prompts
SUMMARY_PROMPT = """You are an expert meeting analyst. Analyze the following meeting transcript and provide a comprehensive analysis.

Return your response as valid JSON with this exact structure:
{
    "executive_summary": "2-3 paragraph summary of the meeting",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "topics": ["Topic 1", "Topic 2"],
    "unresolved_issues": ["Issue 1", "Issue 2"],
    "sentiment": {
        "positive": 62,
        "neutral": 28,
        "negative": 10
    }
}

Meeting Transcript:
"""

ACTION_ITEMS_PROMPT = """Extract all action items from this meeting transcript. Be thorough and identify:
- Tasks that need to be completed
- Who is responsible (use speaker names if mentioned)
- Deadlines (exact dates or relative times like "Thursday", "next week")
- Priority level based on urgency context

Return your response as a valid JSON array:
[
    {
        "task": "Description of the task",
        "assigned_to": "Person's name or Unknown",
        "deadline": "Deadline string or No deadline",
        "priority": "low|medium|high|urgent",
        "context": "Original quote from transcript that led to this action item"
    }
]

Meeting Transcript:
"""

DECISIONS_PROMPT = """Extract all decisions made during this meeting. Identify:
- What was decided
- The reason or rationale
- Whether it was approved, pending, or rejected

Return your response as a valid JSON array:
[
    {
        "title": "Short title for the decision",
        "description": "What was decided",
        "reason": "Why this decision was made",
        "status": "approved|pending|rejected",
        "context": "Original quote from transcript"
    }
]

Meeting Transcript:
"""
