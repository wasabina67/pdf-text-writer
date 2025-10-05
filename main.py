import io

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from config import page_data


def add_text_to_pdf():
    input_pdf = "./pdf/sample.pdf"
    output_pdf = "output.pdf"
    font_name = "NotoSansJP"
    font_path = "./Noto_Sans_JP/static/NotoSansJP-Regular.ttf"
    font_size = 12

    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    page = reader.pages[0]
    for pd in page_data:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont(font_name, font_size)

        can.drawString(pd["x_position"], pd["y_position"], pd["text"])
        can.save()

        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])

    writer.add_page(page)

    with open(output_pdf, "wb") as output:
        writer.write(output)


def main():
    try:
        add_text_to_pdf()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
