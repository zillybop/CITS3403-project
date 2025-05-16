from app import app
from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.forms import LoginForm, RegisterForm, UploadForm, PostForm
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegisterForm, UploadForm, PostForm, ToolResultForm
from app.models import User, Image, FollowRequest, Post
from app import db
from flask import request, jsonify
from sqlalchemy import func
import os, time, base64
from werkzeug.datastructures import MultiDict

#--------------- NAVBAR ROUTES -------------------------
@app.route("/")
@app.route("/introductory")
def introductory():
    return render_template("introductory.html", timestamp=int(time.time()), current_page="introductory")

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    images = Image.query.filter_by(user_id=current_user.id).all()
    print(images)
    
    if 'delete' in request.form:
        image_id = request.form.get('image_id')
        image = Image.query.filter_by(id=image_id, user_id=current_user.id).first()
        if image:
            filepath = os.path.join(app.root_path, 'uploads', image.filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            db.session.delete(image)
            db.session.commit()
            flash('Image deleted successfully!', 'success')
        else:
            flash('Error deleting image.', 'danger')
        return redirect(url_for('upload'))
    
    form = UploadForm()
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
    
    return render_template('upload.html', form=form, images=images, timestamp=int(time.time()), current_page="upload")

@app.route('/uploads/<filename>') #TODO: ensure user has access to this file
@login_required
def uploaded_file(filename):
    upload_folder = os.path.join(app.root_path, 'uploads')
    return send_from_directory(upload_folder, filename)

@app.route('/social')
@login_required
def social_home():
    return redirect(url_for('social_feed'))

@app.route('/tools')
@login_required
def tools():
    return redirect(url_for('visualise'))

#--------------- SOCIAL ROUTES ------------------------
@app.route('/api/users/search')
@login_required
def api_users_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    # case-insensitive search in a DB-agnostic way
    matches = User.query.filter(
        User.id != current_user.id,
        func.lower(User.username).contains(q.lower())
    ).all()

    outgoing = FollowRequest.query.filter_by(follower_id=current_user.id).all()
    status_map = {fr.followed_id: fr.accepted for fr in outgoing}

    payload = [{
        'id':       u.id,
        'username': u.username,
        'isFriend': status_map.get(u.id, False)
    } for u in matches]

    return jsonify(payload)

@app.route('/social/feed')
@login_required
def social_feed():
    followed_ids = [fr.followed_id for fr in current_user.following.filter_by(accepted=True)]
    followed_ids.append(current_user.id)
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.timestamp.desc()).all()
    return render_template('social/feed.html', posts=posts, timestamp=int(time.time()), current_page="social")

@app.route('/social/feed/save_photo/<int:image_id>', methods=['POST', 'GET'])
@login_required
def save_photo(image_id):
    original = Image.query.get_or_404(image_id)

    # Optionally restrict access here if needed
    if original.user_id == current_user.id:
        flash("This image is already in your uploads.", "info")
        return redirect(url_for("social_feed"))
    
    # Check that image is shared via a visible post
    followed_ids = [fr.followed_id for fr in current_user.following.filter_by(accepted=True)]

    valid_post = Post.query.filter_by(image_id=image_id).filter(Post.user_id.in_(followed_ids)).first()
    if not valid_post:
        flash("You don’t have permission to copy this image.", "danger")
        return redirect(url_for("social_feed"))

    new_image = Image(
        filename='',
        title=f"Copy of {original.title}",
        user_id=current_user.id,
        source_type="copied",
        tool_used=original.tool_used,
        parameters=original.parameters,
        derived_from_id=original.id
    )
    db.session.add(new_image)
    db.session.flush()

    # Copy the file
    old_path = os.path.join(app.root_path, "uploads", original.filename)
    ext = original.filename.rsplit(".", 1)[1]
    new_filename = f"{new_image.id}_copy.{ext}"
    new_path = os.path.join(app.root_path, "uploads", new_filename)

    with open(old_path, "rb") as f_in, open(new_path, "wb") as f_out:
        f_out.write(f_in.read())

    new_image.filename = new_filename
    db.session.commit()

    flash("Image added to your uploads!", "success")
    return redirect(url_for("upload"))

@app.route('/social/feed/reopen_tool/<int:image_id>')
@login_required
def reopen_tool(image_id):
    derived = Image.query.get_or_404(image_id)

    # Check that image is shared via a visible post
    followed_ids = [fr.followed_id for fr in current_user.following.filter_by(accepted=True)]
    followed_ids.append(current_user.id)

    valid_post = Post.query.filter_by(image_id=image_id).filter(Post.user_id.in_(followed_ids)).first()
    if not valid_post:
        flash("You don't have permission to reopen this image in the tool.", "danger")
        return redirect(url_for("social_feed"))

    if not derived.tool_used or not derived.parameters or not derived.derived_from_id:
        flash("This image doesn't contain enough information to reopen in the tool.", "danger")
        return redirect(url_for("social_feed"))

    # Ensure the input image exists
    input_image = Image.query.get(derived.derived_from_id)
    if not input_image:
        flash("The input image no longer exists.", "danger")
        return redirect(url_for("social_feed"))

    # Clone the input image if needed
    if input_image.user_id != current_user.id:
        new_input = Image(
            filename='',
            title=f"Copy of {input_image.title}",
            user_id=current_user.id,
            source_type="copied",
            tool_used=input_image.tool_used,
            parameters=input_image.parameters,
            derived_from_id=input_image.id
        )
        db.session.add(new_input)
        db.session.flush()

        ext = input_image.filename.rsplit(".", 1)[1]
        new_filename = f"{new_input.id}_copy.{ext}"
        old_path = os.path.join(app.root_path, "uploads", input_image.filename)
        new_path = os.path.join(app.root_path, "uploads", new_filename)

        with open(old_path, "rb") as f_in, open(new_path, "wb") as f_out:
            f_out.write(f_in.read())

        new_input.filename = new_filename
        db.session.commit()
        
        flash("Image added to your uploads!", "success")
        input_image_id = new_input.id
    else:
        input_image_id = input_image.id

    return redirect(url_for(
        "edge_detect",
        image_id=input_image_id,
        tool=derived.tool_used,
        threshold=derived.parameters.get("threshold", 100)
    ))

@app.route('/social/users')
@login_required
def list_users():
    # grab the raw search term
    q = request.args.get('search', '').strip()

    # build a map of “who I’ve already requested/accepted”
    outgoing = FollowRequest.query.filter_by(follower_id=current_user.id).all()
    status_map = { fr.followed_id: fr.accepted for fr in outgoing }

    # If this is our AJAX‐search call, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # empty search => no results
        if not q:
            return jsonify([])
        # find everyone except me whose username contains q (case-insensitive)
        matches = (User.query
                       .filter(User.id != current_user.id)
                               
                       .all())
        return jsonify([
            {
                'id':       u.id,
                'username': u.username,
                'isFriend': bool(status_map.get(u.id, False))
            }
            for u in matches
        ])

    # Otherwise render full page
    # ────────────────────────
    # Existing “all users” list (for initial load)
    all_users = User.query.filter(User.id != current_user.id).all()
    user_statuses = [
        (u, 1 if status_map.get(u.id) else -1)
        for u in all_users
    ]
    # Your followers panel
    followers = [
        fr.follower
        for fr in FollowRequest.query.filter_by(followed_id=current_user.id, accepted=True)
    ]

    return render_template(
        'social/users.html',
        user_statuses=user_statuses,
        followers=followers,
        current_page="social"
        timestamp=int(time.time())
    )


@app.route('/social/follow/<int:user_id>', methods=['POST'])
@login_required
def send_follow_request(user_id):
    existing = FollowRequest.query.filter_by(
        follower_id=current_user.id,
        followed_id=user_id
    ).first()
    if not existing:
        fr = FollowRequest(follower_id=current_user.id, followed_id=user_id)
        db.session.add(fr)
        db.session.commit()
    # AJAX OK response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({ 'success': True, 'status': 'pending' })
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
    return render_template('social/inbox.html', requests=follow_requests, timestamp=int(time.time()), current_page="social")

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

    image_id = request.args.get("image_id", type=int)
    images = Image.query.filter_by(user_id=current_user.id).all()

    if image_id:
        selected_image = next((img for img in images if img.id == image_id), None)
        if selected_image:
            form.image_id.data = selected_image.id
            form.title.data = selected_image.title or "Generated Result"
            form.subtitle.data = f"Tool: {selected_image.tool_used}, Threshold: {selected_image.parameters.get('threshold')}"
            images = [selected_image]  # TODO: probably get rid of this?

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
    return render_template("social/create_post.html", form=form, images=images, timestamp=int(time.time()), current_page="social")


#------------------------------------- TOOL ROUTES -----------------------------------------
@app.route("/tools/visualise")
@login_required
def visualise():
    images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template("tools/visualise.html", images=images, timestamp=int(time.time()), current_page="tools")

@app.route("/tools/edge_detect", methods=['GET', 'POST'])
@login_required
def edge_detect():
    form = ToolResultForm(formdata=request.form)
    
    # Extract query params
    prefill_image_id = request.args.get("image_id", type=int)
    prefill_tool = request.args.get("tool")
    prefill_threshold = request.args.get("threshold", type=int)
    prefill_filename = None
    if prefill_image_id:
        image = Image.query.filter_by(id=prefill_image_id, user_id=current_user.id).first()
        if image:
            prefill_filename = image.filename

    images = Image.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        app.logger.debug(f"ToolResultForm submitted data:")
        app.logger.debug(f"  tool: {form.tool.data}")
        app.logger.debug(f"  threshold: {form.threshold.data}")
        app.logger.debug(f"  input_image_id: {form.input_image_id.data}")
        if type(form.output_image_dataurl.data) == list:
            app.logger.debug(f"  output_image_dataurl: {form.output_image_dataurl.data[:100]}...")  # only show first 100 chars
        app.logger.debug("")

    if form.validate_on_submit():
        app.logger.debug("Form validated!")
        try:
            # Step 1: Extract and validate base64 data
            data_url = form.output_image_dataurl.data
            if not data_url.startswith("data:image/png;base64,"):
                flash("Invalid image data.", "danger")
                return redirect(url_for('edge_detect'))

            app.logger.debug(data_url)
            # Step 2: Decode and save the image
            base64_data = data_url.split(",")[1]
            image_bytes = base64.b64decode(base64_data)
            
            # Generate a clean filename
            tool = form.tool.data.lower()
            threshold = int(form.threshold.data) if form.threshold.data else None
            input_image_id = form.input_image_id.data

            input_image = Image.query.filter_by(id=input_image_id, user_id=current_user.id).first()
            if not input_image:
                flash("Invalid input image reference.", "danger")
                return redirect(url_for("edge_detect"))

            app.logger.debug(f"tool: {tool}, threshold: {threshold}")

            new_image = Image(
                filename="",  # will set after writing file
                title=f"{tool.capitalize()} Result",
                user_id=current_user.id,
                source_type="tool-generated",
                tool_used=tool,
                parameters={'threshold': threshold} if threshold else {},
                derived_from_id=int(input_image_id) if input_image_id else None
            )
            db.session.add(new_image)
            db.session.flush()

            filename = f"{new_image.id}_{tool}_{threshold}.png"
            filepath = os.path.join(app.root_path, "uploads", filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            new_image.filename = filename
            db.session.commit()

            flash("Your image has been saved successfully!", "success")
            return redirect(url_for("upload"))

        except Exception as e:
            app.logger.error(f"Error saving tool result: {e}")
            flash("An error occurred while sharing your result.", "danger")
            return redirect(url_for("edge_detect"))

    if request.method == "POST":
        flash("There was a problem submitting your result. Please try again.", "warning")
    return render_template("tools/edge_detect.html",
                           form=form,
                           images=images,
                           prefill_image_id=prefill_image_id,
                           prefill_tool=prefill_tool,
                           prefill_threshold=prefill_threshold,
                           prefill_filename=prefill_filename,
                           timestamp=int(time.time())
                           current_page="tools"
            )

@app.route("/tools/histogram")
@login_required
def histogram():
    return render_template("tools/histogram.html", timestamp=int(time.time()), current_page="tools")

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
    return render_template("login.html", form=form, timestamp=int(time.time()), current_page=None)

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
    return render_template("register.html", form=form, timestamp=int(time.time()), current_page=None)
