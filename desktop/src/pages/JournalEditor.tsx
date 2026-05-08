import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { invoke } from "@tauri-apps/api/core";
import { Save, ArrowLeft, Loader2 } from "lucide-react";

export default function JournalEditor() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [content, setContent] = useState("");
  const [mood, setMood] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  const moods = [
    { emoji: "😊", label: "Joyful", color: "bg-yellow-500/20" },
    { emoji: "🙏", label: "Grateful", color: "bg-green-500/20" },
    { emoji: "😔", label: "Heavy", color: "bg-blue-500/20" },
    { emoji: "🤔", label: "Reflective", color: "bg-purple-500/20" },
    { emoji: "⚡", label: "Inspired", color: "bg-orange-500/20" },
  ];

  // Autosave
  useEffect(() => {
    const timer = setTimeout(() => {
      if (content.trim()) {
        handleSave();
      }
    }, 3000);

    return () => clearTimeout(timer);
  }, [content, mood]);

  const handleSave = async () => {
    if (!content.trim() || isSaving) return;

    setIsSaving(true);
    try {
      await invoke("create_journal_entry", {
        content,
        mood,
        tags: [],
      });
      setLastSaved(new Date());
    } catch (err) {
      console.error("Failed to save:", err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h1 className="text-xl font-semibold">
              {id ? "Edit Entry" : "New Entry"}
            </h1>
            {lastSaved && (
              <p className="text-sm text-gray-400">
                Saved {lastSaved.toLocaleTimeString()}
              </p>
            )}
          </div>
        </div>

        <button
          onClick={handleSave}
          disabled={isSaving || !content.trim()}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 rounded-lg font-medium disabled:opacity-50"
        >
          {isSaving ? (
            <Loader2 className="animate-spin" size={18} />
          ) : (
            <Save size={18} />
          )}
          Save
        </button>
      </div>

      {/* Mood Selector */}
      <div className="flex gap-2 mb-4">
        {moods.map((m) => (
          <button
            key={m.label}
            onClick={() => setMood(mood === m.label ? null : m.label)}
            className={`px-3 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              mood === m.label
                ? m.color + " ring-2 ring-white/50"
                : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            <span>{m.emoji}</span>
            <span className="text-sm">{m.label}</span>
          </button>
        ))}
      </div>

      {/* Editor */}
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your thoughts, prayers, reflections..."
        className="flex-1 bg-gray-800 rounded-lg p-4 resize-none focus:outline-none focus:ring-2 focus:ring-brand-500 font-mono text-sm leading-relaxed"
        style={{ minHeight: "400px" }}
      />

      {/* Footer */}
      <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
        <span>{content.length} characters</span>
        <span>Markdown supported</span>
      </div>
    </div>
  );
}
