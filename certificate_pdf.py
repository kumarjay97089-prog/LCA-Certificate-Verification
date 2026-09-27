from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import sqlite3
import qrcode
import os


# ============================================================
# PROJECT BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "certificate.db"
)

CERTIFICATE_DIR = os.path.join(
    BASE_DIR,
    "certificates"
)

os.makedirs(
    CERTIFICATE_DIR,
    exist_ok=True
)


# ============================================================
# FIND IMAGE
# ============================================================

def find_image(path):

    if not path:
        return None

    path = str(path).strip()

    if not path:
        return None

    # Direct path
    if os.path.exists(path):
        return path

    # Project relative path
    project_path = os.path.join(
        BASE_DIR,
        path
    )

    if os.path.exists(project_path):
        return project_path

    # Windows path normalization
    normalized_path = path.replace(
        "\\",
        os.sep
    )

    project_path = os.path.join(
        BASE_DIR,
        normalized_path
    )

    if os.path.exists(project_path):
        return project_path

    return None


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_student(certificate_no):

    conn = sqlite3.connect(DATABASE)
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
            issue_date,
            photo_path
        FROM students
        WHERE certificate_no = ?
    """, (certificate_no,))

    student = cursor.fetchone()

    conn.close()

    return student


# ============================================================
# CREATE CERTIFICATE PDF
# ============================================================

def create_certificate(certificate_no, photo_path=None):

    student = get_student(certificate_no)

    if not student:

        print()
        print("Certificate Not Found")
        print(f"Certificate No.: {certificate_no}")
        print()

        return

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
        issue_date,
        db_photo_path
    ) = student

    # ========================================================
    # NONE को EMPTY TEXT में बदलना
    # ========================================================

    registration_no = registration_no or ""
    student_name = student_name or ""
    father_name = father_name or ""
    mother_name = mother_name or ""
    date_of_birth = date_of_birth or ""
    course = course or ""
    session = session or ""
    result = result or ""
    issue_date = issue_date or ""

    # ========================================================
    # PHOTO PATH
    # ========================================================

    # अगर manually photo path नहीं दिया गया है
    # तो database से photo path लें

    if not photo_path:

        photo_path = db_photo_path

    # Actual image path खोजें

    photo_file = find_image(photo_path)

    print()
    print("Student Photo Path:")
    print(photo_path)

    print("Resolved Photo File:")
    print(photo_file)

    # ========================================================
    # ONLINE QR CODE
    # ========================================================

    qr_data = (
        f"https://Jay97089.pythonanywhere.com/verify/{cert_no}"
    )

    # ========================================================
    # CREATE QR CODE
    # ========================================================

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image()

    qr_filename = os.path.join(
        BASE_DIR,
        "certificate_qr.png"
    )

    qr_image.save(qr_filename)

    # ========================================================
    # PDF FILE
    # ========================================================

    filename = os.path.join(
        CERTIFICATE_DIR,
        f"{certificate_no}.pdf"
    )

    width, height = landscape(A4)

    pdf = canvas.Canvas(
        filename,
        pagesize=(width, height)
    )

    # ========================================================
    # BACKGROUND
    # ========================================================

    pdf.setFillColor(
        colors.whitesmoke
    )

    pdf.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    # ========================================================
    # OUTER BORDER
    # ========================================================

    pdf.setStrokeColor(
        colors.HexColor("#123B6D")
    )

    pdf.setLineWidth(5)

    pdf.rect(
        15 * mm,
        15 * mm,
        width - 30 * mm,
        height - 30 * mm
    )

    # ========================================================
    # INNER BORDER
    # ========================================================

    pdf.setStrokeColor(
        colors.HexColor("#D4AF37")
    )

    pdf.setLineWidth(2)

    pdf.rect(
        20 * mm,
        20 * mm,
        width - 40 * mm,
        height - 40 * mm
    )

    # ========================================================
    # INSTITUTE NAME
    # ========================================================

    pdf.setFillColor(
        colors.HexColor("#123B6D")
    )

    pdf.setFont(
        "Helvetica-Bold",
        25
    )

    pdf.drawCentredString(
        width / 2,
        height - 35 * mm,
        "LAKSHYA COMPUTER ACADEMY"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawCentredString(
        width / 2,
        height - 43 * mm,
        "Akhauripur Gola, Chausa, Buxar - 802114"
    )

    # ========================================================
    # CERTIFICATE TITLE
    # ========================================================

    pdf.setFillColor(
        colors.HexColor("#D4AF37")
    )

    pdf.setFont(
        "Helvetica-Bold",
        23
    )

    pdf.drawCentredString(
        width / 2,
        height - 57 * mm,
        "CERTIFICATE OF COMPLETION"
    )

    # ========================================================
    # CERTIFICATE NUMBER
    # ========================================================

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        30 * mm,
        height - 70 * mm,
        f"Certificate No.: {cert_no}"
    )

    pdf.drawString(
        30 * mm,
        height - 77 * mm,
        f"Registration No.: {registration_no}"
    )

    # ========================================================
    # STUDENT PHOTO
    # ========================================================

    if photo_file:

        try:

            photo_x = 235 * mm
            photo_y = 100 * mm

            photo_width = 32 * mm
            photo_height = 40 * mm

            # ------------------------------------------------
            # PHOTO BORDER
            # ------------------------------------------------

            pdf.setStrokeColor(
                colors.HexColor("#123B6D")
            )

            pdf.setLineWidth(1.5)

            pdf.rect(
                photo_x - 1 * mm,
                photo_y - 1 * mm,
                photo_width + 2 * mm,
                photo_height + 2 * mm
            )

            # ------------------------------------------------
            # PHOTO
            # ------------------------------------------------

            pdf.drawImage(
                ImageReader(photo_file),
                photo_x,
                photo_y,
                width=photo_width,
                height=photo_height,
                preserveAspectRatio=True,
                anchor="c",
                mask="auto"
            )

            # ------------------------------------------------
            # PHOTO LABEL
            # ------------------------------------------------

            pdf.setFont(
                "Helvetica-Bold",
                7
            )

            pdf.setFillColor(
                colors.black
            )

            pdf.drawCentredString(
                photo_x + photo_width / 2,
                photo_y - 4 * mm,
                "STUDENT PHOTO"
            )

            print("Student photo added successfully.")

        except Exception as e:

            print(
                "Photo could not be added:",
                e
            )

    else:

        print(
            "WARNING: Student photo not found."
        )

    # ========================================================
    # MAIN CONTENT
    # ========================================================

    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        width / 2,
        height - 85 * mm,
        "This is to certify that"
    )

    pdf.setFillColor(
        colors.HexColor("#123B6D")
    )

    pdf.setFont(
        "Helvetica-Bold",
        25
    )

    pdf.drawCentredString(
        width / 2,
        height - 99 * mm,
        student_name.upper()
    )

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        width / 2,
        height - 112 * mm,
        f"S/o / D/o {father_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 121 * mm,
        f"has successfully completed the {course} course"
    )

    pdf.drawCentredString(
        width / 2,
        height - 130 * mm,
        f"during the academic session {session}"
    )

    # ========================================================
    # RESULT
    # ========================================================

    pdf.setFillColor(
        colors.HexColor("#123B6D")
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawCentredString(
        width / 2,
        height - 145 * mm,
        f"RESULT: {result}"
    )

    # ========================================================
    # DATE DETAILS
    # ========================================================

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        35 * mm,
        35 * mm,
        f"Date of Birth: {date_of_birth}"
    )

    pdf.drawString(
        35 * mm,
        27 * mm,
        f"Issue Date: {issue_date}"
    )

    # ========================================================
    # QR CODE
    # ========================================================

    if os.path.exists(qr_filename):

        pdf.drawImage(
            qr_filename,
            width - 55 * mm,
            55 * mm,
            width=25 * mm,
            height=25 * mm,
            preserveAspectRatio=True,
            mask="auto"
        )

        pdf.setFont(
            "Helvetica-Bold",
            6
        )

        pdf.setFillColor(
            colors.black
        )

        pdf.drawCentredString(
            width - 42.5 * mm,
            51 * mm,
            "SCAN TO VERIFY"
        )

    # ========================================================
    # DIRECTOR SIGNATURE
    # ========================================================

    signature_path = os.path.join(
        BASE_DIR,
        "director_signature.png"
    )

    if os.path.exists(signature_path):

        try:

            pdf.drawImage(
                ImageReader(signature_path),
                width - 95 * mm,
                39 * mm,
                width=30 * mm,
                height=15 * mm,
                preserveAspectRatio=True,
                mask="auto"
            )

        except Exception as e:

            print(
                "Signature could not be added:",
                e
            )

    # ========================================================
    # DIRECTOR
    # ========================================================

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawRightString(
        width - 65 * mm,
        30 * mm,
        "Director"
    )

    # ========================================================
    # DIRECTOR NAME
    # ========================================================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawRightString(
        width - 65 * mm,
        23 * mm,
        "Jay Prakash Rajbhar"
    )

    # ========================================================
    # FOOTER
    # ========================================================

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawCentredString(
        width / 2,
        18 * mm,
        "This certificate is issued by LAKSHYA COMPUTER ACADEMY."
    )

    # ========================================================
    # SAVE PDF
    # ========================================================

    pdf.save()

    # ========================================================
    # DELETE QR IMAGE
    # ========================================================

    if os.path.exists(qr_filename):

        os.remove(qr_filename)

    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    print()
    print("===================================")
    print("CERTIFICATE CREATED SUCCESSFULLY")
    print("===================================")
    print(f"Certificate No.: {cert_no}")
    print(f"Student Name   : {student_name}")
    print(f"PDF File       : {filename}")
    print(f"QR URL         : {qr_data}")
    print(f"Student Photo  : {photo_file}")
    print("===================================")
    print()

    return filename


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    certificate_no = input(
        "Enter Certificate Number: "
    ).strip()

    create_certificate(
        certificate_no
    )
