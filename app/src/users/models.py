import pyotp
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from src import db, fernetkey #,bcrypt
from src.notes.models import Note 
from config import Config


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(100), unique=True, nullable=False)
    _name = db.Column(db.String(100), nullable=True)
    _password = db.Column(db.String(100), nullable=False)
    _is_two_factor_authentication_enabled = db.Column(
        db.Boolean, nullable=False, default=False)
    _secret_token = db.Column(db.String, unique=True)

    notes = db.relationship(
        Note,
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note._timestamp)"
    )


    def __init__(self, email, name, password):
        self._email = fernetkey.encrypt(email.encode())
        self._name = fernetkey.encrypt(name.encode())
        self._password = generate_password_hash(password=password, method="pbkdf2:sha256:600000", salt_length=8)
        self._secret_token = fernetkey.encrypt(pyotp.random_base32().encode())

    def get_email(self):
        return fernetkey.decrypt(self._email).decode()
    
    def set_email(self, val: str):
        self._email = fernetkey.encrypt(val.encode()).decode("utf-8")
 
    def get_name(self):
        return fernetkey.decrypt(self._name).decode()
    
    def set_name(self, val: str):
        self._name = fernetkey.encrypt(val.encode()).decode()

    def get_secret_token(self):
        return fernetkey.decrypt(self._secret_token).decode()
    
    def set_secret_token(self, val: str):
        self._secret_token = fernetkey.encrypt(val.encode()).decode()

    def get_2fa(self):
        return fernetkey.decrypt(self._is_two_factor_authentication_enabled).decode()
    
    def set_2fa(self, val: str):
        self._is_two_factor_authentication_enabled = fernetkey.encrypt(val.encode()).decode()


    def get_authentication_setup_uri(self):
        return pyotp.totp.TOTP(self.get_secret_token()).provisioning_uri(
            name=self.get_email(), issuer_name=Config.APP_NAME)

    def is_otp_valid(self, user_otp):
        totp = pyotp.parse_uri(self.get_authentication_setup_uri())
        return totp.verify(user_otp)

    # @property
    # def email(self):
    #     return fernetkey.decrypt(self._email).decode()
    
    # @email.setter
    # def email(self, val: str):
    #     self._email = fernetkey.encrypt(val.encode())

    # @property
    # def name(self):
    #     return fernetkey.decrypt(self._name).decode()
    
    # @name.setter
    # def name(self, val: str):
    #     self._name = fernetkey.encrypt(val.encode())

    # @property
    # def secret_token(self):
    #     return fernetkey.decrypt(self._secret_token).decode()
    
    # @secret_token.setter
    # def secret_token(self, val: str):
    #     self._secret_token = fernetkey.encrypt(val.encode())


