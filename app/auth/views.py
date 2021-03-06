from app.requests import get_quotes
from flask_bcrypt import check_password_hash
import secrets, os, app
from . import auth
from sqlalchemy.orm import query
from app.models import User, Post
from app import db, bcrypt
from flask import url_for, render_template, flash, redirect, request, abort
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import json
from ..requests import get_quotes


@auth.route("/register", methods=['GET','POST'])
def register():
    raw_quotes = get_quotes()
    quotes = json.loads(raw_quotes)
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html", title="Register", form=form, quotes=quotes)


@auth.route("/login", methods=['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    raw_quotes = get_quotes()
    quotes = json.loads(raw_quotes)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')  
                flash(f"Logged in successfully!", "success")
                return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash(f"Invalid credentials", "danger")
        
    return render_template("login.html", title="Login", form=form,quotes=quotes)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
