import os
from typing import Optional
from sqlalchemy.types import LargeBinary, TypeDecorator
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class EncryptedString(TypeDecorator):
      impl = LargeBinary
      cache_ok = True
      NONCE_BYTES = 12  # 96-bit nonce is the GCM standard

      def __init__(self, key: bytes, length: Optional[int] = None):
          if len(key) != 16:
              raise ValueError("AES-128 requires a 16-byte (32-hex-char) key")
          self._key = key
          super().__init__(length=length)

      def process_bind_param(self, value, dialect):
          if value is None:
              return None
          plaintext = value.encode("utf-8") if isinstance(value, str) else value
          nonce = os.urandom(self.NONCE_BYTES)
          ct_and_tag = AESGCM(self._key).encrypt(nonce, plaintext, associated_data=None)
          return nonce + ct_and_tag  
      
      def process_result_value(self, value, dialect):
          if value is None:
              return None
          nonce, ct_and_tag = value[: self.NONCE_BYTES], value[self.NONCE_BYTES:]
          plaintext = AESGCM(self._key).decrypt(nonce, ct_and_tag, associated_data=None)
          return plaintext.decode("utf-8")