import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.utils.encoding import force_bytes, force_text


def encrypt(content, password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password)
    cipher = ChaCha20Poly1305(key)

    nonce = os.urandom(12)
    if not isinstance(content, bytes):
        content = force_bytes(content)
    ciphertext = cipher.encrypt(nonce, content, None)
    return salt + nonce + ciphertext


def decrypt(token, password):
    salt = token[:16]
    nonce = token[16:28]
    ciphertext = token[28:]

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password)
    cipher = ChaCha20Poly1305(key)

    content = cipher.decrypt(nonce, ciphertext, None)
    return force_text(content)
