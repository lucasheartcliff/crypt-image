import unittest
import numpy as np
from src.steganography import Steganography, Cryptography

class TestSteganography(unittest.TestCase):
    def test_encode_decode_text(self):
        # Generate RSA key pair
        private_key, public_key = Cryptography.generate_rsa_key_pair()

        # Initialize Cryptography object
        crypto = Cryptography(private_key, public_key)

        # Initialize Steganography object
        image = np.zeros((10, 10, 3), dtype=np.uint8)  # Dummy image
        steganography = Steganography(image, crypto)

        # Message to encode
        message = "Hello, this is a secret message!"

        # Encode and then decode the message
        encoded_image = steganography.encode_text(message)
        steganography = Steganography(encoded_image, crypto)
        decoded_message = steganography.decode_text()

        # Check if the decoded message matches the original message
        self.assertEqual(decoded_message, message)
