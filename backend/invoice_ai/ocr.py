import easyocr

from invoice_ai.preprocess import preprocess_image

print("Loading EasyOCR Model...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

print("EasyOCR Loaded Successfully")


def extract_text(image):
    """
    image : PIL Image

    Returns:
        Extracted OCR text as a single string.
    """

    processed = preprocess_image(image)

    result = reader.readtext(
        processed,
        detail=1,
        paragraph=False
    )

    lines = []

    print("\nDetected Text")
    print("-" * 60)

    for item in result:

        # Safety check
        if len(item) != 3:
            continue

        bbox, text, confidence = item

        text = text.strip()

        if confidence < 0.35:
            continue

        print(f"{confidence:.2f} : {text}")

        lines.append(text)

    print("-" * 60)

    return "\n".join(lines)