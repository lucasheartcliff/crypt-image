import numpy as np
import pytest
from src.cryptography import Cryptography
from src.steganography import Steganography, SteganographyException


def make_image(width: int = 100, height: int = 100, channels: int = 3) -> np.ndarray:
    """Create a random test image."""
    return np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)


class TestSteganography:
    def test_encode_decode_text_roundtrip(self):
        crypto = Cryptography("testkey")
        img = make_image(200, 200)
        steg_enc = Steganography(img.copy(), crypto)
        encoded_img = steg_enc.encode_text("Hello, steganography!")

        steg_dec = Steganography(encoded_img, crypto)
        decoded = steg_dec.decode_text()
        assert decoded == "Hello, steganography!"

    def test_encode_decode_binary_roundtrip(self):
        crypto = Cryptography("testkey")
        data = b"\x00\x01\x02\xff" * 50

        img = make_image(200, 200)
        steg_enc = Steganography(img.copy(), crypto)
        enc_data = crypto.encrypt(data)
        encoded_img = steg_enc.encode_binary(enc_data)

        steg_dec = Steganography(encoded_img, crypto)
        dec_data = steg_dec.decode_binary()
        assert crypto.decrypt(dec_data) == data

    def test_capacity_bytes(self):
        img = make_image(100, 100, 3)
        crypto = Cryptography("key")
        steg = Steganography(img, crypto)
        # 100 * 100 * 3 * 8 bits / 8 = 30000 bytes - 8 header bytes
        assert steg.capacity_bytes() == 29992

    def test_image_too_small_raises_exception(self):
        crypto = Cryptography("key")
        img = make_image(2, 2, 3)  # Very small image
        steg = Steganography(img, crypto)

        large_data = b"x" * (steg.capacity_bytes() + 100)
        with pytest.raises(SteganographyException, match="not big enough"):
            steg.encode_binary(large_data)

    def test_progress_callback_called(self):
        crypto = Cryptography("key")
        img = make_image(200, 200)
        steg = Steganography(img.copy(), crypto)

        progress_calls = []
        enc_data = crypto.encrypt("test data for progress")
        steg.encode_binary(enc_data, progress_callback=lambda cur, tot: progress_calls.append((cur, tot)))

        assert len(progress_calls) > 0
        last_cur, last_tot = progress_calls[-1]
        assert last_cur == last_tot

    def test_decode_progress_callback_called(self):
        crypto = Cryptography("key")
        img = make_image(200, 200)
        steg_enc = Steganography(img.copy(), crypto)
        encoded_img = steg_enc.encode_text("test progress decoding")

        progress_calls = []
        steg_dec = Steganography(encoded_img, crypto)
        enc_text = steg_dec.decode_binary(
            progress_callback=lambda cur, tot: progress_calls.append((cur, tot))
        )

        assert len(progress_calls) > 0

    def test_empty_text(self):
        crypto = Cryptography("key")
        img = make_image(200, 200)
        steg_enc = Steganography(img.copy(), crypto)
        encoded_img = steg_enc.encode_text("")

        steg_dec = Steganography(encoded_img, crypto)
        assert steg_dec.decode_text() == ""

    def test_long_text(self):
        crypto = Cryptography("key")
        img = make_image(500, 500)
        text = "A" * 5000
        steg_enc = Steganography(img.copy(), crypto)
        encoded_img = steg_enc.encode_text(text)

        steg_dec = Steganography(encoded_img, crypto)
        assert steg_dec.decode_text() == text
