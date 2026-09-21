import tkinter as tk
from tkinter import messagebox
import sqlite3


# ==============================
# DATABASE SEARCH
# ==============================

def verify_certificate():

    certificate_no = certificate_entry.get().strip()

    if certificate_no == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Certificate Number"
        )
        return

    conn = sqlite3.connect("certificate.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT certificate_no, registration_no, student_name,
               father_name, mother_name, date_of_birth,
               course, session, result, issue_date
        FROM students
        WHERE certificate_no = ?
    """, (certificate_no,))

    student = cursor.fetchone()

    conn.close()

    # Clear previous result
    result_text.delete("1.0", tk.END)

    if student:

        (
            cert_no,
            registration_no,
            student_name,
            father_name,
            mother_name,
            date_of_birth,
            course,
            session,
            result,
            issue_date
        ) = student

        result_text.insert(
            tk.END,
            "✓ CERTIFICATE VERIFIED\n\n"
        )

        result_text.insert(
            tk.END,
            f"Certificate No. : {cert_no}\n"
            f"Registration No.: {registration_no}\n"
            f"Student Name    : {student_name}\n"
            f"Father's Name   : {father_name}\n"
            f"Mother's Name   : {mother_name}\n"
            f"Date of Birth   : {date_of_birth}\n"
            f"Course          : {course}\n"
            f"Session         : {session}\n"
            f"Result          : {result}\n"
            f"Issue Date      : {issue_date}\n"
        )

    else:

        result_text.insert(
            tk.END,
            "✗ CERTIFICATE NOT FOUND\n\n"
            "The entered certificate number\n"
            "does not exist in the database."
        )


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title(
    "Lakshya Computer Academy - Certificate Verification"
)

root.geometry("650x550")

root.resizable(False, False)


# ==============================
# TITLE
# ==============================

title = tk.Label(
    root,
    text="LAKSHYA COMPUTER ACADEMY",
    font=("Arial", 22, "bold")
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    root,
    text="Certificate Verification System",
    font=("Arial", 14)
)

subtitle.pack(pady=(0, 25))


# ==============================
# CERTIFICATE NUMBER
# ==============================

label = tk.Label(
    root,
    text="Enter Certificate Number",
    font=("Arial", 12, "bold")
)

label.pack()


certificate_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 14),
    justify="center"
)

certificate_entry.pack(pady=10)

certificate_entry.focus()


# ==============================
# VERIFY BUTTON
# ==============================

verify_button = tk.Button(
    root,
    text="VERIFY CERTIFICATE",
    font=("Arial", 12, "bold"),
    command=verify_certificate,
    padx=20,
    pady=10
)

verify_button.pack(pady=15)


# ==============================
# RESULT BOX
# ==============================

result_text = tk.Text(
    root,
    width=65,
    height=17,
    font=("Arial", 11)
)

result_text.pack(padx=20, pady=10)


# ==============================
# FOOTER
# ==============================

footer = tk.Label(
    root,
    text="Akhauripur Gola, Chausa, Buxar - 802114",
    font=("Arial", 9)
)

footer.pack(pady=5)


# ==============================
# START
# ==============================

root.mainloop()