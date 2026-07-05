import base64
import secrets
import string

import bcrypt
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import Config


def hash_password(password: str) -> bytes:
  return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))


def verify_password(password: str, password_hash: bytes) -> bool:
  return bcrypt.checkpw(password.encode("utf-8"), password_hash)


def derive_encryption_key(password: str, salt: bytes) -> bytes:
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=Config.PBKDF2_ITERATIONS,
  )
  key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
  return key


def encrypt_value(key: bytes, plaintext: str) -> str:
  fernet = Fernet(key)
  return fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_value(key: bytes, ciphertext: str) -> str:
  fernet = Fernet(key)
  try:
    return fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
  except InvalidToken:
    raise ValueError("Unable to decrypt data. Master password may be incorrect.")


def generate_password(
  length: int = 16,
  use_uppercase: bool = True,
  use_lowercase: bool = True,
  use_digits: bool = True,
  use_symbols: bool = True,
) -> str:
  charset = ""
  if use_lowercase:
    charset += string.ascii_lowercase
  if use_uppercase:
    charset += string.ascii_uppercase
  if use_digits:
    charset += string.digits
  if use_symbols:
    charset += "!@#$%^&*()-_=+[]{}|;:,.<>?"

  if not charset:
    raise ValueError("At least one character set must be selected.")

  return "".join(secrets.choice(charset) for _ in range(length))
