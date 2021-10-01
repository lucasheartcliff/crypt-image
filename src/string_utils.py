import hashlib as hl

BIN_CODE = 'UTF-8'

def string_to_bytes(text: str):
    return text.encode(BIN_CODE)


def bytes_to_string(bytes:bytes):
    return bytes.decode(BIN_CODE)
