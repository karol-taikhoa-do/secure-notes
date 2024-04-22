from io import BytesIO
import qrcode
from base64 import b64encode
import random
import time
import re
from flask_login import current_user

def get_b64encoded_qr_image(data):
    print(data)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)
    return b64encode(buffered.getvalue()).decode("utf-8")

def random_delay():
    delay = random.uniform(1.3, 2.7) # seconds
    time.sleep(delay)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def is_password_strong(password: str) -> bool:
    
    is_long = len(password) > 11

    has_digit = re.search(r"\d", password) is not None

    has_uppercase = re.search(r"[A-Z]", password) is not None

    has_lowercase = re.search(r"[a-z]", password) is not None

    has_special_char = re.search(r"\W", password) is not None

    varied_chars = (has_lowercase and has_special_char and has_digit and has_uppercase and is_long)

    import string

    charsets = [
        string.ascii_letters,
        string.digits,
        string.punctuation
    ]
    entropy = sum(len(charset) for charset in charsets if any(char in password for char in charset))

    entropy *= len(password)

    high_entropy = entropy > 100

    return high_entropy and varied_chars

def is_note_public(note):
    return note.get_ispublic()

def is_authorized_author(note):
    return current_user.is_authenticated and note.get_person_id() == current_user.id

def can_view_note(note):
    return is_note_public(note) or is_authorized_author(note)