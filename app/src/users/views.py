from .forms import LoginForm, RegisterForm, TwoFactorForm
from src.users.models import User
from src.utils import random_delay, is_valid_email, is_password_strong
from src import db #, bcrypt
from flask_login import current_user, login_user
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash

users_bp = Blueprint("users", __name__)

HOME_URL = "core.home"
SETUP_2FA_URL = "users.setup_two_factor_auth"
VERIFY_2FA_URL = "users.verify_two_factor_auth"

incorrect_attempts = {}
blocked_users = {}

def find_email(email):
    users = User.query.all()

    for u in users:
        if u.get_email() == email:
            return u
        
    return None

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user._is_two_factor_authentication_enabled:
            flash("You are already registered.", "info")
            return redirect(url_for(HOME_URL))
        else:
            flash("You have not enabled 2-Factor Authentication. Please enable first to login.", "info")
            return redirect(url_for(SETUP_2FA_URL))
    
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if not is_valid_email(form.email.data):
            flash("That is not valid email")
            return render_template("users/signup.html", form=form)
        
        if not is_password_strong(form.password.data):
            flash("Your password is too weak. Add more lower, upper case letters, number and special characters")
            return render_template("users/signup.html", form=form)
        
        try:
            user = User(email=form.email.data, name=form.name.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("You are registered. You have to enable 2-Factor Authentication first to login.", "success")

            return redirect(url_for(SETUP_2FA_URL))
        except Exception:
            db.session.rollback()
            flash("Registration failed. Please try again.", "danger")

    return render_template("users/signup.html", form=form)

@users_bp.route("/login", methods=["GET", "POST"])
def login():

    random_delay()
    if current_user.is_authenticated:
        if current_user._is_two_factor_authentication_enabled:
            flash("You are already logged in.", "info")
            return redirect(url_for(HOME_URL))
        else:
            flash("You have not enabled 2-Factor Authentication. Please enable first to login.", "info")
            return redirect(url_for(SETUP_2FA_URL))
        
    form = LoginForm(request.form)
    if form.validate_on_submit():

        random_delay()
        if not is_valid_email(form.email.data):
            flash("That is not valid email")
            return render_template("users/login.html", form=form)
        
        email = form.email.data
        user = find_email(email)

        random_delay()
        if user and check_password_hash(user._password, request.form["password"]):
            if email in incorrect_attempts:
                incorrect_attempts[email] = 0
            
            
            login_user(user)
            if not current_user._is_two_factor_authentication_enabled:
                flash(
                    "You have not enabled 2-Factor Authentication. Please enable first to login.", "info")
                return redirect(url_for(SETUP_2FA_URL))
            return redirect(url_for(VERIFY_2FA_URL))

        else:
            random_delay()

            if email in blocked_users:
                flash("This user account has been blocked")
                return render_template("users/login.html", form=form)
            
            random_delay()
            if email in incorrect_attempts:
                if incorrect_attempts[email] > 5:
                    blocked_users[email] = True
                    del incorrect_attempts[email]
                else:
                    incorrect_attempts[email] += 1

            flash(f"Incorrect username and/or password", "danger")
    return render_template("users/login.html", form=form)

from flask_login import login_required, login_user, logout_user


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("users.login"))

from src.utils import get_b64encoded_qr_image

@users_bp.route("/setup-2fa")
@login_required
def setup_two_factor_auth():
    secret = current_user.get_secret_token()
    uri = current_user.get_authentication_setup_uri()
    base64_qr_image = get_b64encoded_qr_image(uri)
    return render_template("users/setup-2fa.html", secret=secret, qr_image=base64_qr_image)

@users_bp.route("/verify-2fa", methods=["GET", "POST"])
@login_required
def verify_two_factor_auth():
    form = TwoFactorForm(request.form)
    if form.validate_on_submit():
        if current_user.is_otp_valid(form.otp.data):
            if current_user._is_two_factor_authentication_enabled:
                flash("2FA verification successful. You are logged in!", "success")
                return redirect(url_for(HOME_URL))
            else:
                try:
                    current_user._is_two_factor_authentication_enabled = True
                    db.session.commit()
                    flash("2FA setup successful. You are logged in!", "success")
                    return redirect(url_for(HOME_URL))
                except Exception:
                    db.session.rollback()
                    flash("2FA setup failed. Please try again.", "danger")
                    return redirect(url_for(VERIFY_2FA_URL))
        else:
            flash("Invalid OTP. Please try again.", "danger")
            return redirect(url_for(VERIFY_2FA_URL))
    else:
        if not current_user._is_two_factor_authentication_enabled:
            flash(
                "You have not enabled 2-Factor Authentication. Please enable it first.", "info")
        return render_template("users/verify-2fa.html", form=form)