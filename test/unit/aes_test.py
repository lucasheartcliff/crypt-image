
from src.aes import Encryptor
from src.string_utils import bytes_to_string, string_to_bytes

key = string_to_bytes("1234567890123456")

plain_text = "Example Text"

def test_encode():
    enc = Encryptor(key)
    enc_bytes = enc.encrypt(plain_text)
    assert enc_bytes != plain_text

def test_decode():
    cipher = b'\xf6\xc7\xa9\xd30\x89E!q^\xba\xd7\x00\xbc6T\xcd\x89U\xdd\xd0\xdf\x1d\xb9\x05\xac\xab9\xa6\xb8$\x93'
    
    enc = Encryptor(key)
    
    text = enc.decrypt(cipher)
    
    assert text == plain_text
