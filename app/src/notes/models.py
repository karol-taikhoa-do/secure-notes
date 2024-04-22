from datetime import datetime
from werkzeug.security import generate_password_hash

from src import db, fernetkey

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String, nullable=False)
    _person_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    _isPublic = db.Column(db.String(100))
    _content = db.Column(db.Text, nullable=False)
    _isEncrypted = db.Column(db.String(100))
    _password = db.Column(db.String(200))
    _timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, title, person_id, content,
                 isPublic=True, isEncrypted=False, password=None
                 ):
        self._title = fernetkey.encrypt(title.encode()).decode("utf-8")
        self._person_id = person_id
        self._isPublic = fernetkey.encrypt(isPublic.encode()).decode("utf-8")
        self._content = fernetkey.encrypt(content.encode()).decode("utf-8")
        self._isEncrypted = fernetkey.encrypt(isEncrypted.encode()).decode("utf-8")
        if password is not None:
            self._password = self.set_password_hash(password)

    def get_title(self):
        return fernetkey.decrypt(self._title).decode()

    def set_title(self, val: str):
        self._title = fernetkey.encrypt(val.encode()).decode("utf-8")

    def get_person_id(self):
        return self._person_id  
    
    def set_person_id(self, val: str):
        self._person_id = val

    def get_content(self):
        return fernetkey.decrypt(self._content).decode()
        
    def set_content(self, val: str):
        self._content = fernetkey.encrypt(val.encode()).decode("utf-8")

    def get_timestamp(self):
        return self._timestamp
    
    def set_timestamp(self, val: str):
        self._timestamp = val

    def get_ispublic(self):
        return fernetkey.decrypt(self._isPublic).decode()
    
    def set_ispublic(self, val):
        self._isPublic = fernetkey.encrypt(val.encode()).decode("utf-8")

    def get_isencrypted(self):
        return fernetkey.decrypt(self._isEncrypted).decode()
    
    def set_isencrypted(self, val):
        self._isEncrypted = fernetkey.encrypt(val.encode()).decode("utf-8")

    def get_password_hash(self):
        return self._password
    
    def set_password_hash(self, val: str):
        self._password = generate_password_hash(val, method="pbkdf2:sha256:600000", salt_length=8)

    

    # @property
    # def title(self):
    #     return fernetkey.decrypt(self._title).decode()

    # @title.setter
    # def title(self, val: str):
    #     self._title = fernetkey.encrypt(val.encode())  
    
    # @property
    # def person_id(self):
    #     return fernetkey.decrypt(self._person_id).decode()  
    
    # @person_id.setter
    # def person_id(self, val: str):
    #     self._person_id = fernetkey.encrypt(val.encode())
    
    # @property
    # def content(self):
    #     return fernetkey.decrypt(self._content).decode()
    
    # @content.setter
    # def content(self, val: str):
    #     self._content = fernetkey.encrypt(val.encode())

    # @property
    # def timestamp(self):
    #     return fernetkey.decrypt(self._timestamp).decode()
    
    # @timestamp.setter
    # def timestamp(self, val: str):
    #     self._timestamp = fernetkey.encrypt(val.encode())

