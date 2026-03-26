import sqlite3
import os

DB_PATH = "db.sqlite"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        content TEXT
    )
    """)

    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")

    cursor.execute("INSERT INTO comments (author, content) VALUES ('admin', 'Bienvenidos a la aplicación')")
    cursor.execute("INSERT INTO comments (author, content) VALUES ('user', 'Primer comentario de prueba')")

    conn.commit()
    conn.close()

    print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()
