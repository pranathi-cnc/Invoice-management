import os
import tempfile
import fitz

from ocr import extract_text
from ai_parser import parse_invoice
from excel_writer import save_invoice


INPUT_FOLDER = "input"

SUPPORTED_FILES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".pdf"
)


def process_invoice(image_path, source_file):

    # OCR
    ocr_text = extract_text(image_path)

    # AI Understanding
    invoice_data = parse_invoice(ocr_text)

    # Store source file
    invoice_data["Source File"] = source_file

    # Ensure Items exists
    if "Items" not in invoice_data:
        invoice_data["Items"] = []

    # Save to Excel
    save_invoice(invoice_data)


def main():

    files = [
        file
        for file in os.listdir(INPUT_FOLDER)
        if file.lower().endswith(SUPPORTED_FILES)
    ]

    if not files:
        print("No invoices found.")
        return

    print(f"\nFound {len(files)} invoice(s).\n")

    for file in files:

        print("=" * 80)
        print(f"Processing : {file}")

        path = os.path.join(INPUT_FOLDER, file)

        try:

            # ---------------- PDF ---------------- #

            if file.lower().endswith(".pdf"):

                doc = fitz.open(path)

                for page_no in range(len(doc)):

                    page = doc.load_page(page_no)

                    pix = page.get_pixmap(dpi=300)

                    with tempfile.NamedTemporaryFile(
                        suffix=".png",
                        delete=False
                    ) as temp:

                        temp_path = temp.name

                    pix.save(temp_path)

                    print(f"Processing Page {page_no + 1}")

                    process_invoice(
                        temp_path,
                        f"{file} - Page {page_no + 1}"
                    )

                    os.remove(temp_path)

                doc.close()

            # ---------------- Images ---------------- #

            else:

                process_invoice(path, file)

            print(f"✓ {file} completed successfully.\n")

        except Exception as e:

            print(f"✗ Error processing {file}")
            print(e)

    print("=" * 80)
    print("All invoices processed successfully.")


if __name__ == "__main__":
    main()