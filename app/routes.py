from app import app
from flask import render_template, flash, redirect, url_for, send_from_directory
from app.forms import LoginForm, RegisterForm, UploadForm, NewPostForm
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Image, Post
from app import db
import os

@app.route("/")
@app.route("/introductory")
def introductory():
    return render_template("introductory.html")

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
     # Fetch images in reverse chronological order (newest first)
    images = Image.query.filter_by(user_id=current_user.id).order_by(Image.id.desc()).all()
    app.logger.debug(images)
    if form.validate_on_submit():
        file = form.image.data
        image = Image(filename='', title=form.title.data, user_id=current_user.id)

        db.session.add(image)
        db.session.flush()
        sanitized_filename = secure_filename(file.filename)
        ext = sanitized_filename.rsplit('.', 1)[1].lower()
        filename = f"{image.id}.{ext}"
        filepath = os.path.join('app/uploads', filename)
        file.save(filepath)

        image.filename = filename
        db.session.commit()
        app.logger.debug(image)
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form, images=images)

@app.route("/visualise")
@login_required
def about():
    images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template("visualise.html", images=images)

@app.route("/share")
def share():
    return render_template("share.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            app.logger.debug(f"[DEBUG] Found user: id={user.id}, username={user.username}")
        else:
            app.logger.debug("[DEBUG] No user found with that username.")
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
    flash('Logged out successfully', 'success')
    return redirect(url_for('introductory'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        app.logger.debug(f"[DEBUG] Created user: id={user.id}, username={user.username}")
        login_user(user)
        flash('Account created successfully. You are now logged in.', 'success')
        return redirect(url_for('introductory'))
    return render_template("register.html", form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(app.root_path, 'uploads')
    return send_from_directory(upload_folder, filename)

@app.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    # populate choices with (id, filename or thumbnail) for this user
    user_images = Image.query.filter_by(user_id=current_user.id).all()
    form.images.choices = [(img.id, img.filename) for img in user_images]

    if form.validate_on_submit():
        p = Post(title=form.title.data,
                 description=form.description.data,
                 user_id=current_user.id)
        # attach images
        for img_id in form.images.data:
            img = Image.query.get(img_id)
            if img and img.user_id == current_user.id:
                p.images.append(img)
        db.session.add(p)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('share'))  # or 'feed' if you have it

    return render_template('new_post.html', form=form, images=user_images)