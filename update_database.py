import sqlite3


# ==========================================
# CONNECT DATABASE
# ==========================================

connection = sqlite3.connect("certificate.db")

cursor = connection.cursor()


# ==========================================
# ADD NEW COLUMNS
# ==========================================

columns = [
    ("registration_no", "TEXT"),
    ("father_name", "TEXT"),
    ("mother_name", "TEXT"),
    ("date_of_birth", "TEXT"),
    ("issue_date", "TEXT")
]


for column_name, column_type in columns:

    try:

        cursor.execute(
            f"""
            ALTER TABLE students
            ADD COLUMN {column_name} {column_type}
            """
        )

        print(
            f"Added: {column_name}"
        )

    except sqlite3.OperationalError:

        print(
            f"Already exists: {column_name}"
        )


# ==========================================
# SAVE CHANGES
# ==========================================

connection.commit()

connection.close()


print()
print("===================================")
print("DATABASE UPDATE COMPLETED")
print("===================================")