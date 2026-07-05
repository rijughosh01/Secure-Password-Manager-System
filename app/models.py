from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False, index=True)
  password_hash = db.Column(db.LargeBinary, nullable=False)
  salt = db.Column(db.LargeBinary(16), nullable=False)
  created_at = db.Column(
    db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
  )
  entries = db.relationship(
    "CredentialEntry", backref="owner", lazy=True, cascade="all, delete-orphan"
  )

class CredentialEntry(db.Model):
  __tablename__ = "credential_entries"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
  service_name = db.Column(db.String(120), nullable=False)
  username = db.Column(db.String(120), nullable=False, default="")
  encrypted_password = db.Column(db.Text, nullable=False)
  encrypted_notes = db.Column(db.Text, nullable=True)
  created_at = db.Column(
    db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
  )
  updated_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
    nullable=False,
  )
