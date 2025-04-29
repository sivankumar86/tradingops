import hashlib
import base64


def derive_key(password: str, length: int) -> bytes:
    """Derive a key from the password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).digest()[:length]


def xor_encrypt(plaintext: str, password: str) -> str:
    """Encrypt plaintext with password using XOR."""
    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    # Derive key with same length as plaintext
    key = derive_key(password, len(plaintext_bytes))

    # XOR plaintext with key
    ciphertext = bytes(a ^ b for a, b in zip(plaintext_bytes, key))

    # Encode to base64 for safe storage
    return base64.b64encode(ciphertext).decode('utf-8')


def xor_decrypt(ciphertext: str, password: str) -> str:
    """Decrypt ciphertext with password using XOR."""
    # Decode base64
    ciphertext_bytes = base64.b64decode(ciphertext)

    # Derive key with same length as ciphertext
    key = derive_key(password, len(ciphertext_bytes))

    # XOR ciphertext with key to recover plaintext
    plaintext_bytes = bytes(a ^ b for a, b in zip(ciphertext_bytes, key))

    return plaintext_bytes.decode('utf-8')

