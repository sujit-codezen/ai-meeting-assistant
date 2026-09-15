"use client";

import { AuthWrapper } from "@/components/AuthWrapper";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import {
  ArrowLeft,
  Calendar,
  Clock,
  Users,
  Brain,
  CheckSquare,
  AlertTriangle,
  Search,
  Loader2,
} from "lucide-react";
import { meetingsAPI, aiAPI } from "@/lib/api";

interface MeetingDetail {
  id: number;
  title: string;
  description: string;
  date: string;
  status: string;
  recording: string;
  participants: { id: number; name: string; speaker_label: string }[];
  segments: {
    id: number;
    speaker_label: string;
    speaker_name: string;
    text: string;
    start_time: number;
    end_time: number;
  }[];
  summary: {
    executive_summary: string;
    key_points: string[];
    sentiment: { positive: number; neutral: number; negative: number };
    topics: string[];
    unresolved_issues: string[];
  } | null;
  action_items: {
    id: number;
    task: string;
    assigned_to_name: string;
    deadline: string;
    priority: string;
    status: string;
  }[];
  decisions: {
    id: number;
    title: string;
    description: string;
    reason: string;
    status: string;
  }[];
}

function MeetingDetailContent() {
  const params = useParams();
  const router = useRouter();
  const [meeting, setMeeting] = useState<MeetingDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState("transcript");
  const [qaQuestion, setQaQuestion] = useState("");
  const [qaAnswer, setQaAnswer] = useState("");
  const [qaLoading, setQaLoading] = useState(false);

  useEffect(() => {
    meetingsAPI
      .get(Number(params.id))
      .then((res) => setMeeting(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [params.id]);

  const handleProcess = async () => {
    if (!meeting) return;
    setProcessing(true);
    try {
      await meetingsAPI.process(meeting.id);
      setMeeting({ ...meeting, status: "processing" });
    } catch (err) {
      console.error(err);
    } finally {
      setProcessing(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!qaQuestion.trim() || !meeting) return;
    setQaLoading(true);
    try {
      const res = await aiAPI.askQuestion(meeting.id, qaQuestion);
      setQaAnswer(res.data.answer);
    } catch {
      setQaAnswer("Failed to get answer. Please try again.");
    } finally {
      setQaLoading(false);
    }
  };

  const tabs = [
    { id: "transcript", label: "Transcript", icon: Clock },
    { id: "summary", label: "Summary", icon: Brain },
    { id: "actions", label: "Action Items", icon: CheckSquare },
    { id: "decisions", label: "Decisions", icon: AlertTriangle },
    { id: "qa", label: "Q&A", icon: Search },
  ];

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-48"></div>
          <div className="h-64 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  if (!meeting) {
    return (
      <div className="p-8 text-center">
        <p className="text-gray-500">Meeting not found.</p>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex items-center gap-4 mb-6">
        <Button variant="ghost" onClick={() => router.back()}>
          <ArrowLeft className="w-4 h-4" />
        </Button>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-gray-900">{meeting.title}</h1>
            <StatusBadge status={meeting.status} />
          </div>
          <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              {new Date(meeting.date).toLocaleDateString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
              })}
            </span>
            <span className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              {meeting.participants.length} participants
            </span>
          </div>
        </div>
        {meeting.status === "uploaded" && (
          <Button onClick={handleProcess} loading={processing}>
            {processing ? "Processing..." : "Start Processing"}
          </Button>
        )}
      </div>

      <div className="flex gap-1 border-b border-gray-200 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === "transcript" && (
        <Card>
          <CardContent className="p-6">
            {meeting.segments.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                {meeting.status === "uploaded"
                  ? "Processing not started yet."
                  : meeting.status === "processing"
                  ? "Transcription in progress..."
                  : "No transcript available."}
              </p>
            ) : (
              <div className="space-y-4">
                {meeting.segments.map((segment) => (
                  <div key={segment.id} className="flex gap-4">
                    <div className="w-20 flex-shrink-0">
                      <span className="text-xs text-gray-500">
                        {Math.floor(segment.start_time / 60)}:
                        {Math.floor(segment.start_time % 60)
                          .toString()
                          .padStart(2, "0")}
                      </span>
                    </div>
                    <div className="flex-1">
                      <span className="font-medium text-blue-600">
                        {segment.speaker_name || segment.speaker_label}
                      </span>
                      <p className="text-gray-900 mt-1">{segment.text}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {activeTab === "summary" && (
        <div className="space-y-6">
          {meeting.summary ? (
            <>
              <Card>
                <CardHeader>
                  <CardTitle>Executive Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">
                    {meeting.summary.executive_summary}
                  </p>
                </CardContent>
              </Card>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Key Points</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {meeting.summary.key_points.map((point, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckSquare className="w-4 h-4 text-green-600 mt-0.5" />
                          <span className="text-gray-700">{point}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {meeting.summary.sentiment && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Sentiment Analysis</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {[
                          { label: "Positive", value: meeting.summary.sentiment.positive, color: "bg-green-500" },
                          { label: "Neutral", value: meeting.summary.sentiment.neutral, color: "bg-gray-500" },
                          { label: "Negative", value: meeting.summary.sentiment.negative, color: "bg-red-500" },
                        ].map((item) => (
                          <div key={item.label}>
                            <div className="flex justify-between text-sm mb-1">
                              <span>{item.label}</span>
                              <span>{item.value}%</span>
                            </div>
                            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                              <div
                                className={`h-full ${item.color}`}
                                style={{ width: `${item.value}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="text-center py-12">
                <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">Summary not available yet.</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {activeTab === "actions" && (
        <Card>
          <CardContent className="p-6">
            {meeting.action_items.length === 0 ? (
              <p className="text-center text-gray-500 py-8">No action items extracted yet.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Task</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Assigned To</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Deadline</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Priority</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {meeting.action_items.map((item) => (
                      <tr key={item.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4 text-gray-900">{item.task}</td>
                        <td className="py-3 px-4 text-gray-600">{item.assigned_to_name}</td>
                        <td className="py-3 px-4 text-gray-600">{item.deadline}</td>
                        <td className="py-3 px-4">
                          <PriorityBadge priority={item.priority} />
                        </td>
                        <td className="py-3 px-4">
                          <StatusBadge status={item.status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {activeTab === "decisions" && (
        <div className="space-y-4">
          {meeting.decisions.length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No decisions extracted yet.</p>
              </CardContent>
            </Card>
          ) : (
            meeting.decisions.map((decision) => (
              <Card key={decision.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">{decision.title}</h3>
                      <p className="text-gray-600 mt-1">{decision.description}</p>
                      {decision.reason && (
                        <p className="text-sm text-gray-500 mt-2">
                          <span className="font-medium">Reason:</span> {decision.reason}
                        </p>
                      )}
                    </div>
                    <StatusBadge status={decision.status} />
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      {activeTab === "qa" && (
        <Card>
          <CardContent className="p-6">
            <div className="mb-6">
              <h3 className="font-medium text-gray-900 mb-2">
                Ask a question about this meeting
              </h3>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={qaQuestion}
                  onChange={(e) => setQaQuestion(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleAskQuestion()}
                  placeholder="e.g., What did Ram agree to do?"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <Button onClick={handleAskQuestion} loading={qaLoading}>
                  {qaLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Ask"}
                </Button>
              </div>
            </div>

            {qaAnswer && (
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-start gap-3">
                  <Brain className="w-5 h-5 text-blue-600 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-blue-900 mb-1">AI Answer</h4>
                    <p className="text-blue-800">{qaAnswer}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="mt-6 pt-6 border-t border-gray-200">
              <h4 className="font-medium text-gray-900 mb-3">Suggested Questions</h4>
              <div className="flex flex-wrap gap-2">
                {[
                  "What did Ram agree to do?",
                  "Why was the launch postponed?",
                  "What are the unresolved issues?",
                  "Who has the most tasks?",
                ].map((q) => (
                  <button
                    key={q}
                    onClick={() => setQaQuestion(q)}
                    className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default function MeetingDetailPage() {
  return (
    <AuthWrapper>
      <MeetingDetailContent />
    </AuthWrapper>
  );
}
