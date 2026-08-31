from io import BytesIO
import fitz
from PIL import Image

from invoice_ai.ocr import extract_text
from invoice_ai.ai_parser import parse_invoice
from invoice_ai.excel_writer import save_invoice


def process_single_image(image, source_file):

    # OCR
    ocr_text = extract_text(image)

    

    # AI Understanding
    invoice_data = parse_invoice(ocr_text)

    invoice_data["Source File"] = source_file

    if "Items" not in invoice_data:
        invoice_data["Items"] = []

    save_invoice(invoice_data)

    return invoice_data


def process_invoice(file_bytes, source_file):

    # ---------------- PDF ----------------

    if source_file.lower().endswith(".pdf"):

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        all_pages = []

        try:

            for page_no in range(len(doc)):

                page = doc.load_page(page_no)

                pix = page.get_pixmap(dpi=300)

                image = Image.frombytes(
                    "RGB",
                    (pix.width, pix.height),
                    pix.samples
                )

                result = process_single_image(
                    image,
                    f"{source_file} - Page {page_no + 1}"
                )

                all_pages.append(result)

        finally:
            doc.close()

        return all_pages

    # ---------------- IMAGE ----------------

    image = Image.open(BytesIO(file_bytes))

    return process_single_image(image, source_file)