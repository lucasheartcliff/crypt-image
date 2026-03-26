import pytest
from src.cryptography import Cryptography, IntegrityError


class TestCryptography:
    def test_encrypt_decrypt_roundtrip(self):
        crypto = Cryptography("testkey123")
        plaintext = "Hello, World!"
        encrypted = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt_text(encrypted)
        assert decrypted == plaintext

    def test_encrypt_produces_different_ciphertext_each_time(self):
        crypto = Cryptography("testkey123")
        enc1 = crypto.encrypt("same text")
        enc2 = crypto.encrypt("same text")
        # Random salt + IV means different ciphertext each time
        assert enc1 != enc2

    def test_decrypt_with_wrong_key_raises_integrity_error(self):
        crypto1 = Cryptography("correctkey")
        crypto2 = Cryptography("wrongkey")
        encrypted = crypto1.encrypt("secret data")
        with pytest.raises(IntegrityError):
            crypto2.decrypt(encrypted)

    def test_key_too_long_raises_value_error(self):
        with pytest.raises(ValueError, match="must not exceed 32 characters"):
            Cryptography("a" * 33)

    def test_max_length_key_works(self):
        crypto = Cryptography("a" * 32)
        encrypted = crypto.encrypt("test")
        assert crypto.decrypt_text(encrypted) == "test"

    def test_short_key_works(self):
        crypto = Cryptography("x")
        encrypted = crypto.encrypt("test")
        assert crypto.decrypt_text(encrypted) == "test"

    def test_empty_string_encrypt_decrypt(self):
        crypto = Cryptography("key")
        encrypted = crypto.encrypt("")
        assert crypto.decrypt_text(encrypted) == ""

    def test_unicode_text(self):
        crypto = Cryptography("key")
        text = "Hello, World! Привет мир! 你好世界!"
        encrypted = crypto.encrypt(text)
        assert crypto.decrypt_text(encrypted) == text

    def test_binary_data(self):
        crypto = Cryptography("key")
        data = bytes(range(256))
        encrypted = crypto.encrypt(data)
        assert crypto.decrypt(encrypted) == data

    def test_version_byte_present(self):
        crypto = Cryptography("key")
        encrypted = crypto.encrypt("test")
        assert encrypted[0:1] == b"\x02"

    def test_tampered_data_raises_integrity_error(self):
        crypto = Cryptography("key")
        encrypted = bytearray(crypto.encrypt("test"))
        # Flip a byte in the ciphertext area
        encrypted[40] ^= 0xFF
        with pytest.raises(IntegrityError):
            crypto.decrypt(bytes(encrypted))
