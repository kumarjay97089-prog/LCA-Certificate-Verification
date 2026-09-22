import sqlite3

DB_NAME = "certificate.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificate_no TEXT UNIQUE NOT NULL,
    registration_no TEXT,
    student_name TEXT NOT NULL,
    father_name TEXT,
    mother_name TEXT,
    date_of_birth TEXT,
    course TEXT NOT NULL,
    session TEXT NOT NULL,
    result TEXT NOT NULL,
    issue_date TEXT
)
""")

conn.commit()
conn.close()

print("Database structure ready.")