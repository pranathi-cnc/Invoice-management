import cv2
import numpy as np


def preprocess_image(image_path):
    """
    Preprocess invoice image before OCR.

    Steps:
    1. Read Image
    2. Convert to Grayscale
    3. Remove Noise
    4. Improve Contrast
    5. Adaptive Threshold
    6. Sharpen Image

    Returns:
        Processed OpenCV Image
    """

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Unable to read image: {image_path}")

    # Convert to Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove Noise
    gray = cv2.fastNlMeansDenoising(gray)

    # Improve Contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpen = cv2.filter2D(thresh, -1, kernel)

    return sharpen