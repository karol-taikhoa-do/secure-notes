from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.notes.models import Note

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
@login_required
def home():
    notes = Note.query.filter_by(_person_id =current_user.id).order_by(Note._timestamp).all()

    return render_template("core/index.html", notes=notes)