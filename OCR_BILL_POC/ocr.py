import easyocr
import cv2

from preprocess import preprocess_image

print("Loading EasyOCR Model...")

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

print("EasyOCR Loaded Successfully")


def extract_text(image_path):
    """
    Extract text from invoice image.

    Returns:
        Full OCR text as one string.
    """

    processed = preprocess_image(image_path)

    result = reader.readtext(
        processed,
        detail=1,
        paragraph=False
    )

    lines = []

    print("\nDetected Text")
    print("-" * 60)

    for item in result:

        bbox = item[0]

        text = item[1].strip()

        confidence = item[2]

        if confidence < 0.35:
            continue

        print(f"{confidence:.2f} : {text}")

        lines.append(text)

    print("-" * 60)

    return "\n".join(lines)