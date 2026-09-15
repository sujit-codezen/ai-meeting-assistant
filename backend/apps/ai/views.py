from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import ollama
import chromadb
from sentence_transformers import SentenceTransformer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def meeting_qa(request):
    meeting_id = request.data.get('meeting_id')
    question = request.data.get('question')

    if not meeting_id or not question:
        return Response({'error': 'meeting_id and question are required'}, status=400)

    try:
        client = chromadb.PersistentClient(path="./chromadb_data")
        collection = client.get_collection("meeting_transcripts")

        model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5')
        query_embedding = model.encode([question])

        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=5,
            where={"meeting_id": str(meeting_id)}
        )

        context = "\n\n".join(results['documents'][0]) if results['documents'][0] else "No relevant context found."

        response = ollama.chat(model='llama3.2:latest', messages=[
            {'role': 'system', 'content': 'You are a helpful meeting assistant. Answer questions based on the meeting transcript context provided. Be concise and accurate.'},
            {'role': 'user', 'content': f"Context:\n{context}\n\nQuestion: {question}"}
        ])

        return Response({
            'answer': response['message']['content'],
            'sources': results['metadatas'][0] if results['metadatas'] else []
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_meetings(request):
    query = request.data.get('query')
    if not query:
        return Response({'error': 'query is required'}, status=400)

    try:
        client = chromadb.PersistentClient(path="./chromadb_data")
        collection = client.get_collection("meeting_transcripts")

        model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5')
        query_embedding = model.encode([query])

        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=10
        )

        return Response({
            'results': [
                {
                    'text': doc,
                    'metadata': meta
                }
                for doc, meta in zip(results['documents'][0], results['metadatas'][0])
            ] if results['documents'] else []
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)
