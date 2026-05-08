import { useState } from "react";
import { BookOpen, Search, ChevronLeft, ChevronRight } from "lucide-react";

const SAMPLE_PASSAGE = {
  reference: "John 3:16-17",
  verses: [
    { number: 16, text: "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life." },
    { number: 17, text: "For God sent not his Son into the world to condemn the world; but that the world through him might be saved." },
  ],
};

export default function Reader() {
  const [reference, setReference] = useState("John 3:16");

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-800 rounded-lg border border-gray-700 focus:border-brand-500 focus:outline-none"
            placeholder="Enter reference (e.g., Genesis 1:1)"
          />
        </div>

        <div className="flex gap-2">
          <button className="p-2 hover:bg-gray-700 rounded-lg">
            <ChevronLeft size={20} />
          </button>
          <button className="p-2 hover:bg-gray-700 rounded-lg">
            <ChevronRight size={20} />
          </button>
        </div>
      </div>

      {/* Passage */}
      <div className="flex-1 bg-gray-800 rounded-lg p-6 overflow-auto">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <BookOpen size={18} className="text-brand-400" />
          {SAMPLE_PASSAGE.reference}
        </h2>

        <div className="space-y-4 leading-relaxed text-lg">
          {SAMPLE_PASSAGE.verses.map((verse) => (
            <p key={verse.number} className="flex gap-2">
              <sup className="text-brand-400 text-sm mt-1">{verse.number}</sup>
              <span>{verse.text}</span>
            </p>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="mt-4 flex gap-3">
        <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm">
          Highlight
        </button>
        <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm">
          Add Note
        </button>
        <button className="px-4 py-2 bg-brand-600 hover:bg-brand-500 rounded-lg text-sm ml-auto">
          Journal This Passage
        </button>
      </div>
    </div>
  );
}
