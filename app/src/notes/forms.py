from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, ValidationError
from flask_ckeditor import CKEditorField
import bleach

def sanitize_input(form, field):
    cleaned_value = bleach.clean(field.data)
    if cleaned_value != field.data:
        raise ValidationError('Invalid characters detected in input.')


class PasswordNoteForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=100), sanitize_input])

class NoteForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired(), Length(min=1, max=100)])
	content = CKEditorField("Content", validators=[DataRequired(), Length(min=1,max=10000)])
	isPublic = BooleanField("Public")
	isEncrypted = BooleanField("Encrypt")
	password = PasswordField("Password", validators=[Optional(), Length(min=12, max=100)])
	submit = SubmitField("Submit")
