from decouple import config
from flask import Flask, Response
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from cryptography.fernet import Fernet
from flask_wtf.csrf import CSRFProtect

class CustomResponse(Response):
    default_headers = [
        ('Server', None),
    ]

key_file_path = 'secret.key'

with open(key_file_path, 'rb') as f:
    key = f.read()

fernetkey = Fernet(key)

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
app.jinja_options["autoescape"] = lambda _ : True

app.response_class = CustomResponse

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)

login_manager = LoginManager() 
login_manager.init_app(app) 

from src.users.views import users_bp
from src.core.views import core_bp
from src.notes.views import notes_bp

app.register_blueprint(users_bp)
app.register_blueprint(core_bp)
app.register_blueprint(notes_bp)

from src.users.models import User

login_manager.login_view = "users.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()