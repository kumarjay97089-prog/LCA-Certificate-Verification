import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect_database():
    return sqlite3.connect("certificate.db")


# ==========================================
# AUTOMATIC CERTIFICATE NUMBER
# ==========================================

def generate_certificate_number(course, session):

    # Session जैसे 2025-26 से 2025 निकालेगा
    year = session.split("-")[0].strip()

    course_code = course.upper().replace(" ", "")

    prefix = f"LCA-{course_code}-{year}-"

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT certificate_no
        FROM students
        WHERE certificate_no LIKE ?
        ORDER BY certificate_no DESC
        LIMIT 1
    """, (prefix + "%",))

    last_certificate = cursor.fetchone()

    connection.close()

    if last_certificate:

        last_number = last_certificate[0].split("-")[-1]

        try:
            next_number = int(last_number) + 1
        except ValueError:
            next_number = 1

    else:
        next_number = 1

    return f"{prefix}{next_number:04d}"


# ==========================================
# SEARCH CERTIFICATE
# ==========================================

def search_certificate():

    certificate_no = certificate_entry.get().strip()

    if certificate_no == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Certificate Number."
        )
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT certificate_no,
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

    connection.close()

    if student:

        result_text.set(
            f"Certificate No.: {student[0]}\n"
            f"Registration No.: {student[1] or '-'}\n"
            f"Student Name: {student[2]}\n"
            f"Father's Name: {student[3] or '-'}\n"
            f"Mother's Name: {student[4] or '-'}\n"
            f"Date of Birth: {student[5] or '-'}\n"
            f"Course: {student[6]}\n"
            f"Session: {student[7]}\n"
            f"Result: {student[8]}\n"
            f"Issue Date: {student[9] or '-'}\n\n"
            f"STATUS: VALID CERTIFICATE"
        )

        result_label.config(fg="green")

    else:

        result_text.set(
            "❌ Certificate Not Found."
        )

        result_label.config(fg="red")


# ==========================================
# ADD NEW STUDENT
# ==========================================

def add_student_window():

    add_window = tk.Toplevel(root)

    add_window.title("Add New Student")

    add_window.geometry("560x720")

    add_window.resizable(False, False)

    tk.Label(
        add_window,
        text="ADD NEW STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    form_frame = tk.Frame(add_window)
    form_frame.pack(pady=5)

    # ======================================
    # CERTIFICATE NUMBER
    # ======================================

    tk.Label(
        form_frame,
        text="Certificate Number",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=0, column=0, pady=6)

    certificate_no_var = tk.StringVar()

    certificate_no_entry = tk.Entry(
        form_frame,
        textvariable=certificate_no_var,
        font=("Arial", 11),
        width=32,
        state="readonly"
    )

    certificate_no_entry.grid(
        row=0,
        column=1,
        pady=6
    )

    # ======================================
    # REGISTRATION NUMBER
    # ======================================

    tk.Label(
        form_frame,
        text="Registration No.",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=1, column=0, pady=6)

    registration_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    registration_entry.grid(
        row=1,
        column=1,
        pady=6
    )

    # ======================================
    # STUDENT NAME
    # ======================================

    tk.Label(
        form_frame,
        text="Student Name",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=2, column=0, pady=6)

    student_name_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    student_name_entry.grid(
        row=2,
        column=1,
        pady=6
    )

    # ======================================
    # FATHER NAME
    # ======================================

    tk.Label(
        form_frame,
        text="Father's Name",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=3, column=0, pady=6)

    father_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    father_entry.grid(
        row=3,
        column=1,
        pady=6
    )

    # ======================================
    # MOTHER NAME
    # ======================================

    tk.Label(
        form_frame,
        text="Mother's Name",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=4, column=0, pady=6)

    mother_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    mother_entry.grid(
        row=4,
        column=1,
        pady=6
    )

    # ======================================
    # DATE OF BIRTH
    # ======================================

    tk.Label(
        form_frame,
        text="Date of Birth",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=5, column=0, pady=6)

    dob_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    dob_entry.grid(
        row=5,
        column=1,
        pady=6
    )

    # ======================================
    # COURSE DROPDOWN
    # ======================================

    tk.Label(
        form_frame,
        text="Course",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=6, column=0, pady=6)

    course_combo = ttk.Combobox(
        form_frame,
        font=("Arial", 11),
        width=30,
        state="readonly"
    )

    course_combo["values"] = (
        "ADCA",
        "DCA",
        "CCC",
        "TALLY PRIME",
        "DTP",
        "ADCA+",
        "TYPING"
    )

    course_combo.grid(
        row=6,
        column=1,
        pady=6
    )

    # ======================================
    # SESSION
    # ======================================

    tk.Label(
        form_frame,
        text="Session",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=7, column=0, pady=6)

    session_combo = ttk.Combobox(
        form_frame,
        font=("Arial", 11),
        width=30,
        state="readonly"
    )

    session_combo["values"] = (
        "2025-26",
        "2026-27",
        "2027-28",
        "2028-29",
        "2029-30"
    )

    session_combo.grid(
        row=7,
        column=1,
        pady=6
    )

    # ======================================
    # RESULT
    # ======================================

    tk.Label(
        form_frame,
        text="Result",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=8, column=0, pady=6)

    result_combo = ttk.Combobox(
        form_frame,
        font=("Arial", 11),
        width=30,
        state="readonly"
    )

    result_combo["values"] = (
        "PASSED",
        "FAILED",
        "ABSENT"
    )

    result_combo.grid(
        row=8,
        column=1,
        pady=6
    )

    # ======================================
    # ISSUE DATE
    # ======================================

    tk.Label(
        form_frame,
        text="Issue Date",
        font=("Arial", 11),
        width=20,
        anchor="w"
    ).grid(row=9, column=0, pady=6)

    issue_date_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        width=32
    )

    issue_date_entry.grid(
        row=9,
        column=1,
        pady=6
    )

    # ======================================
    # GENERATE CERTIFICATE NUMBER
    # ======================================

    def update_certificate_number(event=None):

        course = course_combo.get()
        session = session_combo.get()

        if course and session:

            certificate_no = generate_certificate_number(
                course,
                session
            )

            certificate_no_var.set(
                certificate_no
            )

    course_combo.bind(
        "<<ComboboxSelected>>",
        update_certificate_number
    )

    session_combo.bind(
        "<<ComboboxSelected>>",
        update_certificate_number
    )

    # ======================================
    # SAVE STUDENT
    # ======================================

    def save_student():

        certificate_no = certificate_no_var.get().strip()
        registration_no = registration_entry.get().strip()
        student_name = student_name_entry.get().strip()
        father_name = father_entry.get().strip()
        mother_name = mother_entry.get().strip()
        date_of_birth = dob_entry.get().strip()
        course = course_combo.get().strip()
        session = session_combo.get().strip()
        result = result_combo.get().strip()
        issue_date = issue_date_entry.get().strip()

        if (
            certificate_no == ""
            or student_name == ""
            or course == ""
            or session == ""
            or result == ""
        ):

            messagebox.showwarning(
                "Warning",
                "Please fill all required fields."
            )

            return

        connection = connect_database()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO students
                (
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
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
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
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                f"Student added successfully.\n\n"
                f"Certificate No.: {certificate_no}"
            )

            add_window.destroy()

        except sqlite3.IntegrityError:

            connection.close()

            messagebox.showerror(
                "Error",
                "Certificate Number already exists."
            )

    tk.Button(
        add_window,
        text="SAVE STUDENT",
        font=("Arial", 12, "bold"),
        command=save_student,
        padx=25,
        pady=10
    ).pack(pady=20)


# ==========================================
# VIEW ALL STUDENTS
# ==========================================

def view_all_students():

    list_window = tk.Toplevel(root)

    list_window.title("Student Management")

    list_window.geometry("1250x650")

    list_window.resizable(False, False)

    tk.Label(
        list_window,
        text="STUDENT MANAGEMENT",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    table_frame = tk.Frame(list_window)
    table_frame.pack(pady=10)

    columns = (
        "certificate_no",
        "registration_no",
        "student_name",
        "father_name",
        "course",
        "session",
        "result",
        "issue_date"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=17
    )

    headings = {
        "certificate_no": "Certificate No.",
        "registration_no": "Registration No.",
        "student_name": "Student Name",
        "father_name": "Father's Name",
        "course": "Course",
        "session": "Session",
        "result": "Result",
        "issue_date": "Issue Date"
    }

    widths = {
        "certificate_no": 170,
        "registration_no": 150,
        "student_name": 160,
        "father_name": 160,
        "course": 120,
        "session": 100,
        "result": 100,
        "issue_date": 120
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=widths[column]
        )

    tree.pack(
        side="left"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ======================================
    # LOAD STUDENTS
    # ======================================

    def load_students():

        for item in tree.get_children():
            tree.delete(item)

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT certificate_no,
                   registration_no,
                   student_name,
                   father_name,
                   course,
                   session,
                   result,
                   issue_date
            FROM students
            ORDER BY id
        """)

        students = cursor.fetchall()

        connection.close()

        for student in students:

            tree.insert(
                "",
                "end",
                values=student
            )

    load_students()

    # ======================================
    # EDIT STUDENT
    # ======================================

    def edit_student():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )

            return

        values = tree.item(
            selected[0],
            "values"
        )

        edit_window = tk.Toplevel(list_window)

        edit_window.title("Edit Student")

        edit_window.geometry("550x650")

        edit_window.resizable(False, False)

        tk.Label(
            edit_window,
            text="EDIT STUDENT",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        form_frame = tk.Frame(edit_window)
        form_frame.pack()

        fields = [
            ("Certificate Number", values[0]),
            ("Registration No.", values[1]),
            ("Student Name", values[2]),
            ("Father's Name", values[3]),
            ("Course", values[4]),
            ("Session", values[5]),
            ("Result", values[6]),
            ("Issue Date", values[7])
        ]

        entries = []

        for row, (label_text, value) in enumerate(fields):

            tk.Label(
                form_frame,
                text=label_text,
                font=("Arial", 11),
                width=20,
                anchor="w"
            ).grid(
                row=row,
                column=0,
                pady=7
            )

            entry = tk.Entry(
                form_frame,
                font=("Arial", 11),
                width=32
            )

            entry.grid(
                row=row,
                column=1,
                pady=7
            )

            entry.insert(
                0,
                value
            )

            entries.append(entry)

        def update_student():

            new_values = [
                entry.get().strip()
                for entry in entries
            ]

            if (
                new_values[0] == ""
                or new_values[2] == ""
                or new_values[4] == ""
                or new_values[5] == ""
                or new_values[6] == ""
            ):

                messagebox.showwarning(
                    "Warning",
                    "Please fill required fields."
                )

                return

            connection = connect_database()
            cursor = connection.cursor()

            try:

                cursor.execute("""
                    UPDATE students
                    SET certificate_no = ?,
                        registration_no = ?,
                        student_name = ?,
                        father_name = ?,
                        course = ?,
                        session = ?,
                        result = ?,
                        issue_date = ?
                    WHERE certificate_no = ?
                """, (
                    new_values[0],
                    new_values[1],
                    new_values[2],
                    new_values[3],
                    new_values[4],
                    new_values[5],
                    new_values[6],
                    new_values[7],
                    values[0]
                ))

                connection.commit()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Student updated successfully."
                )

                edit_window.destroy()

                load_students()

            except sqlite3.IntegrityError:

                connection.close()

                messagebox.showerror(
                    "Error",
                    "Certificate Number already exists."
                )

        tk.Button(
            edit_window,
            text="UPDATE STUDENT",
            font=("Arial", 12, "bold"),
            command=update_student,
            padx=25,
            pady=10
        ).pack(pady=20)

    # ======================================
    # DELETE STUDENT
    # ======================================

    def delete_student():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )

            return

        values = tree.item(
            selected[0],
            "values"
        )

        certificate_no = values[0]
        student_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n"
            f"{student_name}\n"
            f"{certificate_no}?"
        )

        if not confirm:
            return

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE certificate_no = ?
        """, (certificate_no,))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully."
        )

        load_students()

    # ======================================
    # BUTTONS
    # ======================================

    button_frame = tk.Frame(list_window)
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="EDIT STUDENT",
        font=("Arial", 12, "bold"),
        command=edit_student,
        padx=25,
        pady=10
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    tk.Button(
        button_frame,
        text="DELETE STUDENT",
        font=("Arial", 12, "bold"),
        command=delete_student,
        padx=25,
        pady=10
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Button(
        button_frame,
        text="REFRESH",
        font=("Arial", 12, "bold"),
        command=load_students,
        padx=25,
        pady=10
    ).grid(
        row=0,
        column=2,
        padx=10
    )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Lakshya Computer Academy - Certificate Verification"
)

root.geometry("700x650")

root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

tk.Label(
    root,
    text="LAKSHYA COMPUTER ACADEMY",
    font=("Arial", 22, "bold")
).pack(pady=20)

tk.Label(
    root,
    text="Certificate Verification System",
    font=("Arial", 14)
).pack(pady=5)


# ==========================================
# SEARCH
# ==========================================

tk.Label(
    root,
    text="Enter Certificate Number",
    font=("Arial", 12)
).pack(pady=15)

certificate_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=35
)

certificate_entry.pack(pady=5)

tk.Button(
    root,
    text="SEARCH CERTIFICATE",
    font=("Arial", 12, "bold"),
    command=search_certificate,
    padx=20,
    pady=10
).pack(pady=15)


# ==========================================
# RESULT
# ==========================================

result_text = tk.StringVar()

result_label = tk.Label(
    root,
    textvariable=result_text,
    font=("Arial", 11),
    justify="left"
)

result_label.pack(pady=15)


# ==========================================
# ADD STUDENT
# ==========================================

tk.Button(
    root,
    text="ADD NEW STUDENT",
    font=("Arial", 12, "bold"),
    command=add_student_window,
    padx=20,
    pady=10
).pack(pady=8)


# ==========================================
# VIEW ALL STUDENTS
# ==========================================

tk.Button(
    root,
    text="VIEW ALL STUDENTS",
    font=("Arial", 12, "bold"),
    command=view_all_students,
    padx=20,
    pady=10
).pack(pady=8)


# ==========================================
# FOOTER
# ==========================================

tk.Label(
    root,
    text="Akhauripur Gola, Chausa, Buxar - 802114",
    font=("Arial", 10)
).pack(pady=20)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()