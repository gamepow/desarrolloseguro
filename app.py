import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv() # Cargar Variables de Entorno

app = Flask(__name__)

# VULNERABLE: Nunca hardcodear secretos en el código
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(32))
DB_PATH = "db.sqlite"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db_connection()
        cursor = conn.cursor()

	# VULNERABLE: antes se construía la query con f-string (SQL Injection)
        #query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
	#cursor.execute(query)
        # VULNERABLE: este print exponía credenciales y estructura de la BBDD en logs
	#print(f"[DEBUG] Query ejecutada: {query}")

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = user["username"]
            return redirect(url_for("comments"))
        else:
            error = "Credenciales incorrectas"

    return render_template("index.html", error=error)


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if "username" not in session:
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        content = request.form.get("content", "")
        author = session["username"]

        cursor.execute(
            "INSERT INTO comments (author, content) VALUES (?, ?)",
            (author, content)
        )
        conn.commit()

    cursor.execute("SELECT * FROM comments")
    comments_list = cursor.fetchall()
    conn.close()

    return render_template(
        "comments.html",
        comments=comments_list,
        username=session["username"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
