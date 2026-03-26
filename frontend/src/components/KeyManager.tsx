"use client";

import { useState } from "react";
import { generateKey } from "@/lib/api";

interface KeyManagerProps {
  value: string;
  onChange: (key: string) => void;
}

export default function KeyManager({ value, onChange }: KeyManagerProps) {
  const [visible, setVisible] = useState(false);
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const key = await generateKey();
      onChange(key);
    } catch {
      alert("Failed to generate key. Is the backend running?");
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(value);
  };

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-300">
        Passphrase
      </label>
      <div className="flex gap-2">
        <div className="relative flex-1">
          <input
            type={visible ? "text" : "password"}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Enter your passphrase..."
            maxLength={32}
            className="w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-2.5 pr-10 text-sm text-gray-100 placeholder-gray-500 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          />
          <button
            type="button"
            onClick={() => setVisible(!visible)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
            title={visible ? "Hide" : "Show"}
          >
            {visible ? "\u{1F441}" : "\u{1F512}"}
          </button>
        </div>
        <button
          type="button"
          onClick={handleGenerate}
          disabled={generating}
          className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-xs text-gray-300 hover:bg-gray-700 disabled:opacity-50 transition-colors whitespace-nowrap"
        >
          {generating ? "..." : "Generate"}
        </button>
        {value && (
          <button
            type="button"
            onClick={handleCopy}
            className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-xs text-gray-300 hover:bg-gray-700 transition-colors"
            title="Copy to clipboard"
          >
            &#128203;
          </button>
        )}
      </div>
      {value && (
        <p className="text-xs text-gray-500">
          {value.length}/32 characters
        </p>
      )}
    </div>
  );
}
