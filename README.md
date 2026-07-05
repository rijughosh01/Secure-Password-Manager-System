# SecureVault — Password Manager

A secure password manager with encrypted credential storage and a Flask web interface.

## Features

- **User registration & authentication** — bcrypt password hashing with per-user salt
- **Encrypted vault** — credentials encrypted with Fernet (AES-128-CBC + HMAC) using keys derived via PBKDF2-HMAC-SHA256 (600,000 iterations)
- **Password generator** — cryptographically secure random passwords with configurable length and character sets
- **Web dashboard** — add, search, reveal, edit, and delete credentials
- **SQLite database** — encrypted data stored via SQLAlchemy ORM (parameterized queries prevent SQL injection)

## Security Measures

| Threat | Mitigation |
|--------|------------|
| SQL injection | SQLAlchemy ORM with parameterized queries |
| XSS | Jinja2 auto-escaping on all template output |
| CSRF | Flask-WTF CSRF tokens on all state-changing forms |
| Password storage | bcrypt hashing (cost factor 12) for master passwords |
| Credential storage | PBKDF2 key derivation + Fernet symmetric encryption |
| Session security | HttpOnly cookies, SameSite=Lax, security response headers |

## Requirements

- Python 3.10+

## Installation

### Windows (Quick Setup)

Double-click **`setup.bat`** or run from Command Prompt:

```bat
setup.bat
```

This will create a virtual environment, install dependencies, and prepare the app.

To start the server, run **`run.bat`** or:

```bat
venv\Scripts\activate
python run.py
```

### Manual Installation

```bash
cd "Secure Password Manager with Encryption and Web Interface"
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

1. **Register** — create an account with a strong master password (minimum 8 characters)
2. **Sign in** — your master password derives the encryption key for your session
3. **Add credentials** — store service name, username, password, and notes
4. **Generate passwords** — use the built-in generator for strong random passwords

> **Warning:** Your master password cannot be recovered. If lost, encrypted credentials are permanently inaccessible.

## Project Structure

```
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── crypto.py         # Hashing, encryption, password generation
│   ├── forms.py          # WTForms with validation
│   ├── models.py         # User and CredentialEntry models
│   ├── routes/
│   │   ├── auth.py       # Login, register, logout
│   │   └── vault.py      # Vault CRUD and generator
│   ├── static/css/       # Stylesheets
│   └── templates/        # HTML templates
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
└── run.py                # Entry point
```

## Environment Variables (Optional)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask session signing key (auto-generated if unset) |
| `DATABASE_URL` | Database URI (defaults to SQLite file) |

## Architecture

```
Master Password
      │
      ├──► bcrypt hash ──► stored in DB (authentication)
      │
      └──► PBKDF2 + salt ──► Fernet key ──► encrypt/decrypt vault entries
```

Stored credentials in the database contain only encrypted password and notes fields. Plaintext is never written to disk.
