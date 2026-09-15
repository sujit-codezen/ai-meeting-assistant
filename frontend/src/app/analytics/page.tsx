"use client";

import { AuthWrapper } from "@/components/AuthWrapper";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { BarChart3, TrendingUp, Calendar } from "lucide-react";
import { analyticsAPI } from "@/lib/api";

interface TrendData {
  date: string;
  count: number;
}

function AnalyticsContent() {
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analyticsAPI
      .getTrends(30)
      .then((res) => setTrends(res.data.meetings_by_day || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const maxCount = Math.max(...trends.map((t) => t.count), 1);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600">Insights and trends from your meetings.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">This Month</p>
                <p className="text-2xl font-bold text-gray-900">
                  {trends.reduce((sum, t) => sum + t.count, 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Daily Average</p>
                <p className="text-2xl font-bold text-gray-900">
                  {(trends.reduce((sum, t) => sum + t.count, 0) / 30).toFixed(1)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Peak Day</p>
                <p className="text-2xl font-bold text-gray-900">
                  {maxCount} meetings
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Meeting Activity (Last 30 Days)</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="h-64 bg-gray-200 rounded animate-pulse"></div>
          ) : (
            <div className="h-64 flex items-end gap-1">
              {trends.map((trend, i) => (
                <div
                  key={i}
                  className="flex-1 flex flex-col items-center"
                  title={`${trend.date}: ${trend.count} meetings`}
                >
                  <div
                    className="w-full bg-blue-500 rounded-t"
                    style={{
                      height: `${(trend.count / maxCount) * 100}%`,
                      minHeight: trend.count > 0 ? "4px" : "0",
                    }}
                  />
                </div>
              ))}
            </div>
          )}
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>30 days ago</span>
            <span>Today</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function AnalyticsPage() {
  return (
    <AuthWrapper>
      <AnalyticsContent />
    </AuthWrapper>
  );
}
