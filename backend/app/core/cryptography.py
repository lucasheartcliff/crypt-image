import os
import hmac
import hashlib
from typing import Optional
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

PBKDF2_ITERATIONS = 600_000
SALT_SIZE = 16
IV_SIZE = 16
HMAC_SIZE = 32
AES_KEY_SIZE = 32
HMAC_KEY_SIZE = 32
VERSION_BYTE = b"\x02"


class IntegrityError(Exception):
    """Raised when HMAC verification fails during decryption."""
    pass


class Cryptography:
    def __init__(self, key: str):
        if len(key) > 32:
            raise ValueError("Private key must not exceed 32 characters")
        self.passphrase = key

    def _derive_keys(self, salt: bytes) -> tuple[bytes, bytes]:
        derived = PBKDF2(
            self.passphrase,
            salt,
            dkLen=AES_KEY_SIZE + HMAC_KEY_SIZE,
            count=PBKDF2_ITERATIONS,
            prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest(),
        )
        aes_key = derived[:AES_KEY_SIZE]
        hmac_key = derived[AES_KEY_SIZE:]
        return aes_key, hmac_key

    def _compute_hmac(self, hmac_key: bytes, data: bytes) -> bytes:
        return hmac.new(hmac_key, data, hashlib.sha256).digest()

    def encrypt(self, data: bytes | str) -> bytes:
        if isinstance(data, str):
            data = data.encode("utf-8")

        salt = os.urandom(SALT_SIZE)
        iv = os.urandom(IV_SIZE)
        aes_key, hmac_key = self._derive_keys(salt)

        cipher = AES.new(aes_key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(data)

        # Encrypt-then-MAC: HMAC covers iv + ciphertext
        mac = self._compute_hmac(hmac_key, iv + ciphertext)

        # Format: VERSION(1) + salt(16) + iv(16) + ciphertext(N) + hmac(32)
        return VERSION_BYTE + salt + iv + ciphertext + mac

    def decrypt(self, encrypted_data: bytes) -> bytes:
        if encrypted_data[0:1] == VERSION_BYTE:
            return self._decrypt_v2(encrypted_data[1:])
        else:
            # Legacy format: iv(16) + ciphertext
            return self._decrypt_legacy(encrypted_data)

    def decrypt_text(self, encrypted_data: bytes) -> str:
        return self.decrypt(encrypted_data).decode("utf-8")

    def _decrypt_v2(self, data: bytes) -> bytes:
        salt = data[:SALT_SIZE]
        iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
        ciphertext = data[SALT_SIZE + IV_SIZE:-HMAC_SIZE]
        stored_mac = data[-HMAC_SIZE:]

        aes_key, hmac_key = self._derive_keys(salt)

        # Verify HMAC before decryption
        expected_mac = self._compute_hmac(hmac_key, iv + ciphertext)
        if not hmac.compare_digest(stored_mac, expected_mac):
            raise IntegrityError("HMAC verification failed: data may be corrupted or wrong key")

        cipher = AES.new(aes_key, AES.MODE_CFB, iv)
        return cipher.decrypt(ciphertext)

    def _decrypt_legacy(self, data: bytes) -> bytes:
        """Backward compatibility with v1 format (iv + ciphertext, no PBKDF2)."""
        iv = data[:IV_SIZE]
        ciphertext = data[IV_SIZE:]
        key = self.passphrase.encode("utf-8").ljust(32, b"\x00")
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.decrypt(ciphertext)
