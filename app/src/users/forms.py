from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, ValidationError
import bleach

from src.users.models import User

def sanitize_input(form, field):
    cleaned_value = bleach.clean(field.data)
    if cleaned_value != field.data:
        raise ValidationError('Invalid characters detected in input.')

class LoginForm(FlaskForm):
    email = StringField(
        "email", validators=[DataRequired(), sanitize_input]
    )

    password = PasswordField(
        "Password", validators=[DataRequired(),sanitize_input]
    )

class RegisterForm(FlaskForm):
    email = StringField(
        "email", validators=[DataRequired(), Length(min=2, max=100),sanitize_input]
    )

    name = StringField(
        "name", validators=[DataRequired(), Length(min=2, max=100),sanitize_input]
    )

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=12, max=100),sanitize_input]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
            sanitize_input
        ],
    )

    def validate(self, extra_validators):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(_email=self.email.data).first()
        if user:
            self.email.errors.append("This email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True

class TwoFactorForm(FlaskForm):
    otp = StringField('Enter OTP', validators=[
                      InputRequired(), Length(min=6, max=6)])
