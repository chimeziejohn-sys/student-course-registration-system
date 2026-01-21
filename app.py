from flask import Flask, render_template, request, redirect, session
import sqlite3
import database

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO student (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        db.commit()
        db.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM student WHERE email=? AND password=?",
            (email, password)
        )
        student = cursor.fetchone()
        db.close()

        if student:
            session["student_id"] = student[0]
            session["name"] = student[1]
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    db.close()
    return render_template("dashboard.html", courses=courses)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
