import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, calculate_days_left, get_color_class

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
db = SQL("sqlite:///reminder.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    reminders = db.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY due_date ASC", user_id)

    for reminder in reminders:
        days_left = calculate_days_left(reminder["due_date"])
        reminder["days_left"] = days_left
        reminder["color_class"] = get_color_class(days_left)

    return render_template("dashboard.html", reminders=reminders)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or password != confirmation:
            return render_template("register.html", error="Invalid input.")

        hash_pw = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return render_template("register.html", error="Username already exists.")

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not user or not check_password_hash(user[0]["hash"], password):
            return render_template("login.html", error="Invalid username or password.")

        session["user_id"] = user[0]["id"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        frequency = request.form.get("frequency")
        due_date = request.form.get("due_date")

        if not title or not frequency or not due_date:
            return render_template("add.html", error="All fields are required.")

        db.execute("INSERT INTO reminders (user_id, title, frequency, due_date, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                   session["user_id"], title, frequency, due_date)
        return redirect("/")

    return render_template("add.html")


@app.route("/search")
@login_required
def search():
    q = request.args.get("q", "").lower()
    user_id = session["user_id"]

    if q:
        reminders = db.execute("""
            SELECT * FROM reminders
            WHERE user_id = ?
              AND LOWER(title) LIKE ?
            ORDER BY due_date ASC
        """, user_id, f"%{q}%")
    else:
        reminders = db.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY due_date ASC", user_id)

    for reminder in reminders:
        days_left = calculate_days_left(reminder["due_date"])
        reminder["days_left"] = days_left
        reminder["color_class"] = get_color_class(days_left)

    return render_template("reminder_table.html", reminders=reminders)


@app.route("/edit/<int:reminder_id>", methods=["GET", "POST"])
@login_required
def edit(reminder_id):
    reminder = db.execute("SELECT * FROM reminders WHERE id = ? AND user_id = ?", reminder_id, session["user_id"])
    if not reminder:
        return redirect("/")

    if request.method == "POST":
        title = request.form.get("title")
        frequency = request.form.get("frequency")
        due_date = request.form.get("due_date")

        if not title or not frequency or not due_date:
            return render_template("edit.html", reminder=reminder[0], error="All fields are required.")

        db.execute("UPDATE reminders SET title = ?, frequency = ?, due_date = ? WHERE id = ? AND user_id = ?",
                   title, frequency, due_date, reminder_id, session["user_id"])
        return redirect("/")

    return render_template("edit.html", reminder=reminder[0])


@app.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    db.execute("DELETE FROM reminders WHERE id = ? AND user_id = ?", id, session["user_id"])
    return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]

    if request.method == "POST":
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not new_username:
            return render_template("profile.html", error="Username is required.", user=None)

        if new_password:
            if new_password != confirm:
                return render_template("profile.html", error="Passwords do not match.", user=None)
            hashed_pw = generate_password_hash(new_password)
            db.execute("UPDATE users SET username = ?, hash = ? WHERE id = ?", new_username, hashed_pw, user_id)
        else:
            db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, user_id)

        flash("Profile updated successfully!")
        return redirect("/profile")

    user = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]
    return render_template("profile.html", user=user)
