from app import app
from flask import render_template, flash, redirect, url_for, send_from_directory
from app.forms import LoginForm, RegisterForm, UploadForm, PostForm
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Image, FollowRequest, Post
from app.models import User, Image, FollowRequest, Post
from app import db
import os

#--------------- NAVBAR ROUTES -------------------------
@app.route("/")
@app.route("/introductory")
def introductory():
    return render_template("introductory.html")

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    images = Image.query.filter_by(user_id=current_user.id).all()
    print(images)
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
        print(image)
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form, images=images)

@app.route("/visualise") # This is currently "manipulate" in the nav-bar. eventually would like to put it into an analysis or more consolidated form
@login_required
def visualise():
    images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template("visualise.html", images=images)

@app.route('/social')
@login_required
def social_home():
    return redirect(url_for('social_feed'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(app.root_path, 'uploads')
    return send_from_directory(upload_folder, filename)


#--------------- SOCIAL ROUTES ------------------------
@app.route('/social/feed')
@login_required
def social_feed():
    followed_ids = [fr.followed_id for fr in current_user.following.filter_by(accepted=True)]
    followed_ids.append(current_user.id)
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.timestamp.desc()).all()
    return render_template('social/feed.html', posts=posts)

@app.route('/social/users')
@login_required
def list_users():
    users = User.query.filter(User.id != current_user.id).all() # TODO: fuzzy search through all accounts with client-side rendering

    follow_requests = FollowRequest.query.filter_by(follower_id=current_user.id).all()
    status_map = {fr.followed_id: (1 if fr.accepted else 0) for fr in follow_requests}
    followers = [
        fr.follower for fr in FollowRequest.query.filter_by(followed_id=current_user.id, accepted=True).all()
    ]

    user_statuses = []
    for user in users:
        status = status_map.get(user.id, -1)
        user_statuses.append((user, status))
    return render_template('social/users.html', user_statuses=user_statuses, followers=followers)

@app.route('/social/follow/<int:user_id>', methods=['POST'])
@login_required
def send_follow_request(user_id):
    existing = FollowRequest.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if not existing:
        fr = FollowRequest(follower_id=current_user.id, followed_id=user_id)
        db.session.add(fr)
        db.session.commit()
    return redirect(url_for('list_users'))

@app.route('/social/remove_follower/<int:user_id>', methods=['POST'])
@login_required
def remove_follower(user_id):
    fr = FollowRequest.query.filter_by(follower_id=user_id, followed_id=current_user.id, accepted=True).first()
    if fr:
        db.session.delete(fr)
        db.session.commit()
        flash("Follower removed.", "info")
    return redirect(url_for('list_users'))

@app.route('/social/inbox')
@login_required
def inbox():
    follow_requests = current_user.followers.filter_by(accepted=False).all()
    return render_template('social/inbox.html', requests=follow_requests)

@app.route('/social/accept_follow/<int:req_id>', methods=['POST'])
@login_required
def accept_follow(req_id):
    fr = FollowRequest.query.get_or_404(req_id)
    if fr.followed_id == current_user.id:
        fr.accepted = True
        db.session.commit()
    return redirect(url_for('inbox'))

@app.route('/social/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    images = Image.query.filter_by(user_id=current_user.id).all()
    app.logger.debug(f"Form data: id=post.id, title={form.title.data}, subtitle={form.subtitle.data}, image_id={form.image_id.data}, user_id={current_user.id}")
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            image_id=form.image_id.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('social_feed'))
    return render_template("social/create_post.html", form=form, images=images)


#------------ LOGIN ROUTES ------------------------
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
        print(f"[DEBUG] Created user: id={user.id}, username={user.username}")
        login_user(user)
        flash('Account created successfully. You are now logged in.', 'success')
        return redirect(url_for('introductory'))
    return render_template("register.html", form=form)