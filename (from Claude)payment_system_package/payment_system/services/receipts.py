"""Receipt helpers built on pip modules: qrcode, Pillow, reportlab."""
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A5
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def qr_payload(txn):
    return (f"TXN:{txn.txn_id}|PAYER:{txn.payer}|METHOD:{txn.method}|"
            f"AMOUNT:PHP {txn.amount:.2f}|STATUS:{txn.status}")


def make_qr_image(txn, box_size=5):
    """Return a Pillow image containing a QR code for the transaction."""
    qr = qrcode.QRCode(box_size=box_size, border=2)
    qr.add_data(qr_payload(txn))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").get_image()
    return img.convert("RGB")


def export_pdf_receipt(txn, path):
    """Write a one-page PDF receipt using reportlab."""
    width, height = A5
    c = canvas.Canvas(path, pagesize=A5)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "PAYMENT RECEIPT")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, height - 66, "Polymorphism Demo - TIP Manila")
    c.line(40, height - 78, width - 40, height - 78)

    rows = [
        ("Transaction ID", txn.txn_id),
        ("Date / Time", txn.time_str),
        ("Payer", txn.payer),
        ("Method", txn.method),
        ("Amount due", f"PHP {txn.amount:.2f}"),
        ("Status", txn.status),
    ]
    y = height - 105
    for label, value in rows:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(45, y, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(150, y, str(value))
        y -= 20

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(45, y - 5, "Details:")
    text = c.beginText(45, y - 20)
    text.setFont("Helvetica", 9)
    line = ""
    for word in txn.message.split():
        if c.stringWidth(line + " " + word, "Helvetica", 9) > width - 90:
            text.textLine(line.strip())
            line = ""
        line += " " + word
    text.textLine(line.strip())
    c.drawText(text)

    qr = make_qr_image(txn, box_size=4)
    c.drawImage(ImageReader(qr), (width - 110) / 2, 40, 110, 110)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 30, "Scan to verify transaction")

    c.showPage()
    c.save()
    return path
