from app import app
from flask import render_template

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

@app.route("/login")
def login():
    return render_template("login.html")