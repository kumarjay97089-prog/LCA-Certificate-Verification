from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)


# ==============================
# DATABASE SEARCH
# ==============================

def get_certificate(certificate_no):

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

    return student


# ==============================
# HTML PAGE
# ==============================

HTML = """
<!DOCTYPE html>
<html>
<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Certificate Verification</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background: #f2f5f9;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 650px;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }

        h1 {
            text-align: center;
            color: #123B6D;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #555;
            margin-bottom: 25px;
        }

        input {
            width: 100%;
            box-sizing: border-box;
            padding: 13px;
            font-size: 16px;
            border: 1px solid #bbb;
            border-radius: 6px;
            margin-bottom: 12px;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #123B6D;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #0b2c52;
        }

        .valid {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            background: #e8f7ee;
            border: 2px solid #2e8b57;
        }

        .valid-title {
            color: #16733c;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 15px;
        }

        .invalid {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            background: #fdeaea;
            border: 2px solid #cc3333;
        }

        .invalid-title {
            color: #b22222;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
        }

        .detail {
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }

        .label {
            font-weight: bold;
            color: #333;
        }

        .footer {
            text-align: center;
            color: #666;
            font-size: 13px;
            margin-top: 25px;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>LAKSHYA COMPUTER ACADEMY</h1>

    <div class="subtitle">
        Certificate Verification System
    </div>

    <form method="POST">

        <input
            type="text"
            name="certificate_no"
            placeholder="Enter Certificate Number"
            value="{{ certificate_no }}"
            required
        >

        <button type="submit">
            VERIFY CERTIFICATE
        </button>

    </form>


    {% if student %}

    <div class="valid">

        <div class="valid-title">
            ✓ CERTIFICATE VERIFIED
        </div>

        <div class="detail">
            <span class="label">Certificate No.:</span>
            {{ student[0] }}
        </div>

        <div class="detail">
            <span class="label">Registration No.:</span>
            {{ student[1] }}
        </div>

        <div class="detail">
            <span class="label">Student Name:</span>
            {{ student[2] }}
        </div>

        <div class="detail">
            <span class="label">Father's Name:</span>
            {{ student[3] }}
        </div>

        <div class="detail">
            <span class="label">Mother's Name:</span>
            {{ student[4] }}
        </div>

        <div class="detail">
            <span class="label">Date of Birth:</span>
            {{ student[5] }}
        </div>

        <div class="detail">
            <span class="label">Course:</span>
            {{ student[6] }}
        </div>

        <div class="detail">
            <span class="label">Session:</span>
            {{ student[7] }}
        </div>

        <div class="detail">
            <span class="label">Result:</span>
            {{ student[8] }}
        </div>

        <div class="detail">
            <span class="label">Issue Date:</span>
            {{ student[9] }}
        </div>

    </div>

    {% elif searched %}

    <div class="invalid">

        <div class="invalid-title">
            ✗ CERTIFICATE NOT FOUND
        </div>

        <p style="text-align:center;">
            The entered certificate number does not
            exist in the database.
        </p>

    </div>

    {% endif %}


    <div class="footer">

        Akhauripur Gola, Chausa, Buxar - 802114

        <br><br>

        LAKSHYA COMPUTER ACADEMY

    </div>

</div>

</body>
</html>
"""


# ==============================
# VERIFICATION ROUTE
# ==============================

@app.route("/", methods=["GET", "POST"])
def verify():

    student = None
    searched = False
    certificate_no = ""

    if request.method == "POST":

        certificate_no = request.form.get(
            "certificate_no",
            ""
        ).strip()

        student = get_certificate(certificate_no)

        searched = True

    return render_template_string(
        HTML,
        student=student,
        searched=searched,
        certificate_no=certificate_no
    )

# ==============================
# QR VERIFICATION ROUTE
# ==============================

@app.route("/verify/<certificate_no>")
def qr_verify(certificate_no):

    student = get_certificate(certificate_no)

    if student:
        return render_template_string(
            HTML,
            student=student,
            searched=True,
            certificate_no=certificate_no
        )

    return render_template_string(
        HTML,
        student=None,
        searched=True,
        certificate_no=certificate_no
    )
# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":

    print("===================================")
    print("LAKSHYA CERTIFICATE VERIFICATION")
    print("===================================")
    print("Open browser:")
    print("http://127.0.0.1:5000")
    print("===================================")

    app.run(
    host="0.0.0.0",
    port=5000
)