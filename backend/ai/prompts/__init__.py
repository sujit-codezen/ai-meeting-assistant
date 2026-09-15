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

SENTIMENT_PROMPT = """Analyze the overall sentiment and tone of this meeting transcript.

Return your response as a valid JSON object:
{
    "overall_sentiment": "positive|neutral|negative",
    "confidence": 0.85,
    "positive_percentage": 62,
    "neutral_percentage": 28,
    "negative_percentage": 10,
    "key_emotions": ["collaborative", "concerned", "optimistic"],
    "disagreements": ["Description of any disagreements"],
    "concerns": ["Any concerns raised"],
    "questions": ["Important questions asked"]
}

Meeting Transcript:
"""
