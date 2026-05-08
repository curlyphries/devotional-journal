import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { invoke } from "@tauri-apps/api/core";
import { PenLine, BookOpen, Calendar, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

interface JournalEntry {
  id: string;
  content_preview: string;
  created_at: string;
}

export default function Dashboard() {
  const { data: entries, isLoading } = useQuery({
    queryKey: ["journal-entries"],
    queryFn: async () => {
      return invoke<JournalEntry[]>("get_journal_entries", {
        limit: 5,
        offset: 0,
      });
    },
  });

  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{today}</h1>
          <p className="text-gray-400">Welcome back to your devotional journey</p>
        </div>
        <div className="flex gap-3">
          <Link
            to="/journal"
            className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 rounded-lg font-medium"
          >
            <PenLine size={18} />
            New Entry
          </Link>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-orange-500/20 rounded-lg">
              <TrendingUp size={20} className="text-orange-400" />
            </div>
            <span className="text-sm text-gray-400">Current Streak</span>
          </div>
          <p className="text-2xl font-bold">12 days</p>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <BookOpen size={20} className="text-blue-400" />
            </div>
            <span className="text-sm text-gray-400">This Week</span>
          </div>
          <p className="text-2xl font-bold">5 entries</p>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-500/20 rounded-lg">
              <Calendar size={20} className="text-green-400" />
            </div>
            <span className="text-sm text-gray-400">Total Entries</span>
          </div>
          <p className="text-2xl font-bold">{entries?.length || 0}</p>
        </div>
      </div>

      {/* Recent Entries */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Recent Entries</h2>

        {isLoading ? (
          <div className="text-center py-8 text-gray-400">Loading...</div>
        ) : entries && entries.length > 0 ? (
          <div className="space-y-3">
            {entries.map((entry) => (
              <Link
                key={entry.id}
                to={`/journal/${entry.id}`}
                className="block p-4 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors"
              >
                <p className="text-gray-300 line-clamp-2 mb-2">
                  {entry.content_preview}
                </p>
                <p className="text-sm text-gray-500">
                  {new Date(entry.created_at).toLocaleDateString()}
                </p>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-400 mb-4">No entries yet</p>
            <Link
              to="/journal"
              className="text-brand-400 hover:text-brand-300"
            >
              Write your first entry →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
