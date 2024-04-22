from .forms import NoteForm
from src.notes.models import Note
from src import db
from flask_login import current_user
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from src.users.models import User
from src.utils import is_password_strong, can_view_note

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/post-note", methods=["GET","POST"])
@login_required
def post_note():

    form = NoteForm()

    if form.validate_on_submit():
        password_note = form.password.data
        if password_note is not None and not is_password_strong(password_note):
            flash("Your password is too weak. Add more lower, upper case letters, number and special characters")
            return render_template("notes/create.html", form=form)


        author = current_user.id

        new_note = Note(title=form.title.data,
                        person_id=author,
                        content=form.content.data,
                        isPublic= "True" if form.isPublic.data else "False",
                        isEncrypted="True" if form.isEncrypted.data else "False",
                        password=form.password.data
                    )
        
        db.session.add(new_note)
        db.session.commit()

        flash("Successfully created new note")
    else:
        flash("o")

    return render_template("notes/create.html", form=form)


@notes_bp.route("/detail/<int:id>", methods=["GET","POST"])
@login_required
def details(id):
    note = Note.query.get_or_404(id)

    if not can_view_note(note):
        flash("Access denied")
        return redirect(url_for("core.home"))

    if note.get_isencrypted() == "True":
        return redirect(url_for("notes.get_encrypt_password", id=note.id))
    
    owner = User.query.filter_by(id=note.get_person_id()).first()

    return render_template("notes/details.html", note=note, author=owner.get_name())

@notes_bp.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)

    if note.get_ispublic():
        owner = User.query.filter_by(id=note.get_person_id()).first()

        if owner.id != current_user.id:
            flash("Access denied to edit this note")
            return redirect(url_for("core.home"))

    if note.get_isencrypted() == "True":
        return render_template("notes/password-notes.html", note=note)
    
    form = NoteForm()

    if form.validate_on_submit():
        note.set_title(form.title.data)
        note.set_content(form.content.data)
        note.set_ispublic(form.isPublic.data)
        note.set_isencrypted(form.isEncrypted.data)
        if note.get_isencrypted():
            note.set_password(form.password.data)
        
        db.session.add(note)
        db.session.commit()

        flash("Note successfully updated")
        return redirect(url_for("core.home"))
    
    if note.get_person_id() == current_user.id:
        form.title.data = note.get_title()
        form.content.data = note.get_content()
        form.isPublic.data = note.get_ispublic()
        form.isEncrypted.data = note.get_isencrypted()
        return render_template("notes/edit.html", form=form)
    else:
        flash("Access denied to edit this note")
        notes = Note.query.order_by(Note.get_timestamp())
        return render_template("core/index.html", notes=notes)
    

@notes_bp.route("/delete/<int:id>", methods=["GET","POST"])
@login_required
def delete(id):
    note_to_delete = Note.query.get_or_404(id)
    owner_id = note_to_delete.get_person_id()

    if owner_id == current_user.id:
        db.session.delete(note_to_delete)
        db.session.commit()

        flash("Successfully deleted note")
    
    else:
        flash("Permission denied. You're not the owner")

    return redirect(url_for("core.home"))

@notes_bp.route("/password-note/<int:id>", methods=["GET","POST"])
@login_required
def get_encrypt_password(id):

    from src.notes.forms import PasswordNoteForm
    from werkzeug.security import check_password_hash

    form = PasswordNoteForm()

    note = Note.query.get_or_404(id)

    if form.validate_on_submit():

        if check_password_hash(
            note.get_password_hash(),
            form.password.data
            ):
            owner = User.query.filter_by(id=note.get_person_id()).first()

            return render_template("notes/details.html", note=note, author=owner.get_name())

        else:
            flash("Invalid password to view this note")
            

    return render_template("notes/password-notes.html", note=note, form=form)