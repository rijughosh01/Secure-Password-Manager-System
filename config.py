import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
  SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'password_manager.db')}"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  WTF_CSRF_ENABLED = True
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = "Lax"
  PERMANENT_SESSION_LIFETIME = 3600
  PBKDF2_ITERATIONS = 600_000
