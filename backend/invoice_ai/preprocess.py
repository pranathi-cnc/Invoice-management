import cv2
import numpy as np


def preprocess_image(image):

    """
    image : PIL Image

    Returns:
        Processed OpenCV Image
    """

    # PIL -> NumPy
    image = np.array(image)

    # RGB -> BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.fastNlMeansDenoising(gray)

    # CLAHE
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

    sharpen = cv2.filter2D(
        thresh,
        -1,
        kernel
    )

    return sharpen