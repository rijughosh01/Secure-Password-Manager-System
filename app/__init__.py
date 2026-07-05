from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.models import User, db
from config import Config


login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  login_manager.init_app(app)
  csrf.init_app(app)

  login_manager.login_view = "auth.login"
  login_manager.login_message_category = "info"

  @login_manager.user_loader
  def load_user(user_id):
    return db.session.get(User, int(user_id))

  from app.routes.auth import auth_bp
  from app.routes.vault import vault_bp

  app.register_blueprint(auth_bp)
  app.register_blueprint(vault_bp)

  @app.after_request
  def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
      "default-src 'self'; "
      "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
      "font-src fonts.gstatic.com; "
      "script-src 'self'"
    )
    return response

  with app.app_context():
    db.create_all()

  return app
