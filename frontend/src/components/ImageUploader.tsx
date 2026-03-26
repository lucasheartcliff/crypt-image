"use client";

import { useCallback, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface ImageUploaderProps {
  onFileSelect: (file: File) => void;
  label?: string;
  accept?: string;
}

export default function ImageUploader({
  onFileSelect,
  label = "Drop an image here or click to browse",
  accept = "image/*",
}: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(
    (file: File) => {
      setFileName(file.name);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target?.result as string);
      reader.readAsDataURL(file);
      onFileSelect(file);
    },
    [onFileSelect]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={cn(
        "relative cursor-pointer rounded-lg border-2 border-dashed p-8 text-center transition-all",
        isDragging
          ? "border-primary-400 bg-primary-950/20"
          : "border-gray-700 hover:border-gray-500 bg-gray-900/30",
        preview && "p-4"
      )}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />

      {preview ? (
        <div className="space-y-3">
          <img
            src={preview}
            alt="Preview"
            className="mx-auto max-h-48 rounded-md object-contain"
          />
          <p className="text-sm text-gray-400">{fileName}</p>
        </div>
      ) : (
        <div className="space-y-2">
          <div className="text-4xl text-gray-600">&#128444;&#65039;</div>
          <p className="text-sm text-gray-400">{label}</p>
        </div>
      )}
    </div>
  );
}
