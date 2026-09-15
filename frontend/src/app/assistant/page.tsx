"use client";

import { AuthWrapper } from "@/components/AuthWrapper";
import { useState } from "react";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Brain, Loader2, Send } from "lucide-react";
import { aiAPI } from "@/lib/api";

function AssistantContent() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await aiAPI.searchMeetings(query);
      if (res.data.results && res.data.results.length > 0) {
        const context = res.data.results.map((r: { text: string }) => r.text).join("\n\n");
        setAnswer(`Based on your meetings:\n\n${context}`);
      } else {
        setAnswer("No relevant information found in your meetings.");
      }
    } catch {
      setAnswer("Failed to get response. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">AI Assistant</h1>
        <p className="text-gray-600">
          Ask questions across all your meetings and get AI-powered insights.
        </p>
      </div>

      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleAsk()}
              placeholder="Ask anything about your meetings..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
            />
            <Button onClick={handleAsk} loading={loading} size="lg">
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </Button>
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">Try asking:</span>
            {[
              "Summarize all meetings from this week",
              "What are the most common action items?",
              "Which meetings had the most decisions?",
              "What topics come up frequently?",
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setQuery(suggestion)}
                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {loading && (
        <div className="text-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Thinking...</p>
        </div>
      )}

      {answer && !loading && (
        <Card>
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <Brain className="w-5 h-5 text-blue-600" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 mb-2">AI Response</h3>
                <div className="text-gray-700 whitespace-pre-wrap">{answer}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default function AssistantPage() {
  return (
    <AuthWrapper>
      <AssistantContent />
    </AuthWrapper>
  );
}
