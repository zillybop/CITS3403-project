from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db

@app.route("/")
@app.route("/introductory")
def introductory():
    return render_template("introductory.html")

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html")

@app.route("/visualise")
def about():
    return render_template("visualise.html")

@app.route("/share")
def share():
    return render_template("share.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(f"[DEBUG] Found user: id={user.id}, username={user.username}")
        else:
            print("[DEBUG] No user found with that username.")
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('introductory'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out succesfully', 'success')
    return redirect(url_for('introductory'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print(f"[DEBUG] Created user: id={user.id}, username={user.username}")
        login_user(user)
        flash('Account created successfully. You are now logged in.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)