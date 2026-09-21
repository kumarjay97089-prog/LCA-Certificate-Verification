from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
import sqlite3
import qrcode
import os


# ==============================
# DATABASE CONNECTION
# ==============================

def get_student(certificate_no):

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
# CREATE CERTIFICATE PDF
# ==============================

def create_certificate(certificate_no):

    student = get_student(certificate_no)

    if not student:
        print("Certificate Not Found")
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
        issue_date
    ) = student

    # ==============================
    # QR CODE VERIFICATION URL
    # ==============================

    qr_data = (
        f"http://10.77.202.120:5000/verify/{cert_no}"
    )

    # ==============================
    # CREATE QR CODE
    # ==============================

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image()

    qr_filename = "certificate_qr.png"

    qr_image.save(qr_filename)

    # ==============================
    # PDF FILE
    # ==============================

    filename = f"{certificate_no}.pdf"

    width, height = landscape(A4)

    pdf = canvas.Canvas(
        filename,
        pagesize=(width, height)
    )

    # ==============================
    # BACKGROUND
    # ==============================

    pdf.setFillColor(colors.whitesmoke)

    pdf.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    # ==============================
    # OUTER BORDER
    # ==============================

    pdf.setStrokeColor(
        colors.HexColor("#123B6D")
    )

    pdf.setLineWidth(5)

    pdf.rect(
        15*mm,
        15*mm,
        width-30*mm,
        height-30*mm
    )

    # ==============================
    # INNER BORDER
    # ==============================

    pdf.setStrokeColor(
        colors.HexColor("#D4AF37")
    )

    pdf.setLineWidth(2)

    pdf.rect(
        20*mm,
        20*mm,
        width-40*mm,
        height-40*mm
    )

    # ==============================
    # INSTITUTE NAME
    # ==============================

    pdf.setFillColor(
        colors.HexColor("#123B6D")
    )

    pdf.setFont(
        "Helvetica-Bold",
        25
    )

    pdf.drawCentredString(
        width / 2,
        height - 35*mm,
        "LAKSHYA COMPUTER ACADEMY"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawCentredString(
        width / 2,
        height - 43*mm,
        "Akhauripur Gola, Chausa, Buxar - 802114"
    )

    # ==============================
    # CERTIFICATE TITLE
    # ==============================

    pdf.setFillColor(
        colors.HexColor("#D4AF37")
    )

    pdf.setFont(
        "Helvetica-Bold",
        23
    )

    pdf.drawCentredString(
        width / 2,
        height - 57*mm,
        "CERTIFICATE OF COMPLETION"
    )

    # ==============================
    # CERTIFICATE NUMBER
    # ==============================

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        30*mm,
        height - 70*mm,
        f"Certificate No.: {cert_no}"
    )

    pdf.drawRightString(
        width - 30*mm,
        height - 70*mm,
        f"Registration No.: {registration_no}"
    )

    # ==============================
    # MAIN CONTENT
    # ==============================

    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        width / 2,
        height - 85*mm,
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
        height - 99*mm,
        student_name.upper()
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        width / 2,
        height - 112*mm,
        f"S/o / D/o {father_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 121*mm,
        f"has successfully completed the {course} course"
    )

    pdf.drawCentredString(
        width / 2,
        height - 130*mm,
        f"during the academic session {session}"
    )

    # ==============================
    # RESULT
    # ==============================

    pdf.setFillColor(
        colors.HexColor("#123B6D")
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawCentredString(
        width / 2,
        height - 145*mm,
        f"RESULT: {result}"
    )

    # ==============================
    # DATE DETAILS
    # ==============================

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        35*mm,
        35*mm,
        f"Date of Birth: {date_of_birth}"
    )

    pdf.drawString(
        35*mm,
        27*mm,
        f"Issue Date: {issue_date}"
    )

    # ==============================
    # DIRECTOR
    # ==============================

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawRightString(
        width - 65*mm,
        38*mm,
        "Director"
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawRightString(
        width - 65*mm,
        30*mm,
        "R.K. Singh"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawRightString(
        width - 65*mm,
        23*mm,
        "M.Sc., B.Ed."
    )

    # ==============================
    # QR CODE
    # ==============================

    qr_size = 32*mm

    pdf.drawImage(
        qr_filename,
        width - 58*mm,
        25*mm,
        qr_size,
        qr_size
    )

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    pdf.drawCentredString(
        width - 42*mm,
        21*mm,
        "SCAN TO VERIFY"
    )

    # ==============================
    # FOOTER
    # ==============================

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawCentredString(
        width / 2,
        18*mm,
        "This certificate is issued by LAKSHYA COMPUTER ACADEMY."
    )

    # ==============================
    # SAVE PDF
    # ==============================

    pdf.save()

    # Delete temporary QR image

    if os.path.exists(qr_filename):
        os.remove(qr_filename)

    print("===================================")
    print("CERTIFICATE CREATED SUCCESSFULLY")
    print("===================================")
    print(f"File: {filename}")
    print("QR CODE VERIFICATION URL ADDED")


# ==============================
# TEST CERTIFICATE
# ==============================

create_certificate("LCA-ADCA-2026-0001")