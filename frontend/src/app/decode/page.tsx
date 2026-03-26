"use client";

import { useState } from "react";
import ImageUploader from "@/components/ImageUploader";
import KeyManager from "@/components/KeyManager";
import ProgressBar from "@/components/ProgressBar";
import { decode } from "@/lib/api";

export default function DecodePage() {
  const [image, setImage] = useState<File | null>(null);
  const [key, setKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDecode = async () => {
    if (!image || !key) return;
    setLoading(true);
    setProgress(20);
    setError(null);
    setResult(null);

    try {
      setProgress(50);
      const data = await decode(image, key);
      setResult(data.text);
      setProgress(100);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        "Decoding failed. Wrong key or not a steganographic image.";
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result) navigator.clipboard.writeText(result);
  };

  const handleDownloadText = () => {
    if (!result) return;
    const blob = new Blob([result], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "decoded.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Decode</h1>
        <p className="text-gray-400 mt-1">
          Extract hidden data from a steganographic image
        </p>
      </div>

      {/* Step 1: Image */}
      <section className="space-y-3">
        <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
          1. Encoded Image
        </h2>
        <ImageUploader
          onFileSelect={(file) => {
            setImage(file);
            setResult(null);
            setError(null);
          }}
          label="Drop the encoded image here"
        />
      </section>

      {/* Step 2: Key */}
      <section className="space-y-3">
        <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
          2. Passphrase
        </h2>
        <KeyManager value={key} onChange={setKey} />
      </section>

      {/* Decode Button */}
      <button
        onClick={handleDecode}
        disabled={!image || !key || loading}
        className="w-full rounded-lg bg-primary-600 py-3 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Decoding..." : "Decode"}
      </button>

      {loading && <ProgressBar progress={progress} label="Decoding..." />}

      {error && (
        <div className="rounded-lg border border-red-800 bg-red-950/50 p-4 text-sm text-red-300">
          {error}
        </div>
      )}

      {/* Result */}
      {result !== null && (
        <section className="space-y-3">
          <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
            Decoded Content
          </h2>
          <div className="rounded-lg border border-gray-700 bg-gray-900 p-4">
            <pre className="whitespace-pre-wrap text-sm text-gray-200 max-h-96 overflow-y-auto">
              {result}
            </pre>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="rounded-lg border border-gray-700 bg-gray-800 px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 transition-colors"
            >
              Copy to Clipboard
            </button>
            <button
              onClick={handleDownloadText}
              className="rounded-lg border border-primary-600 bg-primary-600/10 px-4 py-2 text-sm text-primary-400 hover:bg-primary-600/20 transition-colors"
            >
              Download as File
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
