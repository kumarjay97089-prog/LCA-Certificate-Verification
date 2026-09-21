import sqlite3

# Database connection
connection = sqlite3.connect("certificate.db")
cursor = connection.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificate_no TEXT UNIQUE NOT NULL,
    student_name TEXT NOT NULL,
    course TEXT NOT NULL,
    session TEXT NOT NULL,
    result TEXT NOT NULL
)
""")

# Test Student
try:
    cursor.execute("""
    INSERT INTO students
    (certificate_no, student_name, course, session, result)
    VALUES (?, ?, ?, ?, ?)
    """, (
        "LCA-ADCA-2026-0001",
        "Rahul Kumar",
        "ADCA",
        "2025-26",
        "PASSED"
    ))

    print("Student added successfully!")

except sqlite3.IntegrityError:
    print("Student already exists.")

# Save
connection.commit()

# Close
connection.close()