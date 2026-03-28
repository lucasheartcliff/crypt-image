# Snap Vault

Hide encrypted messages inside images using AES-256 encryption and LSB steganography.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)

## Features

- **AES-256 encryption** with PBKDF2 key derivation (600,000 iterations)
- **HMAC-SHA256 integrity** verification (encrypt-then-MAC)
- **LSB steganography** across 8 bit planes per channel
- **CLI tool** for quick encode/decode operations
- **REST API** powered by FastAPI with automatic OpenAPI docs
- **Web UI** built with Next.js, React, and Tailwind CSS
- **Docker** support for one-command deployment
- **Backward compatible** with v1 encrypted format

## Architecture

```
                    +-------------------+
                    |    Web UI         |
                    |  (Next.js :3000)  |
                    +--------+----------+
                             |
                             v
+-------------+    +-------------------+
|   CLI       |--->|    Core Engine     |
| (main.py)   |    | - Cryptography    |
+-------------+    | - Steganography   |
                    +--------+----------+
                             ^
                             |
                    +-------------------+
                    |    REST API       |
                    | (FastAPI :8000)   |
                    +-------------------+
```

The cryptography and steganography modules are shared between the CLI, API, and web interface.

## Project Structure

```
snap-vault/
├── main.py                        # CLI entry point
├── src/
│   ├── cryptography.py            # AES-256 + PBKDF2 + HMAC module
│   └── steganography.py           # LSB steganography module
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                # FastAPI application
│       ├── api/routes.py          # API endpoints
│       ├── core/                  # Core modules (backend copy)
│       └── models/schemas.py      # Pydantic models
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── app/                   # Next.js pages (home, encode, decode)
│       ├── components/            # React components
│       └── lib/                   # API client & utilities
├── cli/main.py                    # CLI wrapper using backend modules
├── tests/
│   ├── test_cryptography.py       # 11 crypto tests
│   └── test_steganography.py      # 8 steganography tests
├── docker-compose.yml
├── example/                       # Sample files for testing
└── requirements/requirements.txt  # CLI dependencies
```

## Quick Start

### Prerequisites

- Python 3.11+ (CLI and backend)
- Node.js 20+ (frontend)
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (recommended)

```bash
git clone https://github.com/lucasheartcliff/snap-vault.git
cd snap-vault
docker-compose up
```

- Web UI: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/requirements.txt

# Frontend
cd frontend
npm install
```

## CLI Usage

### Encode

Hide a text file inside an image:

```bash
python3 main.py encode -i <input_image> -o <output_image> -f <secret_file> -k <key_file>
```

**Example:**

```bash
python3 main.py encode -i example/th.jpeg -o output.png -f example/test_txt -k example/key.file
```

### Decode

Extract hidden data from an image:

```bash
python3 main.py decode -i <encoded_image> -o <output_file> -k <key_file>
```

**Example:**

```bash
python3 main.py decode -i output.png -o decoded.txt -k example/key.file
```

### Options

| Flag | Description |
|------|-------------|
| `-i, --in` | Input image (carrier for encode, encoded for decode) |
| `-o, --out` | Output file (encoded image or decoded text) |
| `-f, --file` | File to hide (encode only) |
| `-k, --key` | Key file containing the passphrase (max 32 characters) |

> **Note:** If the output format is JPEG/JPG, it will be automatically converted to PNG since lossy formats destroy steganographic data.

## Web UI

Start the backend and frontend separately for development:

```bash
# Terminal 1: Backend API
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open http://localhost:3000 to access the web interface.

### Pages

- **Home** (`/`) - Overview with links to encode and decode
- **Encode** (`/encode`) - Upload carrier image, enter secret text or file, set passphrase, download encoded image with side-by-side preview
- **Decode** (`/decode`) - Upload encoded image, enter passphrase, view or download decoded content

## API Reference

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/encode` | Hide data in an image |
| POST | `/api/decode` | Extract data from an image |
| POST | `/api/capacity` | Check image hiding capacity |
| POST | `/api/generate-key` | Generate a random key |
| GET | `/api/health` | Health check |

Interactive API docs available at http://localhost:8000/docs (Swagger UI).

### POST `/api/encode`

Encode secret data into a carrier image.

**Request** (multipart/form-data):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | File | Yes | Carrier image (PNG, JPEG, BMP) |
| `key` | String | Yes | Encryption passphrase (max 32 chars) |
| `text` | String | No | Text to hide (provide `text` OR `secret_file`) |
| `secret_file` | File | No | File to hide |

**Response:** `image/png` binary (encoded image download)

**Errors:** `400` invalid input or capacity exceeded, `413` file too large (max 50MB)

### POST `/api/decode`

Decode hidden data from a steganographic image.

**Request** (multipart/form-data):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | File | Yes | Encoded image |
| `key` | String | Yes | Decryption passphrase |

**Response:**

```json
{ "text": "decoded secret message" }
```

**Errors:** `400` wrong key, corrupted data, or invalid image

### POST `/api/capacity`

Check how much data can be hidden in an image.

**Request** (multipart/form-data): `image` (File)

**Response:**

```json
{
  "max_bytes": 504802,
  "max_kb": 492.97,
  "dimensions": "411x410"
}
```

### POST `/api/generate-key`

Generate a random base64-encoded encryption key.

**Response:**

```json
{ "key": "YTJiM2M0ZDVlNmY3ZzhoOQ==" }
```

### GET `/api/health`

```json
{ "status": "ok", "version": "2.0.0" }
```

## Security

### Encryption

- **Algorithm:** AES-256 in CFB (Cipher Feedback) mode
- **Key Derivation:** PBKDF2 with HMAC-SHA256 PRF, 600,000 iterations, random 16-byte salt
- **Integrity:** HMAC-SHA256 computed over IV + ciphertext (encrypt-then-MAC pattern)
- **IV:** Random 16 bytes generated per encryption operation

### Encrypted Data Format (v2)

```
+--------+------+----+------------+------+
| VER(1) | SALT | IV | CIPHERTEXT | HMAC |
| 0x02   | 16B  |16B | variable   | 32B  |
+--------+------+----+------------+------+
```

- **VER:** Version byte (`0x02`) identifies the format
- **SALT:** Random salt for PBKDF2 key derivation
- **IV:** Random initialization vector for AES-CFB
- **CIPHERTEXT:** AES-256-CFB encrypted data
- **HMAC:** SHA-256 HMAC over (IV + CIPHERTEXT) for tamper detection

The decryptor verifies HMAC before attempting decryption. If verification fails, an `IntegrityError` is raised (wrong key or tampered data).

### Backward Compatibility

Images encoded with v1 (no version byte prefix) are still decodable. The decryptor detects the absence of `0x02` and falls back to legacy decryption.

## How It Works

### LSB Steganography

Data is hidden in the **Least Significant Bits** of image pixel values. Each pixel has 3 color channels (RGB), and each channel uses 8 bits. By modifying only the least significant bit, visual changes are imperceptible.

The encoder progresses through the image in this order:
1. Channels (R, G, B) of each pixel
2. Pixels left-to-right across each row
3. Rows top-to-bottom
4. If the first bit plane fills up, move to the second bit plane, and so on (up to 8)

### Capacity

The maximum data that can be hidden in an image:

```
capacity = (width x height x channels x 8) / 8 - 8 bytes (header)
```

For example, a 1920x1080 RGB image can hold approximately **6.2 MB** of encrypted data.

The first 64 bits (8 bytes) store the data length as a header, followed by the encrypted payload.

## Testing

```bash
source .venv/bin/activate
pip install pytest
pytest tests/ -v
```

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| Cryptography | 11 | Roundtrip, IV uniqueness, HMAC verification, key validation, unicode, binary data, tampering detection |
| Steganography | 8 | Roundtrip (text + binary), capacity calculation, overflow detection, progress callbacks, empty/long text |

## Docker

### Build and Run

```bash
docker-compose up --build
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| `backend` | 8000 | FastAPI + Uvicorn |
| `frontend` | 3000 | Next.js (standalone) |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend URL for frontend |
| `PYTHONPATH` | `/app` | Python module resolution path |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest tests/ -v`)
5. Commit and push your branch
6. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.
