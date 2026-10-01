from flask import Flask, request, render_template_string, send_file, jsonify
from db import get_certificate, get_result, get_admit_card

import os
import sqlite3
from io import BytesIO
from werkzeug.utils import secure_filename

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


app = Flask(__name__)


# ============================================================
# ONLINE SYNC SECURITY TOKEN
# ============================================================

SYNC_TOKEN = os.environ.get(
    "LCA_SYNC_TOKEN",
    ""
)


# ============================================================
# COMMON CSS
# ============================================================

CSS = """
<style>
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background: #f2f5f9;
}

.header {
    background: #0b2d5c;
    color: white;
    padding: 22px 10px;
    text-align: center;
}

.header h1 {
    margin: 0;
    font-size: 28px;
}

.header p {
    margin: 6px 0 0 0;
    font-size: 14px;
}

.container {
    max-width: 650px;
    margin: 30px auto;
    padding: 0 15px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.card h2 {
    color: #0b2d5c;
    text-align: center;
    margin-top: 0;
}

label {
    display: block;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 6px;
}

input {
    width: 100%;
    box-sizing: border-box;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 7px;
    font-size: 16px;
}

button {
    width: 100%;
    margin-top: 20px;
    padding: 13px;
    background: #0b2d5c;
    color: white;
    border: none;
    border-radius: 7px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #174a8c;
}

.menu {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 20px auto;
    max-width: 650px;
}

.menu a {
    text-decoration: none;
    background: white;
    color: #0b2d5c;
    padding: 10px 15px;
    border-radius: 7px;
    font-weight: bold;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.success {
    background: #e8f7ed;
    color: #146c2e;
    border: 1px solid #a9dfb8;
    padding: 12px;
    border-radius: 7px;
    text-align: center;
    font-weight: bold;
}

.error {
    background: #fdeaea;
    color: #a40000;
    border: 1px solid #f0aaaa;
    padding: 12px;
    border-radius: 7px;
    text-align: center;
    font-weight: bold;
}

.info-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

.info-table td {
    border: 1px solid #ddd;
    padding: 10px;
}

.info-table td:first-child {
    font-weight: bold;
    background: #f4f6f8;
    width: 40%;
}

.footer {
    text-align: center;
    color: #666;
    font-size: 13px;
    padding: 25px 10px;
}
</style>
"""


# ============================================================
# HEADER + MENU
# ============================================================

def page_header():

    return """
    <div class="header">
        <h1>LAKSHYA COMPUTER ACADEMY</h1>
        <p>Akhauripur Gola, Chausa, Buxar - 802114</p>
    </div>

    <div class="menu">
        <a href="/">Certificate Verification</a>
        <a href="/result">Online Result</a>
        <a href="/admit-card">Online Admit Card</a>
    </div>
    """


# ============================================================
# CERTIFICATE HTML
# ============================================================

CERTIFICATE_HTML = CSS + page_header() + """

<div class="container">

    <div class="card">

        <h2>Certificate Verification</h2>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if student %}

            <div class="success">
                ✓ Certificate Verified Successfully
            </div>

            <table class="info-table">

                <tr>
                    <td>Certificate No.</td>
                    <td>{{ student['certificate_no'] }}</td>
                </tr>

                <tr>
                    <td>Registration No.</td>
                    <td>{{ student['registration_no'] }}</td>
                </tr>

                <tr>
                    <td>Student Name</td>
                    <td>{{ student['student_name'] }}</td>
                </tr>

                <tr>
                    <td>Father's Name</td>
                    <td>{{ student['father_name'] }}</td>
                </tr>

                <tr>
                    <td>Mother's Name</td>
                    <td>{{ student['mother_name'] }}</td>
                </tr>

                <tr>
                    <td>Date of Birth</td>
                    <td>{{ student['date_of_birth'] }}</td>
                </tr>

                <tr>
                    <td>Course</td>
                    <td>{{ student['course'] }}</td>
                </tr>

                <tr>
                    <td>Session</td>
                    <td>{{ student['session'] }}</td>
                </tr>

                <tr>
                    <td>Result</td>
                    <td>{{ student['result'] }}</td>
                </tr>

                <tr>
                    <td>Issue Date</td>
                    <td>{{ student['issue_date'] }}</td>
                </tr>

            </table>

        {% else %}

            <form method="POST">

                <label>Certificate Number</label>

                <input
                    type="text"
                    name="certificate_no"
                    placeholder="Enter Certificate No."
                    required
                >

                <button type="submit">
                    VERIFY CERTIFICATE
                </button>

            </form>

        {% endif %}

    </div>

</div>

<div class="footer">
    © LAKSHYA COMPUTER ACADEMY
</div>
"""


# ============================================================
# RESULT HTML
# ============================================================

RESULT_HTML = CSS + page_header() + """

<div class="container">

    <div class="card">

        <h2>Online Result</h2>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if student %}

            <div class="success">
                ✓ Result Found Successfully
            </div>

            <table class="info-table">

                <tr>
                    <td>Roll No.</td>
                    <td>{{ student['roll_no'] }}</td>
                </tr>

                <tr>
                    <td>Student Name</td>
                    <td>{{ student['student_name'] }}</td>
                </tr>

                <tr>
                    <td>Father's Name</td>
                    <td>{{ student['father_name'] }}</td>
                </tr>

                <tr>
                    <td>Mother's Name</td>
                    <td>{{ student['mother_name'] }}</td>
                </tr>

                <tr>
                    <td>Date of Birth</td>
                    <td>{{ student['date_of_birth'] }}</td>
                </tr>

                <tr>
                    <td>Registration No.</td>
                    <td>{{ student['registration_no'] }}</td>
                </tr>

                <tr>
                    <td>Course</td>
                    <td>{{ student['course'] }}</td>
                </tr>

                <tr>
                    <td>Session</td>
                    <td>{{ student['session'] }}</td>
                </tr>

                <tr>
                    <td>Result</td>
                    <td><strong>{{ student['result'] }}</strong></td>
                </tr>

            </table>

        {% else %}

            <form method="POST">

                <label>Roll Number</label>

                <input
                    type="text"
                    name="roll_no"
                    placeholder="Enter Roll No."
                    required
                >

                <label>Date of Birth</label>

                <input
                    type="text"
                    name="date_of_birth"
                    placeholder="DD-MM-YYYY"
                    required
                >

                <button type="submit">
                    CHECK RESULT
                </button>

            </form>

        {% endif %}

    </div>

</div>

<div class="footer">
    © LAKSHYA COMPUTER ACADEMY
</div>
"""


# ============================================================
# ADMIT CARD HTML
# ============================================================

ADMIT_CARD_HTML = CSS + page_header() + """

<div class="container">

    <div class="card">

        <h2>Online Admit Card</h2>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST">

            <label>Registration Number</label>

            <input
                type="text"
                name="registration_no"
                placeholder="Enter Registration No."
                required
            >

            <label>Date of Birth</label>

            <input
                type="text"
                name="date_of_birth"
                placeholder="DD-MM-YYYY"
                required
            >

            <button type="submit">
                DOWNLOAD ADMIT CARD
            </button>

        </form>

    </div>

</div>

<div class="footer">
    © LAKSHYA COMPUTER ACADEMY
</div>
"""


# ============================================================
# CERTIFICATE VERIFICATION
# ============================================================

@app.route("/", methods=["GET", "POST"])
def verify():

    student = None
    error = None

    if request.method == "POST":

        certificate_no = request.form.get(
            "certificate_no",
            ""
        ).strip()

        if certificate_no:

            student = get_certificate(
                certificate_no
            )

            if not student:

                error = (
                    "✗ Certificate not found. "
                    "Please check Certificate Number."
                )

        else:

            error = "Please enter Certificate Number."

    return render_template_string(
        CERTIFICATE_HTML,
        student=student,
        error=error
    )


# ============================================================
# QR VERIFICATION
# ============================================================

@app.route("/verify/<certificate_no>")
def verify_qr(certificate_no):

    student = get_certificate(
        certificate_no
    )

    error = None

    if not student:

        error = "✗ Certificate not found."

    return render_template_string(
        CERTIFICATE_HTML,
        student=student,
        error=error
    )


# ============================================================
# ONLINE RESULT
# ============================================================

@app.route("/result", methods=["GET", "POST"])
def result():

    student = None
    error = None

    if request.method == "POST":

        roll_no = request.form.get(
            "roll_no",
            ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth",
            ""
        ).strip()

        if roll_no and date_of_birth:

            student = get_result(
                roll_no,
                date_of_birth
            )

            if not student:

                error = (
                    "✗ Result not found. "
                    "Please check Roll No. "
                    "and Date of Birth."
                )

        else:

            error = (
                "Please enter Roll No. "
                "and Date of Birth."
            )

    return render_template_string(
        RESULT_HTML,
        student=student,
        error=error
    )


# ============================================================
# FIND LOCAL IMAGE
# ============================================================

def find_image(image_path):

    if not image_path:
        return None

    if os.path.exists(image_path):
        return image_path

    relative_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        image_path
    )

    if os.path.exists(relative_path):
        return relative_path

    return None


# ============================================================
# ADMIT CARD PDF
# ============================================================

def generate_admit_card_pdf(student):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    address_style = ParagraphStyle(
        "AddressStyle",
        parent=styles["Normal"],
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        alignment=TA_CENTER,
        spaceBefore=5,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )

    story = []

    # ========================================================
    # HEADER
    # ========================================================

    story.append(
        Paragraph(
            "LAKSHYA COMPUTER ACADEMY",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Akhauripur Gola, Chausa, Buxar - 802114",
            address_style
        )
    )

    story.append(
        Paragraph(
            "ADMIT CARD",
            heading_style
        )
    )

    # ========================================================
    # SESSION
    # ========================================================

    session_data = [
        [
            Paragraph(
                "<b>Session</b>",
                normal_style
            ),
            Paragraph(
                str(student["session"] or ""),
                normal_style
            )
        ]
    ]

    session_table = Table(
        session_data,
        colWidths=[
            45 * mm,
            125 * mm
        ]
    )

    session_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.7, colors.black),
            ("BACKGROUND", (0, 0), (0, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(session_table)

    story.append(
        Spacer(1, 8)
    )

    # ========================================================
    # STUDENT PHOTO
    # ========================================================

    photo = None

    photo_path = find_image(
        student["photo_path"]
    )

    if photo_path:

        try:

            photo = Image(
                photo_path,
                width=35 * mm,
                height=45 * mm
            )

        except Exception:

            photo = None

    if photo is None:

        photo = Paragraph(
            "<b>PHOTO</b>",
            ParagraphStyle(
                "PhotoPlaceholder",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=11
            )
        )

    # ========================================================
    # SYSTEM STUDENT SIGNATURE
    # ========================================================

    system_signature = None

    signature_path = find_image(
        student["signature_path"]
    )

    if signature_path:

        try:

            system_signature = Image(
                signature_path,
                width=35 * mm,
                height=12 * mm
            )

        except Exception:

            system_signature = None

    if system_signature is None:

        system_signature = Paragraph(
            "",
            small_style
        )

    # ========================================================
    # STUDENT INFORMATION
    # ========================================================

    student_info_data = [

        [
            Paragraph(
                "<b>Registration No.</b>",
                normal_style
            ),
            Paragraph(
                str(student["registration_no"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Roll No.</b>",
                normal_style
            ),
            Paragraph(
                str(student["roll_no"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Student Name</b>",
                normal_style
            ),
            Paragraph(
                str(student["student_name"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Father's Name</b>",
                normal_style
            ),
            Paragraph(
                str(student["father_name"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Mother's Name</b>",
                normal_style
            ),
            Paragraph(
                str(student["mother_name"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Date of Birth</b>",
                normal_style
            ),
            Paragraph(
                str(student["date_of_birth"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Course</b>",
                normal_style
            ),
            Paragraph(
                str(student["course"] or ""),
                normal_style
            )
        ]
    ]

    student_info_table = Table(
        student_info_data,
        colWidths=[
            42 * mm,
            88 * mm
        ],
        rowHeights=[
            10 * mm,
            10 * mm,
            10 * mm,
            10 * mm,
            10 * mm,
            10 * mm,
            10 * mm
        ]
    )

    student_info_table.setStyle(
        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.7, colors.black),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )

    # ========================================================
    # PHOTO + SYSTEM SIGNATURE
    # ========================================================

    photo_signature_block = Table(
        [
            [
                photo
            ],
            [
                system_signature
            ],
            [
                Paragraph(
                    "System Signature",
                    small_style
                )
            ]
        ],
        colWidths=[
            40 * mm
        ],
        rowHeights=[
            45 * mm,
            14 * mm,
            8 * mm
        ]
    )

    photo_signature_block.setStyle(
        TableStyle([

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),

            ("BOX", (0, 0), (-1, -1), 0.7, colors.black),
        ])
    )

    # ========================================================
    # COMBINE STUDENT INFORMATION + PHOTO/SIGNATURE
    # ========================================================

    student_main_table = Table(
        [
            [
                student_info_table,
                photo_signature_block
            ]
        ],
        colWidths=[
            130 * mm,
            40 * mm
        ]
    )

    student_main_table.setStyle(
        TableStyle([

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),

        ])
    )

    story.append(student_main_table)

    story.append(
        Spacer(1, 10)
    )

    # ========================================================
    # EXAM DETAILS
    # ========================================================

    story.append(
        Paragraph(
            "EXAMINATION DETAILS",
            heading_style
        )
    )

    exam_data = [

        [
            Paragraph(
                "<b>Exam Date</b>",
                normal_style
            ),
            Paragraph(
                str(student["exam_date"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Exam Time</b>",
                normal_style
            ),
            Paragraph(
                str(student["exam_time"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Reporting Time</b>",
                normal_style
            ),
            Paragraph(
                str(student["reporting_time"] or ""),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Exam Center</b>",
                normal_style
            ),
            Paragraph(
                str(student["exam_center"] or ""),
                normal_style
            )
        ]
    ]

    exam_table = Table(
        exam_data,
        colWidths=[
            55 * mm,
            115 * mm
        ]
    )

    exam_table.setStyle(
        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.7, colors.black),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(exam_table)

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # INSTRUCTIONS
    # ========================================================

    story.append(
        Paragraph(
            "<b>IMPORTANT INSTRUCTIONS</b>",
            heading_style
        )
    )

    instructions = [

        "1. Candidate must bring this Admit Card to the examination center.",

        "2. Candidate should report at the examination center before the reporting time.",

        "3. Candidate must follow all instructions given by the examination authority.",

        "4. Mobile phones and other prohibited electronic devices may not be allowed in the examination hall.",

        "5. Admit Card should be kept safely until completion of the examination."
    ]

    for instruction in instructions:

        story.append(
            Paragraph(
                instruction,
                small_style
            )
        )

        story.append(
            Spacer(1, 3)
        )

    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # EXAM HALL CANDIDATE SIGNATURE
    # ========================================================

    candidate_signature = Paragraph(
        "____________________________<br/>"
        "<b>Candidate Signature</b><br/>"
        "<font size=7>(To be signed in the examination hall)</font>",
        normal_style
    )

    # ========================================================
    # AUTHORIZED SIGNATURE
    # ========================================================

    authorized_signature = Paragraph(
        "____________________________<br/>"
        "<b>Authorized Signature</b>",
        normal_style
    )

    signature_data = [
        [
            candidate_signature,
            authorized_signature
        ]
    ]

    signature_table = Table(
        signature_data,
        colWidths=[
            85 * mm,
            85 * mm
        ]
    )

    signature_table.setStyle(
        TableStyle([

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),

            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),

            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(signature_table)

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # FOOTER
    # ========================================================

    story.append(
        Paragraph(
            "This is a computer generated Admit Card.",
            ParagraphStyle(
                "FooterStyle",
                parent=small_style,
                alignment=TA_CENTER
            )
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(story)

    buffer.seek(0)

    return buffer


# ============================================================
# ONLINE ADMIT CARD
# ============================================================

@app.route(
    "/admit-card",
    methods=["GET", "POST"]
)
def admit_card():

    error = None

    if request.method == "POST":

        registration_no = request.form.get(
            "registration_no",
            ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth",
            ""
        ).strip()

        if not registration_no or not date_of_birth:

            error = (
                "Please enter Registration No. "
                "and Date of Birth."
            )

        else:

            student = get_admit_card(
                registration_no,
                date_of_birth
            )

            if not student:

                error = (
                    "✗ Admit Card not found. "
                    "Please check Registration No. "
                    "and Date of Birth."
                )

            else:

                try:

                    pdf_buffer = generate_admit_card_pdf(
                        student
                    )

                    roll_no = (
                        student["roll_no"]
                        or "Admit_Card"
                    )

                    filename = (
                        "Admit_Card_"
                        + str(roll_no)
                        + ".pdf"
                    )

                    return send_file(
                        pdf_buffer,
                        mimetype="application/pdf",
                        as_attachment=True,
                        download_name=filename
                    )

                except Exception as e:

                    error = (
                        "PDF generation error: "
                        + str(e)
                    )

    return render_template_string(
        ADMIT_CARD_HTML,
        error=error
    )


# ============================================================
# SYNC DATABASE CONNECTION
# ============================================================

def sync_db_connection():

    database_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "certificate.db"
    )

    conn = sqlite3.connect(
        database_path
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# SAVE SYNC IMAGE
# ============================================================

def save_sync_file(
    uploaded_file,
    folder_name,
    registration_no
):

    if not uploaded_file:

        return None

    original_name = secure_filename(
        uploaded_file.filename or ""
    )

    if not original_name:

        return None

    extension = os.path.splitext(
        original_name
    )[1].lower()

    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    if extension not in allowed_extensions:

        raise ValueError(
            "Only JPG, JPEG and PNG files are allowed."
        )

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    folder_path = os.path.join(
        base_dir,
        folder_name
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    # Remove old image files
    for old_ext in allowed_extensions:

        old_file = os.path.join(
            folder_path,
            str(registration_no) + old_ext
        )

        if os.path.exists(old_file):

            try:

                os.remove(old_file)

            except Exception:

                pass

    filename = (
        str(registration_no)
        + extension
    )

    file_path = os.path.join(
        folder_path,
        filename
    )

    uploaded_file.save(
        file_path
    )

    return (
        folder_name
        + "/"
        + filename
    )


# ============================================================
# ONLINE STUDENT SYNC API
# ============================================================

@app.route(
    "/api/sync-student",
    methods=["POST"]
)
def sync_student():

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    token = request.headers.get(
        "X-Sync-Token",
        ""
    ).strip()

    if not SYNC_TOKEN:

        return jsonify({
            "success": False,
            "message": "Sync service is not configured."
        }), 503

    if token != SYNC_TOKEN:

        return jsonify({
            "success": False,
            "message": "Unauthorized sync request."
        }), 401


    # --------------------------------------------------------
    # GET FORM DATA
    # --------------------------------------------------------

    certificate_no = request.form.get(
        "certificate_no",
        ""
    ).strip()

    registration_no = request.form.get(
        "registration_no",
        ""
    ).strip()

    student_name = request.form.get(
        "student_name",
        ""
    ).strip()

    father_name = request.form.get(
        "father_name",
        ""
    ).strip()

    mother_name = request.form.get(
        "mother_name",
        ""
    ).strip()

    date_of_birth = request.form.get(
        "date_of_birth",
        ""
    ).strip()

    course = request.form.get(
        "course",
        ""
    ).strip()

    session = request.form.get(
        "session",
        ""
    ).strip()

    result_value = request.form.get(
        "result",
        ""
    ).strip()

    issue_date = request.form.get(
        "issue_date",
        ""
    ).strip()

    roll_no = request.form.get(
        "roll_no",
        ""
    ).strip()

    exam_date = request.form.get(
        "exam_date",
        ""
    ).strip()

    exam_time = request.form.get(
        "exam_time",
        ""
    ).strip()

    reporting_time = request.form.get(
        "reporting_time",
        ""
    ).strip()

    exam_center = request.form.get(
        "exam_center",
        ""
    ).strip()


    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    if not certificate_no:

        return jsonify({
            "success": False,
            "message": "Certificate Number is required."
        }), 400

    if not registration_no:

        return jsonify({
            "success": False,
            "message": "Registration Number is required."
        }), 400

    if not student_name:

        return jsonify({
            "success": False,
            "message": "Student Name is required."
        }), 400

    if not roll_no:

        return jsonify({
            "success": False,
            "message": "Roll Number is required."
        }), 400


    conn = None

    try:

        conn = sync_db_connection()

        cursor = conn.cursor()


        # ----------------------------------------------------
        # CHECK DUPLICATE REGISTRATION NUMBER
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT certificate_no
            FROM students
            WHERE registration_no = ?
            AND certificate_no != ?
            """,
            (
                registration_no,
                certificate_no
            )
        )

        registration_duplicate = cursor.fetchone()

        if registration_duplicate:

            return jsonify({
                "success": False,
                "message": (
                    "Registration Number already "
                    "belongs to another certificate."
                )
            }), 409


        # ----------------------------------------------------
        # CHECK DUPLICATE ROLL NUMBER
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT certificate_no
            FROM students
            WHERE roll_no = ?
            AND certificate_no != ?
            """,
            (
                roll_no,
                certificate_no
            )
        )

        roll_duplicate = cursor.fetchone()

        if roll_duplicate:

            return jsonify({
                "success": False,
                "message": (
                    "Roll Number already "
                    "belongs to another certificate."
                )
            }), 409


        # ----------------------------------------------------
        # CHECK EXISTING CERTIFICATE
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE certificate_no = ?
            """,
            (certificate_no,)
        )

        existing_student = cursor.fetchone()


        # ----------------------------------------------------
        # PHOTO
        # ----------------------------------------------------

        photo_file = request.files.get(
            "photo"
        )

        signature_file = request.files.get(
            "signature"
        )

        photo_path = None
        signature_path = None


        if photo_file and photo_file.filename:

            photo_path = save_sync_file(
                photo_file,
                "photos",
                registration_no
            )

        elif existing_student:

            photo_path = existing_student["photo_path"]


        # ----------------------------------------------------
        # SIGNATURE
        # ----------------------------------------------------

        if signature_file and signature_file.filename:

            signature_path = save_sync_file(
                signature_file,
                "signatures",
                registration_no
            )

        elif existing_student:

            signature_path = existing_student["signature_path"]


        # ----------------------------------------------------
        # UPDATE EXISTING STUDENT
        # ----------------------------------------------------

        if existing_student:

            cursor.execute(
                """
                UPDATE students
                SET
                    registration_no = ?,
                    student_name = ?,
                    father_name = ?,
                    mother_name = ?,
                    date_of_birth = ?,
                    course = ?,
                    session = ?,
                    result = ?,
                    issue_date = ?,
                    roll_no = ?,
                    exam_date = ?,
                    exam_time = ?,
                    reporting_time = ?,
                    exam_center = ?,
                    photo_path = ?,
                    signature_path = ?
                WHERE certificate_no = ?
                """,
                (
                    registration_no,
                    student_name,
                    father_name,
                    mother_name,
                    date_of_birth,
                    course,
                    session,
                    result_value,
                    issue_date,
                    roll_no,
                    exam_date,
                    exam_time,
                    reporting_time,
                    exam_center,
                    photo_path,
                    signature_path,
                    certificate_no
                )
            )

            action = "updated"


        # ----------------------------------------------------
        # ADD NEW STUDENT
        # ----------------------------------------------------

        else:

            cursor.execute(
                """
                INSERT INTO students (
                    certificate_no,
                    registration_no,
                    student_name,
                    father_name,
                    mother_name,
                    date_of_birth,
                    course,
                    session,
                    result,
                    issue_date,
                    roll_no,
                    exam_date,
                    exam_time,
                    reporting_time,
                    exam_center,
                    photo_path,
                    signature_path
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    certificate_no,
                    registration_no,
                    student_name,
                    father_name,
                    mother_name,
                    date_of_birth,
                    course,
                    session,
                    result_value,
                    issue_date,
                    roll_no,
                    exam_date,
                    exam_time,
                    reporting_time,
                    exam_center,
                    photo_path,
                    signature_path
                )
            )

            action = "added"


        conn.commit()


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "action": action,
            "certificate_no": certificate_no,
            "registration_no": registration_no,
            "student_name": student_name,
            "message": (
                "Student data "
                + action
                + " successfully online."
            )
        })


    except Exception as e:

        if conn:

            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


    finally:

        if conn:

            conn.close()


# ============================================================
# START LOCAL SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("===================================")
    print("LAKSHYA COMPUTER ACADEMY")
    print("CERTIFICATE + RESULT + ADMIT CARD")
    print("ONLINE STUDENT SYNC API")
    print("===================================")
    print()

    print("Certificate Verification:")
    print("http://127.0.0.1:5000")
    print()

    print("Online Result:")
    print("http://127.0.0.1:5000/result")
    print()

    print("Online Admit Card:")
    print("http://127.0.0.1:5000/admit-card")
    print()

    print("Online Sync API:")
    print("http://127.0.0.1:5000/api/sync-student")
    print()

    print("===================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
