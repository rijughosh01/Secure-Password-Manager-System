import os

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.crypto import derive_encryption_key, hash_password, verify_password
from app.forms import LoginForm, RegistrationForm
from app.models import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
  if current_user.is_authenticated:
    return redirect(url_for("vault.dashboard"))
  return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for("vault.dashboard"))

  form = RegistrationForm()
  if form.validate_on_submit():
    username = form.username.data.strip().lower()
    password = form.password.data
    salt = os.urandom(16)

    user = User(
      username=username,
      password_hash=hash_password(password),
      salt=salt,
    )
    db.session.add(user)
    db.session.commit()

    flash("Account created successfully. Please sign in.", "success")
    return redirect(url_for("auth.login"))

  return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("vault.dashboard"))

  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data.strip().lower()
    password = form.password.data
    user = User.query.filter_by(username=username).first()

    if user is None or not verify_password(password, user.password_hash):
      flash("Invalid username or password.", "danger")
      return render_template("login.html", form=form)

    encryption_key = derive_encryption_key(password, user.salt)
    session["encryption_key"] = encryption_key.decode("utf-8")
    session.permanent = True

    login_user(user)
    flash("Signed in successfully.", "success")
    return redirect(url_for("vault.dashboard"))

  return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
  session.pop("encryption_key", None)
  logout_user()
  flash("You have been signed out.", "info")
  return redirect(url_for("auth.login"))
