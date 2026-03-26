"use client";

import { useState } from "react";
import ImageUploader from "@/components/ImageUploader";
import KeyManager from "@/components/KeyManager";
import ProgressBar from "@/components/ProgressBar";
import { encode, getCapacity } from "@/lib/api";
import { formatBytes } from "@/lib/utils";

type InputMode = "text" | "file";

export default function EncodePage() {
  const [image, setImage] = useState<File | null>(null);
  const [key, setKey] = useState("");
  const [inputMode, setInputMode] = useState<InputMode>("text");
  const [text, setText] = useState("");
  const [secretFile, setSecretFile] = useState<File | null>(null);
  const [capacity, setCapacity] = useState<{
    max_bytes: number;
    dimensions: string;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<string | null>(null);
  const [resultBlob, setResultBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = async (file: File) => {
    setImage(file);
    setResult(null);
    setError(null);
    try {
      const cap = await getCapacity(file);
      setCapacity(cap);
    } catch {
      setCapacity(null);
    }
  };

  const dataSize = inputMode === "text" ? new Blob([text]).size : (secretFile?.size || 0);

  const handleEncode = async () => {
    if (!image || !key) return;
    setLoading(true);
    setProgress(10);
    setError(null);
    setResult(null);

    try {
      setProgress(30);
      const blob = await encode(
        image,
        key,
        inputMode === "text" ? text : undefined,
        inputMode === "file" ? secretFile || undefined : undefined
      );
      setProgress(90);
      const url = URL.createObjectURL(blob);
      setResult(url);
      setResultBlob(blob);
      setProgress(100);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Encoding failed. Is the backend running?";
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;
    const a = document.createElement("a");
    a.href = result;
    a.download = "encoded.png";
    a.click();
  };

  const canEncode =
    image && key && (inputMode === "text" ? text.length > 0 : !!secretFile);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Encode</h1>
        <p className="text-gray-400 mt-1">
          Hide secret data inside an image
        </p>
      </div>

      {/* Step 1: Image */}
      <section className="space-y-3">
        <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
          1. Carrier Image
        </h2>
        <ImageUploader onFileSelect={handleImageSelect} />
        {capacity && (
          <p className="text-xs text-gray-500">
            {capacity.dimensions} &middot; Capacity:{" "}
            {formatBytes(capacity.max_bytes)}
          </p>
        )}
      </section>

      {/* Step 2: Secret Data */}
      <section className="space-y-3">
        <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
          2. Secret Data
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => setInputMode("text")}
            className={`rounded-lg px-4 py-2 text-sm transition-colors ${
              inputMode === "text"
                ? "bg-primary-600 text-white"
                : "bg-gray-800 text-gray-400 hover:text-white"
            }`}
          >
            Text
          </button>
          <button
            onClick={() => setInputMode("file")}
            className={`rounded-lg px-4 py-2 text-sm transition-colors ${
              inputMode === "file"
                ? "bg-primary-600 text-white"
                : "bg-gray-800 text-gray-400 hover:text-white"
            }`}
          >
            File
          </button>
        </div>

        {inputMode === "text" ? (
          <div className="space-y-1">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type your secret message..."
              rows={5}
              className="w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 resize-y"
            />
            <p className="text-xs text-gray-500">
              {formatBytes(dataSize)}
              {capacity && ` / ${formatBytes(capacity.max_bytes)}`}
            </p>
          </div>
        ) : (
          <div className="space-y-1">
            <input
              type="file"
              onChange={(e) => setSecretFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-400 file:mr-4 file:rounded-lg file:border-0 file:bg-gray-800 file:px-4 file:py-2 file:text-sm file:text-gray-300 hover:file:bg-gray-700"
            />
            {secretFile && (
              <p className="text-xs text-gray-500">
                {secretFile.name} &middot; {formatBytes(secretFile.size)}
                {capacity && ` / ${formatBytes(capacity.max_bytes)}`}
              </p>
            )}
          </div>
        )}
      </section>

      {/* Step 3: Key */}
      <section className="space-y-3">
        <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
          3. Passphrase
        </h2>
        <KeyManager value={key} onChange={setKey} />
      </section>

      {/* Encode Button */}
      <button
        onClick={handleEncode}
        disabled={!canEncode || loading}
        className="w-full rounded-lg bg-primary-600 py-3 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Encoding..." : "Encode"}
      </button>

      {loading && <ProgressBar progress={progress} label="Encoding..." />}

      {error && (
        <div className="rounded-lg border border-red-800 bg-red-950/50 p-4 text-sm text-red-300">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <section className="space-y-4">
          <h2 className="text-sm font-medium text-gray-300 uppercase tracking-wider">
            Result
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <p className="text-xs text-gray-500">Original</p>
              {image && (
                <img
                  src={URL.createObjectURL(image)}
                  alt="Original"
                  className="rounded-lg border border-gray-800 max-h-64 object-contain w-full"
                />
              )}
            </div>
            <div className="space-y-2">
              <p className="text-xs text-gray-500">
                Encoded{resultBlob && ` (${formatBytes(resultBlob.size)})`}
              </p>
              <img
                src={result}
                alt="Encoded"
                className="rounded-lg border border-gray-800 max-h-64 object-contain w-full"
              />
            </div>
          </div>
          <button
            onClick={handleDownload}
            className="rounded-lg border border-primary-600 bg-primary-600/10 px-6 py-2.5 text-sm text-primary-400 hover:bg-primary-600/20 transition-colors"
          >
            Download Encoded Image
          </button>
        </section>
      )}
    </div>
  );
}
