import sys
from pathlib import Path

import cv2
import pytesseract


# Adjust this path if Tesseract is not in the default location on your system.
# For most Linux distributions where tesseract is installed via apt (sudo apt install tesseract-ocr),
# the binary resides at /usr/bin/tesseract. Uncomment and modify the next line if necessary.
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def ocr_korean(image_path: Path) -> str:
    """Run OCR on the provided image and return the extracted Korean text.

    Parameters
    ----------
    image_path : Path
        Path to the image file containing Korean text.

    Returns
    -------
    str
        The text detected in the image, stripped of leading/trailing whitespace.
    """
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    # Convert to grayscale for better OCR accuracy
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Optional preprocessing: you can experiment with thresholding or noise removal here
    # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                               cv2.THRESH_BINARY, 31, 2)

    # OCR configuration: --oem 3 uses the LSTM neural net, --psm 6 treats the image as a block of text
    config = "--oem 3 --psm 6 -l kor"

    text = pytesseract.image_to_string(gray, config=config)
    return text.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_korean.py <image_path>")
        sys.exit(1)

    img_path = Path(sys.argv[1])
    extracted = ocr_korean(img_path)

    print("Extracted text:")
    print(extracted)