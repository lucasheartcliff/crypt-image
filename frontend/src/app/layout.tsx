import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Crypt Image - Steganography Tool",
  description: "Encrypt and hide data inside images using steganography",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
          <div className="mx-auto max-w-5xl px-4 py-4 flex items-center justify-between">
            <a href="/" className="text-xl font-bold text-primary-400">
              Crypt Image
            </a>
            <div className="flex gap-4">
              <a
                href="/encode"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Encode
              </a>
              <a
                href="/decode"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Decode
              </a>
            </div>
          </div>
        </nav>
        <main className="mx-auto max-w-5xl px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
