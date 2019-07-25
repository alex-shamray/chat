import io
import os

from cryptography import exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.core.files.base import File
from django.urls import reverse
from django.utils.encoding import force_bytes
from storages.backends.s3boto3 import S3Boto3Storage


class EncryptedFilesMixin:
    def _encrypt(self, content, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = kdf.derive(password)
        cipher = ChaCha20Poly1305(key)

        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, content, None)
        return salt + nonce + ciphertext

    def _decrypt(self, token, password):
        salt = token[:16]
        nonce = token[16:28]
        ciphertext = token[28:]

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = kdf.derive(password)
        cipher = ChaCha20Poly1305(key)

        return cipher.decrypt(nonce, ciphertext, None)

    def _open(self, name, mode='rb'):
        file = super()._open(name, mode)
        try:
            return File(io.BytesIO(self._decrypt(file.read(), force_bytes(settings.SECRET_KEY))))
        except exceptions.InvalidTag:
            return file

    def _save(self, name, content):
        content.seek(0)
        encrypted = self._encrypt(content.read(), force_bytes(settings.SECRET_KEY))
        content.seek(0)
        content.write(encrypted)
        return super()._save(name, content)

    def url(self, name):
        """
        Returns an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        return reverse('file-download', args=(name,))


class S3Boto3Storage(EncryptedFilesMixin, S3Boto3Storage):
    pass
