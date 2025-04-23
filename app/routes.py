from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route("/")
@app.route("/introductory")
def introductory():
    return render_template("introductory.html")

@app.route("/upload")
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
        flash('Login successful (dummy message)')
        return redirect(url_for('introductory'))
    return render_template("login.html", form=form)

@app.route("/register")
def register():
    return render_template("introductory.html") #TODO