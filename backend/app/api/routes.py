import base64
import io
import os

import cv2
import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from backend.app.core.cryptography import Cryptography, IntegrityError
from backend.app.core.steganography import Steganography, SteganographyException
from backend.app.models.schemas import (
    CapacityResponse,
    DecodeResponse,
    ErrorResponse,
    GenerateKeyResponse,
    HealthResponse,
)

router = APIRouter(prefix="/api")

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB


async def _read_image(file: UploadFile) -> np.ndarray:
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Could not decode image")
    return img


@router.post("/encode", responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}})
async def encode(
    image: UploadFile = File(..., description="Carrier image"),
    key: str = Form(..., description="Encryption passphrase"),
    text: str = Form(None, description="Text to hide (use this OR secret_file)"),
    secret_file: UploadFile = File(None, description="File to hide (use this OR text)"),
):
    """Encode secret data into an image using steganography."""
    if not text and not secret_file:
        raise HTTPException(status_code=400, detail="Provide either 'text' or 'secret_file'")

    img = await _read_image(image)

    try:
        crypto = Cryptography(key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    steg = Steganography(img, crypto)

    if text:
        data = text
    else:
        file_bytes = await secret_file.read()
        data = file_bytes.decode("utf-8")

    try:
        result_img = steg.encode_text(data)
    except SteganographyException as e:
        raise HTTPException(status_code=400, detail=str(e))

    _, buffer = cv2.imencode(".png", result_img)
    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=encoded.png"},
    )


@router.post("/decode", responses={400: {"model": ErrorResponse}})
async def decode(
    image: UploadFile = File(..., description="Encoded image"),
    key: str = Form(..., description="Decryption passphrase"),
):
    """Decode hidden data from a steganographic image."""
    img = await _read_image(image)

    try:
        crypto = Cryptography(key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    steg = Steganography(img, crypto)

    try:
        text = steg.decode_text()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Decryption failed: wrong key or corrupted data")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode text. The password might be wrong, or the data is not valid text.")
    except Exception as e:
        if "codec can't decode" in str(e):
            raise HTTPException(status_code=400, detail="Failed to decode text. The password might be wrong, or the image may not contain hidden data.")
        raise HTTPException(status_code=400, detail=f"Failed to extract data. The image might not contain a valid secret. (details: {str(e)})")

    return DecodeResponse(text=text)


@router.post("/capacity", response_model=CapacityResponse)
async def capacity(
    image: UploadFile = File(..., description="Image to check capacity"),
):
    """Check how much data can be hidden in an image."""
    img = await _read_image(image)
    crypto = Cryptography("dummy")
    steg = Steganography(img, crypto)

    max_bytes = steg.capacity_bytes()
    h, w = img.shape[:2]

    return CapacityResponse(
        max_bytes=max_bytes,
        max_kb=round(max_bytes / 1024, 2),
        dimensions=f"{w}x{h}",
    )


@router.post("/generate-key", response_model=GenerateKeyResponse)
async def generate_key():
    """Generate a random encryption key."""
    key_bytes = os.urandom(24)
    key = base64.b64encode(key_bytes).decode("ascii")
    return GenerateKeyResponse(key=key)


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="ok", version="2.0.0")
