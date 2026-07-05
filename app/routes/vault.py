from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app.crypto import decrypt_value, encrypt_value, generate_password
from app.forms import CredentialForm, PasswordGeneratorForm
from app.models import CredentialEntry, db

vault_bp = Blueprint("vault", __name__)


def _get_encryption_key():
  key = session.get("encryption_key")
  if not key:
    return None
  return key.encode("utf-8")


def _require_encryption_key():
  if _get_encryption_key() is None:
    flash("Session expired. Please sign in again.", "warning")
    return False
  return True


@vault_bp.route("/dashboard")
@login_required
def dashboard():
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  search = request.args.get("q", "").strip()
  query = CredentialEntry.query.filter_by(user_id=current_user.id)

  if search:
    like = f"%{search}%"
    query = query.filter(
      db.or_(
        CredentialEntry.service_name.ilike(like),
        CredentialEntry.username.ilike(like),
      )
    )

  entries = query.order_by(CredentialEntry.service_name.asc()).all()
  return render_template("dashboard.html", entries=entries, search=search)


@vault_bp.route("/entries/add", methods=["GET", "POST"])
@login_required
def add_entry():
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  form = CredentialForm()
  if form.validate_on_submit():
    key = _get_encryption_key()
    entry = CredentialEntry(
      user_id=current_user.id,
      service_name=form.service_name.data.strip(),
      username=form.username.data.strip(),
      encrypted_password=encrypt_value(key, form.password.data),
      encrypted_notes=encrypt_value(key, form.notes.data or ""),
    )
    db.session.add(entry)
    db.session.commit()
    flash("Credential saved securely.", "success")
    return redirect(url_for("vault.dashboard"))

  return render_template("entry_form.html", form=form, title="Add Credential")


@vault_bp.route("/entries/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  entry = CredentialEntry.query.filter_by(
    id=entry_id, user_id=current_user.id
  ).first_or_404()

  key = _get_encryption_key()
  form = CredentialForm()

  if form.validate_on_submit():
    entry.service_name = form.service_name.data.strip()
    entry.username = form.username.data.strip()
    entry.encrypted_password = encrypt_value(key, form.password.data)
    entry.encrypted_notes = encrypt_value(key, form.notes.data or "")
    db.session.commit()
    flash("Credential updated.", "success")
    return redirect(url_for("vault.dashboard"))

  if request.method == "GET":
    form.service_name.data = entry.service_name
    form.username.data = entry.username
    try:
      form.password.data = decrypt_value(key, entry.encrypted_password)
      form.notes.data = decrypt_value(key, entry.encrypted_notes or "")
    except ValueError as exc:
      flash(str(exc), "danger")
      return redirect(url_for("vault.dashboard"))

  return render_template("entry_form.html", form=form, title="Edit Credential")


@vault_bp.route("/entries/<int:entry_id>/reveal")
@login_required
def reveal_password(entry_id):
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  entry = CredentialEntry.query.filter_by(
    id=entry_id, user_id=current_user.id
  ).first_or_404()

  key = _get_encryption_key()
  try:
    password = decrypt_value(key, entry.encrypted_password)
    notes = decrypt_value(key, entry.encrypted_notes or "")
  except ValueError as exc:
    flash(str(exc), "danger")
    return redirect(url_for("vault.dashboard"))

  return render_template(
    "reveal.html", entry=entry, password=password, notes=notes
  )


@vault_bp.route("/entries/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_entry(entry_id):
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  entry = CredentialEntry.query.filter_by(
    id=entry_id, user_id=current_user.id
  ).first_or_404()

  db.session.delete(entry)
  db.session.commit()
  flash("Credential deleted.", "info")
  return redirect(url_for("vault.dashboard"))


@vault_bp.route("/generator", methods=["GET", "POST"])
@login_required
def password_generator():
  if not _require_encryption_key():
    return redirect(url_for("auth.login"))

  form = PasswordGeneratorForm()
  generated = None

  if form.validate_on_submit():
    try:
      generated = generate_password(
        length=form.length.data,
        use_uppercase=form.use_uppercase.data,
        use_lowercase=form.use_lowercase.data,
        use_digits=form.use_digits.data,
        use_symbols=form.use_symbols.data,
      )
    except ValueError as exc:
      flash(str(exc), "danger")

  return render_template("generator.html", form=form, generated=generated)
