import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] gap-12">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold tracking-tight">
          <span className="text-primary-400">Crypt</span> Image
        </h1>
        <p className="text-lg text-gray-400 max-w-lg mx-auto">
          Hide encrypted messages inside images using AES-256 encryption and LSB
          steganography. Your secrets stay invisible.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-2xl">
        <Link
          href="/encode"
          className="group rounded-xl border border-gray-800 bg-gray-900/50 p-8 hover:border-primary-500/50 hover:bg-gray-900 transition-all"
        >
          <div className="text-3xl mb-4">&#128274;</div>
          <h2 className="text-xl font-semibold mb-2 group-hover:text-primary-400 transition-colors">
            Encode
          </h2>
          <p className="text-sm text-gray-400">
            Upload an image and hide your secret message or file inside it.
            Protected with AES-256 encryption.
          </p>
        </Link>

        <Link
          href="/decode"
          className="group rounded-xl border border-gray-800 bg-gray-900/50 p-8 hover:border-primary-500/50 hover:bg-gray-900 transition-all"
        >
          <div className="text-3xl mb-4">&#128275;</div>
          <h2 className="text-xl font-semibold mb-2 group-hover:text-primary-400 transition-colors">
            Decode
          </h2>
          <p className="text-sm text-gray-400">
            Extract and decrypt hidden data from a steganographic image using
            your passphrase.
          </p>
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-8 text-center text-sm text-gray-500 max-w-2xl">
        <div>
          <div className="text-2xl mb-1">&#128737;&#65039;</div>
          <div className="font-medium text-gray-300">AES-256 + PBKDF2</div>
          <div>Military-grade encryption</div>
        </div>
        <div>
          <div className="text-2xl mb-1">&#128065;&#65039;</div>
          <div className="font-medium text-gray-300">Invisible</div>
          <div>Undetectable to the naked eye</div>
        </div>
        <div>
          <div className="text-2xl mb-1">&#9989;</div>
          <div className="font-medium text-gray-300">HMAC Verified</div>
          <div>Tamper-proof integrity checks</div>
        </div>
      </div>
    </div>
  );
}
