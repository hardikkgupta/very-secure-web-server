import os
import re
from flask import Blueprint, render_template, redirect, url_for, request, session, abort, send_from_directory, jsonify
from .forms import RegistrationForm, LoginForm
from .models import User
from . import db, bcrypt, limiter
from werkzeug.security import generate_password_hash, check_password_hash
import logging

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Input Validation
        if not re.match("^[A-Za-z0-9_]+$", username):
            logging.warning(f"Invalid registration attempt with username: {username}")
            return "Invalid username!", 400

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            logging.warning(f"Registration attempt with existing username: {username}")
            return "Username already exists!", 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        logging.info(f"New user registered: {username}")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Fetch user from database
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            logging.info(f"User logged in: {username}")
            return redirect(url_for('main.dashboard'))
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            return "Invalid credentials!", 401
    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', username=user.username)

@main.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.pop('user_id', None)
    logging.info(f"User logged out: {user_id}")
    return redirect(url_for('main.home'))

# Secure Static File Serving Example
@main.route('/static/<path:filename>')
def static_files(filename):
    if ".." in filename or filename.startswith("/"):
        abort(403)
    return send_from_directory('static', filename)
