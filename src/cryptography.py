from Crypto.Cipher import AES
from Crypto import Random

class Cryptography():
    def __init__(self, key: str):
        iv = 16 * "j"

        remaining_char_len = 32 - len(key)
        
        if remaining_char_len <0: raise "Private Key should not be greater 32 characters"

        i =0
        n_key = key
        while i< remaining_char_len:
            n_key = n_key + "0"
            i+=1
        
        encoded_key = n_key.encode("utf-8")
        self.cipher = AES.new(encoded_key, AES.MODE_CFB,iv)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode("utf-8"))

    def decrypt(self, encrypted_text):
        text = self.cipher.decrypt(encrypted_text).decode("utf-8")
        return text
