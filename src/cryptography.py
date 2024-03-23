from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

class Cryptography():
    def __init__(self, private_key: bytes, public_key: bytes):
        # Load provided RSA private key
        self.private_key = RSA.import_key(private_key)
        # Load provided RSA public key
        self.public_key = RSA.import_key(public_key)

        # Create cipher objects for encryption and decryption
        self.cipher_encrypt = PKCS1_OAEP.new(self.public_key)
        self.cipher_decrypt = PKCS1_OAEP.new(self.private_key)

    def encrypt(self, text):
        # Encrypt the text using RSA public key
        encrypted_text = self.cipher_encrypt.encrypt(text.encode("utf-8"))
        return encrypted_text

    def decrypt(self, encrypted_text):
        # Decrypt the text using RSA private key
        decrypted_text = self.cipher_decrypt.decrypt(encrypted_text).decode("utf-8")
        return decrypted_text
    
    def generate_rsa_key_pair():
        # Generate a new RSA key pair with the defined key size
        key = RSA.generate(4096)
        
        # Export the private key
        private_key = key.export_key()
        
        # Export the public key
        public_key = key.publickey().export_key()
        
        return private_key, public_key