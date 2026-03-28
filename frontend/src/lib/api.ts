import axios from "axios";

// Empty string = relative URLs, routed through Next.js /api/* rewrites.
// Set NEXT_PUBLIC_API_URL to override (e.g. direct backend access).
const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export async function encode(
  image: File,
  key: string,
  text?: string,
  file?: File
): Promise<Blob> {
  const form = new FormData();
  form.append("image", image);
  form.append("key", key);
  if (text !== undefined) form.append("text", text);
  if (file !== undefined) form.append("secret_file", file);

  const response = await axios.post(`${BASE_URL}/api/encode`, form, {
    responseType: "blob",
  });
  return response.data as Blob;
}

export async function decode(
  image: File,
  key: string
): Promise<{ text: string }> {
  const form = new FormData();
  form.append("image", image);
  form.append("key", key);

  const response = await axios.post(`${BASE_URL}/api/decode`, form);
  return response.data as { text: string };
}

export async function getCapacity(
  file: File
): Promise<{ max_bytes: number; dimensions: string }> {
  const form = new FormData();
  form.append("image", file);

  const response = await axios.post(`${BASE_URL}/api/capacity`, form);
  return response.data as { max_bytes: number; dimensions: string };
}

export async function generateKey(): Promise<string> {
  const response = await axios.post(`${BASE_URL}/api/generate-key`);
  return (response.data as { key: string }).key;
}
