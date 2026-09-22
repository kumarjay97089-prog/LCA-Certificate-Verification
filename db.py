import sqlite3

DATABASE = "certificate.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_certificate(certificate_no):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            certificate_no,
            registration_no,
            student_name,
            father_name,
            mother_name,
            date_of_birth,
            course,
            session,
            result,
            issue_date
        FROM students
        WHERE certificate_no = ?
    """, (certificate_no,))

    student = cursor.fetchone()

    conn.close()

    return student