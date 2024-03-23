import unittest
from src.cryptography import Cryptography

class TestCryptography(unittest.TestCase):
    def setUp(self):
        private_key, public_key = Cryptography.generate_rsa_key_pair()

        # Create Cryptography object with the provided RSA key
        self.crypto = Cryptography(private_key,public_key)

    def test_encrypt_decrypt(self):
        # Test encryption and decryption
        message = "Hello, this is a secret message!"
        encrypted_message = self.crypto.encrypt(message)
        decrypted_message = self.crypto.decrypt(encrypted_message)
        self.assertEqual(decrypted_message, message)