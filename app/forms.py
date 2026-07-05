from flask_wtf import FlaskForm
from wtforms import (
  BooleanField,
  IntegerField,
  PasswordField,
  StringField,
  SubmitField,
  TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
  username = StringField(
    "Username",
    validators=[DataRequired(), Length(min=3, max=80)],
    render_kw={"autocomplete": "username"},
  )
  password = PasswordField(
    "Master Password",
    validators=[DataRequired(), Length(min=8, max=128)],
    render_kw={"autocomplete": "new-password"},
  )
  confirm_password = PasswordField(
    "Confirm Master Password",
    validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    render_kw={"autocomplete": "new-password"},
  )
  submit = SubmitField("Create Account")

  def validate_username(self, field):
    if User.query.filter_by(username=field.data.strip().lower()).first():
      raise ValidationError("Username is already taken.")


class LoginForm(FlaskForm):
  username = StringField(
    "Username",
    validators=[DataRequired(), Length(min=3, max=80)],
    render_kw={"autocomplete": "username"},
  )
  password = PasswordField(
    "Master Password",
    validators=[DataRequired()],
    render_kw={"autocomplete": "current-password"},
  )
  submit = SubmitField("Sign In")


class CredentialForm(FlaskForm):
  service_name = StringField(
    "Service / Website",
    validators=[DataRequired(), Length(min=1, max=120)],
  )
  username = StringField("Username / Email", validators=[Length(max=120)])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=512)])
  notes = TextAreaField("Notes", validators=[Length(max=2000)])
  submit = SubmitField("Save")


class PasswordGeneratorForm(FlaskForm):
  length = IntegerField(
    "Length",
    default=16,
    validators=[DataRequired(), NumberRange(min=8, max=128)],
  )
  use_uppercase = BooleanField("Uppercase (A-Z)", default=True)
  use_lowercase = BooleanField("Lowercase (a-z)", default=True)
  use_digits = BooleanField("Digits (0-9)", default=True)
  use_symbols = BooleanField("Symbols (!@#...)", default=True)
  submit = SubmitField("Generate Password")
