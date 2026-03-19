import sqlite3

conn = sqlite3.connect("notes.db")
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

c.execute('''CREATE TABLE IF NOT EXISTS users (

user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
user_name TEXT NOT NULL,
user_email TEXT NOT NULL,
user_password TEXT NOT NULL
)''')

c.execute(''' CREATE TABLE IF NOT EXISTS notes(

note_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
note_title TEXT,
note_content TEXT NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')


conn.commit()
conn.close()